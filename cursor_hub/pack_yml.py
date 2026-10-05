"""Minimal pack.yml parsing without PyYAML (stdlib only)."""
from __future__ import annotations

import os
from typing import Any


def read_pack_yml(pack_dir: str) -> dict[str, Any]:
    path = os.path.join(pack_dir, "pack.yml")
    data: dict[str, Any] = {
        "name": os.path.basename(pack_dir),
        "skills": [],
        "hooks_merge": False,
    }
    if not os.path.isfile(path):
        return data

    current_list: str | None = None
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if stripped.startswith("- ") and current_list == "skills":
                val = stripped[2:].strip().strip("'\"")
                if val:
                    data["skills"].append(val)
                continue
            current_list = None
            if ":" not in stripped:
                continue
            key, val = stripped.split(":", 1)
            key = key.strip()
            val = val.strip().strip("'\"")
            if key == "name" and val:
                data["name"] = val
            elif key == "version" and val:
                data["version"] = val
            elif key == "skills":
                current_list = "skills"
                if val:
                    data["skills"].append(val)
            elif key == "hooks" and val.lower() in ("true", "yes", "1"):
                data["hooks_merge"] = True
            elif key == "hooks_merge" and val.lower() in ("true", "yes", "1"):
                data["hooks_merge"] = True
    return data
