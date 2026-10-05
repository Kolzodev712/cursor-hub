"""Merge Cursor hooks.json fragments idempotently."""
from __future__ import annotations

import json
import os
from typing import Any


def _hook_key(entry: dict[str, Any]) -> str:
    """Stable identity for deduplication (hub-managed doctrine hooks)."""
    cmd = entry.get("command", "")
    matcher = entry.get("matcher", "")
    hook_type = entry.get("type", "command")
    return f"{hook_type}|{matcher}|{cmd}"


def merge_hooks_json(
    existing: dict[str, Any] | None,
    fragment: dict[str, Any],
) -> dict[str, Any]:
    """Merge fragment hooks into existing; dedupe by command+matcher+type."""
    base: dict[str, Any] = {"version": 1, "hooks": {}}
    if existing:
        base["version"] = existing.get("version", 1)
        base["hooks"] = {k: list(v) for k, v in (existing.get("hooks") or {}).items()}
    frag_hooks = fragment.get("hooks") or {}
    for event, entries in frag_hooks.items():
        if not isinstance(entries, list):
            continue
        current = base["hooks"].setdefault(event, [])
        seen = {_hook_key(e) for e in current if isinstance(e, dict)}
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            key = _hook_key(entry)
            if key in seen:
                continue
            current.append(entry)
            seen.add(key)
    return base


def load_hooks_json(path: str) -> dict[str, Any] | None:
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
    except (OSError, json.JSONDecodeError):
        pass
    return None


def write_hooks_json(path: str, data: dict[str, Any], dry_run: bool) -> None:
    if dry_run:
        print(f"[dry-run] would write merged hooks.json -> {path}")
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
