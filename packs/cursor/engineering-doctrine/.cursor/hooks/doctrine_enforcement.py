"""
Doctrine context gate — shared logic for hook script and unit tests.

Tracks Read tool paths under `.cursor/doctrine/` and required skill references;
blocks Write-family tools to classified components until requirements are met.
Stdlib only; copied to target `.cursor/hooks/` on install.
"""
from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass
from typing import Any


DOCTRINE_DIR = os.path.join(".cursor", "doctrine")
COMPONENTS_FILE = os.path.join(DOCTRINE_DIR, "components.json")
STATE_FILE = os.path.join(".cursor", "hooks", ".doctrine-gate-state.json")
STATE_VERSION = 3

MANDATORY_CREDITS = frozenset({"full_text", "hook_supplied"})
HOOK_SUPPLIED_MAX_BYTES = 512_000

WRITE_TOOLS = frozenset(
    {"Write", "StrReplace", "ApplyPatch", "Delete", "EditNotebook", "NotebookEdit"}
)
READ_TOOLS = frozenset({"Read"})

INVALID_CONFIG_AGENT_MSG = (
    "Doctrine configuration is invalid; fix `.cursor/doctrine/components.json` before continuing. "
    "Details: {detail}"
)
INVALID_CONFIG_USER_MSG = (
    "Engineering-doctrine gate: components.json exists but is invalid — substantive file writes are blocked."
)


def norm_rel_path(path: str, workspace_root: str | None) -> str:
    """Project-relative path with forward slashes (keeps leading `.cursor/` when present)."""
    if workspace_root:
        root = os.path.abspath(workspace_root)
        if os.path.isabs(path):
            ap = os.path.normpath(path)
        else:
            ap = os.path.normpath(os.path.join(root, path))
        try:
            rel = os.path.relpath(ap, root)
        except ValueError:
            rel = path
        if rel == ".":
            return ""
        return rel.replace("\\", "/")
    return path.replace("\\", "/").lstrip("./")


def path_matches_glob(rel_path: str, pattern: str) -> bool:
    rel_path = rel_path.replace("\\", "/").lstrip("./")
    pattern = pattern.replace("\\", "/").lstrip("./")
    if fnmatch.fnmatch(rel_path, pattern):
        return True
    if "**" not in pattern:
        return False
    prefix, suffix = pattern.split("**", 1)
    prefix = prefix.rstrip("/")
    suffix = suffix.lstrip("/")
    if prefix and not (rel_path == prefix or rel_path.startswith(prefix + "/")):
        return False
    if not suffix or suffix == "*":
        return True
    tail = rel_path[len(prefix) + 1 :] if prefix else rel_path
    return fnmatch.fnmatch(tail, suffix) or fnmatch.fnmatch(tail, "**/" + suffix)


@dataclass
class Component:
    id: str
    patterns: list[str]
    required_project_files: list[str]
    required_doctrine_refs: list[str]


def components_file_path(project_root: str) -> str:
    return os.path.join(project_root, COMPONENTS_FILE)


def load_components(project_root: str) -> tuple[list[Component], str | None]:
    path = components_file_path(project_root)
    if not os.path.isfile(path):
        return [], None
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        return [], f"Invalid {COMPONENTS_FILE}: {e}"
    if not isinstance(raw, dict):
        return [], f"{COMPONENTS_FILE} must be a JSON object"
    items = raw.get("components")
    if items is None:
        return [], None
    if not isinstance(items, list):
        return [], f"{COMPONENTS_FILE}: 'components' must be a list"
    out: list[Component] = []
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            return [], f"{COMPONENTS_FILE}: components[{i}] must be an object"
        cid = item.get("id")
        if not cid or not isinstance(cid, str):
            return [], f"{COMPONENTS_FILE}: components[{i}] missing string 'id'"
        patterns = item.get("patterns") or []
        if not isinstance(patterns, list):
            return [], f"{COMPONENTS_FILE}: components[{i}].patterns must be a list"
        rpf = item.get("required_project_files") or []
        rdr = item.get("required_doctrine_refs") or []
        if not isinstance(rpf, list) or not isinstance(rdr, list):
            return [], f"{COMPONENTS_FILE}: components[{i}] file lists must be arrays"
        out.append(
            Component(
                id=cid,
                patterns=[str(p) for p in patterns],
                required_project_files=[str(x).replace("\\", "/") for x in rpf],
                required_doctrine_refs=[str(x).replace("\\", "/") for x in rdr],
            )
        )
    return out, None


def match_components(rel_path: str, components: list[Component]) -> list[Component]:
    matched: list[Component] = []
    for comp in components:
        for pat in comp.patterns:
            if path_matches_glob(rel_path, pat):
                matched.append(comp)
                break
    return matched


