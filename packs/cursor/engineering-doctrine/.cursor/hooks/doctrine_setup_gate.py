"""
Doctrine setup status (stdlib only). Copied to target `.cursor/hooks/` with doctrine_enforcement.py.
"""
from __future__ import annotations

import json
import os
import re
from typing import Any

DOCTRINE_SETUP_SCHEMA_VERSION = 2
SETUP_REL = os.path.join(".cursor", "doctrine", "setup.json")
AMBIENT_RULE = os.path.join(".cursor", "rules", "engineering-doctrine-ambient.mdc")

MARKER_REPO = "<!-- doctrine-setup:repository -->"
MARKER_OBJECTIVES = "<!-- doctrine-setup:objectives -->"
MARKER_INVARIANTS = "<!-- doctrine-setup:invariants -->"
MARKER_WORKLOAD = "<!-- doctrine-setup:workload -->"

SECTIONS = ("repository", "objectives", "invariants", "workload", "components")

SETUP_BLOCK_STATUSES = frozenset({"INCOMPLETE", "INVALID", "STALE_SCHEMA"})


def ambient_doctrine_installed(project_root: str) -> bool:
    return os.path.isfile(os.path.join(project_root, AMBIENT_RULE))


def _read(path: str) -> str:
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def _section_repository(root: str) -> tuple[bool, list[str]]:
    path = os.path.join(root, ".cursor", "doctrine", "architecture.md")
    if not os.path.isfile(path):
        return False, ["missing architecture.md"]
    text = _read(path)
    if MARKER_REPO not in text and "<!-- Replace" in text:
        return False, ["repository responsibility not configured"]
    body = text.split(MARKER_REPO)[0] if MARKER_REPO in text else text
    if "# Repository responsibility" in body:
        chunk = body.split("# Repository responsibility", 1)[1].strip()
        if not chunk:
            return False, ["repository responsibility empty"]
        return True, []
    if "<!-- Replace" in text:
        return False, ["repository responsibility not configured"]
    return True, []


def _section_objectives(root: str) -> tuple[bool, list[str]]:
    path = os.path.join(root, ".cursor", "doctrine", "objectives.md")
    if not os.path.isfile(path):
        return False, ["missing objectives.md"]
    text = _read(path)
    if MARKER_OBJECTIVES not in text and "<!-- Replace" in text:
        return False, ["objectives not configured"]
    if "## Selected properties" not in text:
        return False, ["objectives missing structured sections"]
    return True, []


def _section_invariants(root: str) -> tuple[bool, list[str]]:
    path = os.path.join(root, ".cursor", "doctrine", "invariants.md")
    if not os.path.isfile(path):
        return False, ["missing invariants.md"]
    text = _read(path)
    if MARKER_INVARIANTS not in text and "<!-- Replace" in text:
        return False, ["invariants not configured"]
    return True, []


def _section_workload(root: str) -> tuple[bool, list[str]]:
    path = os.path.join(root, ".cursor", "doctrine", "workload.md")
    if not os.path.isfile(path):
        return False, ["missing workload.md"]
    text = _read(path)
    if MARKER_WORKLOAD not in text and "<!-- Replace" in text:
        return False, ["workload not configured"]
    if "Performance materially important" not in text:
        return False, ["workload missing performance importance"]
    return True, []


def _validate_components(root: str) -> tuple[bool, list[str]]:
    path = os.path.join(root, ".cursor", "doctrine", "components.json")
    if not os.path.isfile(path):
        return False, ["missing components.json"]
    try:
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        return False, [f"components.json invalid: {e}"]
    if not isinstance(raw, dict):
        return False, ["components.json must be an object"]
    items = raw.get("components")
    if items is None:
        return False, ["components.json missing components array"]
    if not isinstance(items, list):
        return False, ["components must be a list"]
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            return False, [f"component[{i}] must be an object"]
        if not item.get("id"):
            return False, [f"component[{i}] missing id"]
        pats = item.get("patterns")
        if not isinstance(pats, list) or not pats:
            return False, [f"component[{item.get('id')}] missing patterns"]
        for ref in item.get("required_doctrine_refs") or []:
            ref_path = os.path.join(root, str(ref).replace("/", os.sep))
            if not os.path.isfile(ref_path):
                return False, [f"component[{item.get('id')}] missing doctrine ref {ref}"]
        for pf in item.get("required_project_files") or []:
            pf_path = os.path.join(root, str(pf).replace("/", os.sep))
            if not os.path.isfile(pf_path):
                return False, [f"component[{item.get('id')}] missing project file {pf}"]
    return True, []


