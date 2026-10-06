"""Merge Cursor hooks.json fragments idempotently."""
from __future__ import annotations

import json
import os
from typing import Any

# Hub-owned hook scripts (by filename). User hooks with other commands are never replaced.
HUB_HOOK_SCRIPT_MARKERS: tuple[str, ...] = (
    "doctrine_enforcement.py",
    "doctrine_setup_gate.py",
)


def is_hub_owned_hook(entry: dict[str, Any]) -> bool:
    cmd = str(entry.get("command") or "")
    return any(marker in cmd for marker in HUB_HOOK_SCRIPT_MARKERS)


def _hook_key(entry: dict[str, Any]) -> str:
    """Stable identity for non-hub deduplication."""
    cmd = entry.get("command", "")
    matcher = entry.get("matcher", "")
    hook_type = entry.get("type", "command")
    return f"{hook_type}|{matcher}|{cmd}"


def parse_hooks_json_file(path: str) -> tuple[dict[str, Any] | None, str | None]:
    """Return (data, error). error set when file exists but is not valid hooks JSON."""
    if not os.path.isfile(path):
        return None, None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        return None, f"hooks.json exists but is invalid JSON: {e}"
    if not isinstance(data, dict):
        return None, "hooks.json must be a JSON object"
    hooks = data.get("hooks")
    if hooks is not None and not isinstance(hooks, dict):
        return None, "hooks.json: 'hooks' must be an object"
    return data, None


def load_hooks_json(path: str) -> dict[str, Any] | None:
    data, err = parse_hooks_json_file(path)
    if err:
        return None
    return data


def merge_hooks_json(
    existing: dict[str, Any] | None,
    fragment: dict[str, Any],
) -> dict[str, Any]:
    """
    Merge engineering-doctrine hook fragment:
    - Remove prior hub-owned entries for events present in the fragment.
    - Append fresh hub entries from the fragment.
    - Preserve unrelated user hooks; dedupe identical non-hub entries.
    """
    base: dict[str, Any] = {"version": 1, "hooks": {}}
    if existing:
        base["version"] = existing.get("version", 1)
        base["hooks"] = {k: list(v) for k, v in (existing.get("hooks") or {}).items()}
    frag_hooks = fragment.get("hooks") or {}
    for event, entries in frag_hooks.items():
        if not isinstance(entries, list):
            continue
        current = base["hooks"].setdefault(event, [])
        kept = [e for e in current if isinstance(e, dict) and not is_hub_owned_hook(e)]
        seen = {_hook_key(e) for e in kept if isinstance(e, dict)}
        refreshed: list[dict[str, Any]] = []
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            refreshed.append(dict(entry))
        for entry in refreshed:
            key = _hook_key(entry)
            if key in seen:
                continue
            kept.append(entry)
            seen.add(key)
        base["hooks"][event] = kept
    return base


def write_hooks_json(path: str, data: dict[str, Any], dry_run: bool) -> None:
    if dry_run:
        print(f"[dry-run] would write merged hooks.json -> {path}")
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