def _explicit_conversation_id(payload: dict[str, Any]) -> str | None:
    for key in ("conversation_id", "conversationId", "session_id", "sessionId", "chat_id"):
        val = payload.get(key)
        if val:
            return str(val)
    return None


def _ephemeral_session_key(project_root: str) -> str:
    """Process+workspace scoped key when Cursor does not supply conversation_id (never shared 'default')."""
    root = os.path.abspath(project_root)
    root_tag = hashlib.sha256(root.encode("utf-8")).hexdigest()[:16]
    return f"ephemeral:pid-{os.getpid()}:root-{root_tag}"


def session_key_from_payload(payload: dict[str, Any], project_root: str) -> str:
    explicit = _explicit_conversation_id(payload)
    if explicit:
        return explicit
    return _ephemeral_session_key(project_root)


def load_state(project_root: str) -> dict[str, Any]:
    path = os.path.join(project_root, STATE_FILE)
    if not os.path.isfile(path):
        return {"version": STATE_VERSION, "sessions": {}}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and "sessions" in data:
            if "version" not in data:
                data["version"] = 1
            return data
    except (OSError, json.JSONDecodeError):
        pass
    return {"version": STATE_VERSION, "sessions": {}}


def save_state(project_root: str, state: dict[str, Any]) -> None:
    state["version"] = STATE_VERSION
    path = os.path.join(project_root, STATE_FILE)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
        f.write("\n")


def _canonical_path(rel_path: str) -> str:
    p = rel_path.replace("\\", "/")
    if p.startswith("./"):
        return p[2:]
    return p