def count_unknown_facts(root: str) -> int:
    n = 0
    for name in ("architecture.md", "objectives.md", "invariants.md", "workload.md"):
        text = _read(os.path.join(root, ".cursor", "doctrine", name))
        for line in text.splitlines():
            if re.search(r":\s*UNKNOWN\s*$", line):
                n += 1
            elif line.strip() == "UNKNOWN" and "Priority" not in line:
                n += 1
            elif line.startswith("- UNKNOWN"):
                n += 1
    return n


def compute_setup_status(project_root: str) -> tuple[str, dict[str, Any]]:
    """Return (status, detail dict with sections, issues, unknown_count)."""
    root = os.path.abspath(project_root)
    detail: dict[str, Any] = {"sections": {}, "issues": [], "unknown_count": 0}
    setup_path = os.path.join(root, SETUP_REL.replace("/", os.sep))
    meta: dict[str, Any] | None = None
    if os.path.isfile(setup_path):
        try:
            with open(setup_path, encoding="utf-8") as f:
                meta = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            detail["issues"].append(f"setup.json invalid: {e}")
            return "INVALID", detail
        if not isinstance(meta, dict):
            detail["issues"].append("setup.json must be an object")
            return "INVALID", detail
        sv = meta.get("schema_version")
        if sv != DOCTRINE_SETUP_SCHEMA_VERSION:
            detail["issues"].append(
                f"setup schema {sv!r} != required {DOCTRINE_SETUP_SCHEMA_VERSION}"
            )
            return "STALE_SCHEMA", detail
        if not meta.get("approved_at") and not meta.get("awaiting_final_approval"):
            # Structurally complete files without explicit schema v2 approval.
            pass

    def _section_components(root: str) -> tuple[bool, list[str]]:
        ok, issues = _validate_components(root)
        if not ok:
            return False, issues
        if not meta:
            return False, ["components interview not completed (run doctrine setup)"]
        if (meta.get("sections") or {}).get("components") != "complete":
            return False, ["components interview not completed in setup wizard"]
        return True, []

    checks = {
        "repository": _section_repository,
        "objectives": _section_objectives,
        "invariants": _section_invariants,
        "workload": _section_workload,
        "components": _section_components,
    }
    all_ok = True
    for name, fn in checks.items():
        ok, issues = fn(root)
        detail["sections"][name] = "complete" if ok else "incomplete"
        if not ok:
            all_ok = False
            detail["issues"].extend(issues)

    detail["unknown_count"] = count_unknown_facts(root)

    if not all_ok:
        return "INCOMPLETE", detail
    if detail["issues"]:
        return "INVALID", detail
    if meta and not meta.get("approved_at"):
        detail["issues"].append("setup not approved — confirm summary with W in doctrine setup")
        return "INCOMPLETE", detail
    if detail["unknown_count"] > 0:
        return "COMPLETE_WITH_UNKNOWNS", detail
    return "COMPLETE", detail


def setup_blocks_writes(project_root: str) -> tuple[bool, str, str]:
    """Returns (blocks, status, user_message)."""
    if not ambient_doctrine_installed(project_root):
        return False, "", ""
    status, detail = compute_setup_status(project_root)
    if status in SETUP_BLOCK_STATUSES:
        msg = (
            "Engineering doctrine repository setup is incomplete or invalid.\n\n"
            "Run:\n\n"
            "    cursor-hub doctrine setup .\n\n"
            f"Current status:\n{status}"
        )
        if detail.get("issues"):
            msg += "\n\n" + "\n".join(detail["issues"][:5])
        return True, status, msg
    return False, status, ""
