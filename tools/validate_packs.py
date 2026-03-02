#!/usr/bin/env python3
"""
Validate pack structure under packs/ (or given path).
Checks: pack.yml present, rules .mdc with frontmatter description, commands .md non-empty,
agents dir and files exist, no duplicate command names per pack.
Exit non-zero on any failure.
"""
from __future__ import annotations

import argparse
import os
import re
import sys


CURSOR_DIR = ".cursor"
RULES = "rules"
COMMANDS = "commands"
AGENTS = "agents"
PACK_YML = "pack.yml"


def read_frontmatter(path: str):
    """Return (frontmatter dict, error message or None). frontmatter has at least 'description' if valid."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError as e:
        return {}, str(e)
    if not content.strip().startswith("---"):
        return {}, "Missing YAML frontmatter (must start with ---)"
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, "Frontmatter not closed (need --- ... ---)"
    block = parts[1].strip()
    data = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            k, v = k.strip(), v.strip()
            if v and v[0] in '"\'':
                v = v.strip(v[0])
            data[k] = v
    if "description" not in data:
        return data, "Frontmatter must include 'description'"
    return data, None


def validate_pack(pack_path: str, pack_name: str) -> list[str]:
    errors = []
    # pack.yml
    pack_yml = os.path.join(pack_path, PACK_YML)
    if not os.path.isfile(pack_yml):
        errors.append(f"{pack_name}: missing {PACK_YML}")
        return errors

    cursor_dir = os.path.join(pack_path, CURSOR_DIR)
    if not os.path.isdir(cursor_dir):
        if pack_name != "_shared":
            errors.append(f"{pack_name}: missing .cursor/")
        return errors

    # rules
    rules_dir = os.path.join(cursor_dir, RULES)
    if os.path.isdir(rules_dir):
        for name in os.listdir(rules_dir):
            if not name.endswith(".mdc"):
                continue
            path = os.path.join(rules_dir, name)
            if not os.path.isfile(path):
                continue
            _, err = read_frontmatter(path)
            if err:
                errors.append(f"{pack_name}: rule {name}: {err}")

    # commands
    commands_dir = os.path.join(cursor_dir, COMMANDS)
    cmd_names = []
    if os.path.isdir(commands_dir):
        for name in os.listdir(commands_dir):
            if not name.endswith(".md"):
                continue
            path = os.path.join(commands_dir, name)
            if not os.path.isfile(path):
                continue
            base = os.path.splitext(name)[0]
            if base in cmd_names:
                errors.append(f"{pack_name}: duplicate command name: {base}")
            cmd_names.append(base)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    if len(f.read().strip()) == 0:
                        errors.append(f"{pack_name}: command {name} is empty")
            except OSError as e:
                errors.append(f"{pack_name}: command {name}: {e}")

    # agents: require .cursor/agents/ for non-_shared packs that have commands
    agents_dir = os.path.join(cursor_dir, AGENTS)
    if pack_name != "_shared" and os.path.isdir(commands_dir) and cmd_names:
        if not os.path.isdir(agents_dir):
            errors.append(f"{pack_name}: missing .cursor/agents/")
        else:
            for name in os.listdir(agents_dir):
                path = os.path.join(agents_dir, name)
                if os.path.isfile(path) and not name.endswith(".md"):
                    errors.append(f"{pack_name}: agent {name} should be .md")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate pack structure")
    parser.add_argument("root", nargs="?", default="packs", help="Root directory containing packs (default: packs)")
    args = parser.parse_args()

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print(f"Error: {root} is not a directory", file=sys.stderr)
        return 1

    cursor_root = os.path.join(root, "cursor")
    if not os.path.isdir(cursor_root):
        cursor_root = root
    all_errors = []
    for name in sorted(os.listdir(cursor_root)):
        pack_path = os.path.join(cursor_root, name)
        if not os.path.isdir(pack_path) or name.startswith("."):
            continue
        all_errors.extend(validate_pack(pack_path, name))

    if all_errors:
        for e in all_errors:
            print(e, file=sys.stderr)
        return 1
    print("Validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