def file_fingerprint(project_root: str, rel_path: str) -> str | None:
    """SHA-256 of file bytes for context invalidation; None if missing/unreadable."""
    key = _canonical_path(rel_path)
    abs_path = os.path.join(project_root, key)
    if not os.path.isfile(abs_path):
        return None
    try:
        h = hashlib.sha256()
        with open(abs_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return None


def mark_read(
    state: dict[str, Any],
    session: str,
    rel_path: str,
    project_root: str,
    *,
    content_sha256: str | None = None,
    credit: str = "path",
) -> None:
    sessions = state.setdefault("sessions", {})
    sess = sessions.setdefault(session, {"reads": {}})
    reads = sess.setdefault("reads", {})
    key = _canonical_path(rel_path)
    fp = file_fingerprint(project_root, key)
    if fp is None:
        reads[key] = {"sha256": None, "missing": True, "credit": credit}
    else:
        entry: dict[str, Any] = {"sha256": fp, "credit": credit}
        if content_sha256:
            entry["content_sha256"] = content_sha256
        reads[key] = entry


def _mandatory_context_satisfied(
    entry: Any,
    project_root: str,
    req_path: str,
) -> bool:
    """Mandatory reads require verified full content or hook-supplied full file version."""
    if entry is True:
        return False
    if not isinstance(entry, dict):
        return False
    if entry.get("missing"):
        return False
    credit = str(entry.get("credit") or "")
    if credit not in MANDATORY_CREDITS:
        return False
    stored = entry.get("sha256")
    if not stored or not isinstance(stored, str):
        return False
    current = file_fingerprint(project_root, req_path)
    if current is None or stored != current:
        return False
    content_sha = entry.get("content_sha256")
    if not content_sha or not isinstance(content_sha, str):
        return False
    return content_sha == current


def has_read(state: dict[str, Any], session: str, rel_path: str, project_root: str) -> bool:
    sessions = state.get("sessions", {})
    sess = sessions.get(session, {})
    reads = sess.get("reads", {})
    key = _canonical_path(rel_path)
    entry = reads.get(key)
    if entry is None and key.startswith(".cursor/"):
        entry = reads.get(key.lstrip("./"))
    if entry is None:
        return False
    return _mandatory_context_satisfied(entry, project_root, key)


def workspace_root_from_payload(payload: dict[str, Any]) -> str | None:
    for key in ("workspace_root", "workspaceRoot", "project_root", "projectRoot", "cwd"):
        val = payload.get(key)
        if val and isinstance(val, str):
            return val
    roots = payload.get("workspace_roots") or payload.get("workspaceRoots")
    if isinstance(roots, list) and roots:
        first = roots[0]
        if isinstance(first, str):
            return first
    return None


def tool_name_from_payload(payload: dict[str, Any]) -> str:
    for key in ("tool_name", "toolName", "tool"):
        val = payload.get(key)
        if isinstance(val, str):
            return val
    return ""


def tool_input_from_payload(payload: dict[str, Any]) -> dict[str, Any]:
    for key in ("tool_input", "toolInput", "input", "arguments"):
        val = payload.get(key)
        if isinstance(val, dict):
            return val
    return {}


def file_path_from_tool_input(tool_input: dict[str, Any]) -> str | None:
    for key in ("path", "file_path", "filePath", "target_file", "targetFile"):
        val = tool_input.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()
    return None


def extract_write_paths(tool: str, tool_input: dict[str, Any]) -> tuple[list[str], str | None]:
    """Return project-relative paths affected by a mutation tool, or ( [], error )."""
    if tool in ("Write", "StrReplace", "Delete", "EditNotebook", "NotebookEdit"):
        p = file_path_from_tool_input(tool_input)
        if not p:
            return [], f"{tool}: missing path in tool_input"
        return [p], None
    if tool == "ApplyPatch":
        p = file_path_from_tool_input(tool_input)
        if p:
            return [p], None
        patch = tool_input.get("patch") or tool_input.get("patchText") or tool_input.get("text")
        if isinstance(patch, str) and patch.strip():
            paths: list[str] = []
            for m in re.finditer(r"^\*\*\* (?:Update|Add|Delete) File: (.+)$", patch, re.MULTILINE):
                paths.append(m.group(1).strip())
            for m in re.finditer(r"^\+\+\+ [ab]/(.+)$", patch, re.MULTILINE):
                paths.append(m.group(1).strip())
            if paths:
                deduped = list(dict.fromkeys(paths))
                return deduped, None
        files = tool_input.get("files")
        if isinstance(files, list):
            out = [str(x) for x in files if isinstance(x, str) and x.strip()]
            if out:
                return out, None
        return [], "ApplyPatch: cannot determine affected file paths"
    return [], f"Unsupported mutation tool for path extraction: {tool}"


def read_result_text_from_payload(payload: dict[str, Any]) -> str | None:
    for key in ("tool_output", "toolOutput", "output", "result"):
        val = payload.get(key)
        if isinstance(val, dict):
            for inner in ("content", "text", "stdout", "output"):
                t = val.get(inner)
                if isinstance(t, str) and t.strip():
                    return t
        elif isinstance(val, str) and val.strip():
            return val
    return None


def _path_escape_blocked(project_root: str, rel: str) -> bool:
    root = os.path.abspath(project_root)
    rel = rel.replace("\\", "/").lstrip("./")
    if rel.startswith("../") or "/../" in f"/{rel}/":
        return True
    abs_path = os.path.normpath(os.path.join(root, rel))
    try:
        common = os.path.commonpath([root, abs_path])
    except ValueError:
        return True
    return common != root


def handle_pre_compact(payload: dict[str, Any], project_root: str) -> dict[str, Any]:
    state = load_state(project_root)
    session = session_key_from_payload(payload, project_root)
    sessions = state.get("sessions", {})
    if session in sessions:
        sessions[session]["reads"] = {}
        save_state(project_root, state)
    return {"permission": "allow"}


def missing_requirements(
    state: dict[str, Any],
    session: str,
    components: list[Component],
    project_root: str,
) -> list[str]:
    missing: list[str] = []
    seen: set[str] = set()
    for comp in components:
        for req in comp.required_project_files + comp.required_doctrine_refs:
            req = _canonical_path(req)
            if req in seen:
                continue
            seen.add(req)
            if not has_read(state, session, req, project_root):
                missing.append(req)
    return missing


def deny_invalid_config(cfg_err: str) -> dict[str, Any]:
    return {
        "permission": "deny",
        "agent_message": INVALID_CONFIG_AGENT_MSG.format(detail=cfg_err),
        "user_message": INVALID_CONFIG_USER_MSG,
    }


def handle_track_read(payload: dict[str, Any], project_root: str) -> dict[str, Any]:
    tool = tool_name_from_payload(payload)
    if tool not in READ_TOOLS:
        return {"permission": "allow"}
    tool_input = tool_input_from_payload(payload)
    fpath = file_path_from_tool_input(tool_input)
    if not fpath:
        return {"permission": "allow"}
    ws = workspace_root_from_payload(payload) or project_root
    rel = norm_rel_path(fpath, ws)
    if not (
        rel.startswith(".cursor/doctrine/")
        or rel.startswith("cursor/doctrine/")
        or rel.startswith(".cursor/skills/")
        or rel.startswith("cursor/skills/")
        or rel in (COMPONENTS_FILE, COMPONENTS_FILE.lstrip("./"))
    ):
        return {"permission": "allow"}
    state = load_state(project_root)
    session = session_key_from_payload(payload, project_root)
    body = read_result_text_from_payload(payload)
    file_fp = file_fingerprint(project_root, rel)
    content_hash = hashlib.sha256(body.encode("utf-8")).hexdigest() if body else None
    if body and file_fp and content_hash == file_fp:
        credit = "full_text"
    elif body:
        credit = "partial_text"
    else:
        credit = "path_only"
    mark_read(
        state,
        session,
        rel,
        project_root,
        content_sha256=content_hash if credit == "full_text" else None,
        credit=credit,
    )
    out: dict[str, Any] = {"permission": "allow"}
    if credit == "path_only" and file_fp:
        abs_path = os.path.join(project_root, rel.replace("/", os.sep))
        try:
            with open(abs_path, "rb") as f:
                raw = f.read(HOOK_SUPPLIED_MAX_BYTES + 1)
            if len(raw) <= HOOK_SUPPLIED_MAX_BYTES:
                full_text = raw.decode("utf-8", errors="replace")
                supplied_hash = hashlib.sha256(raw).hexdigest()
                if supplied_hash == file_fp:
                    mark_read(
                        state,
                        session,
                        rel,
                        project_root,
                        content_sha256=supplied_hash,
                        credit="hook_supplied",
                    )
                    out["additional_context"] = (
                        "Doctrine gate: mandatory context for "
                        f"`{rel}` (credit=hook_supplied):\n\n{full_text}"
                    )
        except OSError:
            pass
    save_state(project_root, state)
    return out


def _load_setup_gate():
    hook_dir = os.path.dirname(os.path.abspath(__file__))
    if hook_dir not in sys.path:
        sys.path.insert(0, hook_dir)
    try:
        import doctrine_setup_gate as gate  # type: ignore[import-not-found]
    except ImportError:
        from cursor_hub import doctrine_setup_gate as gate  # type: ignore[no-redef]
    return gate


def handle_gate_write(payload: dict[str, Any], project_root: str) -> dict[str, Any]:
    tool = tool_name_from_payload(payload)
    if tool not in WRITE_TOOLS:
        return {"permission": "allow"}
    tool_input = tool_input_from_payload(payload)
    paths, path_err = extract_write_paths(tool, tool_input)
    if path_err:
        return {
            "permission": "deny",
            "agent_message": f"Doctrine gate cannot classify this edit safely: {path_err}",
            "user_message": "Doctrine gate: unrecognized mutation payload.",
        }
    if not paths:
        return {"permission": "allow"}
    ws = workspace_root_from_payload(payload) or project_root
    rel_paths = [norm_rel_path(p, ws) for p in paths]
    for rel in rel_paths:
        if _path_escape_blocked(project_root, rel):
            return {
                "permission": "deny",
                "agent_message": f"Blocked path outside workspace: {rel}",
                "user_message": "Doctrine gate: path traversal blocked.",
            }

    gate = _load_setup_gate()
    blocks, _status, user_msg = gate.setup_blocks_writes(project_root)
    if blocks:
        return {
            "permission": "deny",
            "agent_message": user_msg,
            "user_message": "Engineering doctrine setup must be completed before classified edits.",
        }

    components, cfg_err = load_components(project_root)
    if cfg_err and os.path.isfile(components_file_path(project_root)):
        return deny_invalid_config(cfg_err)

    if not components:
        return {"permission": "allow"}

    matched_all: list[Component] = []
    for rel in rel_paths:
        matched_all.extend(match_components(rel, components))
    if not matched_all:
        return {"permission": "allow"}

    state = load_state(project_root)
    session = session_key_from_payload(payload, project_root)
    seen_ids: set[str] = set()
    matched_unique: list[Component] = []
    for c in matched_all:
        if c.id not in seen_ids:
            seen_ids.add(c.id)
            matched_unique.append(c)
    missing = missing_requirements(state, session, matched_unique, project_root)
    if missing:
        comp_ids = ", ".join(sorted({c.id for c in matched_unique}))
        targets = ", ".join(rel_paths)
        lines = "\n".join(f"  - {m}" for m in missing)
        msg = (
            f"Write blocked for classified component(s) [{comp_ids}]. "
            f"Read the **current** contents of these paths with the Read tool before editing ({targets}):\n{lines}\n"
            "Also load the engineering-doctrine skill when doctrine references are listed."
        )
        return {
            "permission": "deny",
            "agent_message": msg,
            "user_message": "Doctrine context gate: required reads not recorded for this session.",
        }
    return {"permission": "allow"}


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) < 1:
        print(json.dumps({"permission": "allow"}))
        return 0
    mode = argv[0]
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        payload = {}
    if not isinstance(payload, dict):
        payload = {}
    project_root = os.getcwd()
    ws = workspace_root_from_payload(payload)
    if ws:
        project_root = ws

    if mode == "track-read":
        out = handle_track_read(payload, project_root)
    elif mode == "gate-write":
        out = handle_gate_write(payload, project_root)
    elif mode == "pre-compact":
        out = handle_pre_compact(payload, project_root)
    else:
        out = {"permission": "allow"}
    print(json.dumps(out))
    if out.get("permission") == "deny":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
