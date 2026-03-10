#!/usr/bin/env python3
"""
Install Cursor packs from cursor-hub into a target project.
Always includes _shared. Put the target directory last.

Usage:
  python tools/install.py [options] <pack> [pack ...] <target_dir>
  python tools/install.py all ../my-project          # Unix
  python tools/install.py rust-design-review ../my-project

Use "all" to install every Rust pack. Target is the last argument.
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys


PACKS_ROOT = "packs"
CURSOR_DIR = ".cursor"
RULES = "rules"
COMMANDS = "commands"
AGENTS = "agents"
TOOLS_DIR = "tools"
DESIGN_LOG_DIR = "design-log"
SHARED_PACK = "_shared"
# Alias: "all" or "rust" = all Rust packs
ALL_RUST_PACKS = ["design-log", "rust-design-review", "rust-implementation", "rust-testing", "rust-bugfix", "rust-review", "documentation"]
DESIGN_LOG_README = """# Design Log

Design decisions and implementation notes live here as `NNN-short-name.md`.
Create new entries from the project root:

    python .cursor/tools/new_design_log.py --slug <short-name>

Use `--dir` to target a different directory (e.g. another repo).
"""


def find_repo_root(start: str) -> str | None:
    """Walk up from start to find a directory containing packs/cursor/_shared."""
    current = os.path.abspath(start)
    while current and current != os.path.dirname(current):
        check = os.path.join(current, PACKS_ROOT, "cursor", SHARED_PACK)
        if os.path.isdir(check):
            return current
        current = os.path.dirname(current)
    return None


def get_hub_root() -> str | None:
    """Find cursor-hub root: from cwd first, then from this script's location."""
    root = find_repo_root(os.getcwd())
    if root:
        return root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.normpath(os.path.join(script_dir, ".."))
    if os.path.isdir(os.path.join(candidate, PACKS_ROOT, "cursor", SHARED_PACK)):
        return candidate
    return None


def get_pack_dirs(repo_root: str, pack_names: list[str]) -> list[str]:
    """Resolve pack names to full paths. Always prepend _shared."""
    cursor_packs = os.path.join(repo_root, PACKS_ROOT, "cursor")
    seen = set()
    out = []
    for name in [SHARED_PACK] + [p for p in pack_names if p != SHARED_PACK]:
        if name in seen:
            continue
        path = os.path.join(cursor_packs, name)
        if not os.path.isdir(path):
            raise FileNotFoundError(f"Pack not found: {name} at {path}")
        pack_yml = os.path.join(path, "pack.yml")
        if not os.path.isfile(pack_yml):
            raise FileNotFoundError(f"Pack has no pack.yml: {name}")
        seen.add(name)
        out.append(path)
    return out


def merge_cursor_dir(src: str, dst: str, overwrite: bool, dry_run: bool) -> tuple[int, int, int]:
    """Copy contents of src/.cursor/* into dst/.cursor/*. Merge by default; overwrite replaces.
    Returns (rules_count, commands_count, agents_count) of files copied."""
    src_cursor = os.path.join(src, CURSOR_DIR)
    r, c, a = 0, 0, 0
    if not os.path.isdir(src_cursor):
        return (r, c, a)
    for sub in (RULES, COMMANDS, AGENTS):
        src_sub = os.path.join(src_cursor, sub)
        if not os.path.isdir(src_sub):
            continue
        dst_sub = os.path.join(dst, CURSOR_DIR, sub)
        if dry_run:
            for name in os.listdir(src_sub):
                f = os.path.join(src_sub, name)
                if os.path.isfile(f):
                    print(f"[dry-run] would add {os.path.join(CURSOR_DIR, sub, name)}")
            continue
        os.makedirs(dst_sub, exist_ok=True)
        for name in os.listdir(src_sub):
            src_file = os.path.join(src_sub, name)
            if not os.path.isfile(src_file):
                continue
            dst_file = os.path.join(dst_sub, name)
            if overwrite or not os.path.exists(dst_file):
                shutil.copy2(src_file, dst_file)
                if sub == RULES:
                    r += 1
                elif sub == COMMANDS:
                    c += 1
                else:
                    a += 1
    return (r, c, a)


def read_pack_version(pack_dir: str) -> str | None:
    """Read version from pack.yml if present. Returns None if missing or unparseable."""
    path = os.path.join(pack_dir, "pack.yml")
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("version:") and ":" in line:
                    val = line.split(":", 1)[1].strip().strip("'\"")
                    return val if val else None
    except OSError:
        pass
    return None


def copy_tools(repo_root: str, target: str, dry_run: bool) -> None:
    """Copy hub tools/ into target/.cursor/tools/ so scripts run from .cursor/tools in any repo."""
    src = os.path.join(repo_root, "tools")
    dst = os.path.join(target, CURSOR_DIR, TOOLS_DIR)
    if not os.path.isdir(src):
        return
    if dry_run:
        print(f"[dry-run] would copy tools/ into {CURSOR_DIR}/{TOOLS_DIR}/")
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    print(f"  Copied tools into {CURSOR_DIR}/{TOOLS_DIR}/ (run from project root: python {CURSOR_DIR}/{TOOLS_DIR}/new_design_log.py --slug <name>).")


def ensure_design_log_dir(target: str, dry_run: bool) -> None:
    """Create target/.cursor/design-log/ and README.md if missing."""
    log_dir = os.path.join(target, CURSOR_DIR, DESIGN_LOG_DIR)
    readme = os.path.join(log_dir, "README.md")
    if os.path.isfile(readme):
        return
    if dry_run:
        print(f"[dry-run] would create {CURSOR_DIR}/{DESIGN_LOG_DIR}/README.md")
        return
    os.makedirs(log_dir, exist_ok=True)
    with open(readme, "w", encoding="utf-8") as f:
        f.write(DESIGN_LOG_README)


def main() -> int:
    parser = argparse.ArgumentParser(description="Install Cursor packs into a target project.")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be done without writing")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing rule/command/agent files")
    parser.add_argument("--target", "-t", metavar="DIR", help="Target project directory (else last arg is target)")
    parser.add_argument("packs", nargs="+", help="Pack name(s) then target dir as last arg. Use 'all' for all Rust packs.")
    args = parser.parse_args()

    # Resolve target: explicit --target, or last positional arg, or cwd if only one arg
    if args.target:
        target = os.path.abspath(args.target)
        pack_names = list(args.packs)
    elif len(args.packs) == 1:
        pack_names = list(args.packs)
        target = os.path.abspath(os.getcwd())
    else:
        pack_names = list(args.packs[:-1])
        target = os.path.abspath(args.packs[-1])

    # Expand "all" or "rust" to all Rust packs
    expanded = []
    for p in pack_names:
        if p in ("all", "rust"):
            expanded.extend(ALL_RUST_PACKS)
        else:
            expanded.append(p)
    # Dedupe, keep order
    seen = set()
    pack_names = [x for x in expanded if x not in seen and not seen.add(x)]

    repo_root = get_hub_root()
    if not repo_root:
        print("Error: Could not find cursor-hub root (run from inside the hub repo or run install.py from the hub's tools/ dir)", file=sys.stderr)
        return 1

    repo_root = os.path.normpath(os.path.abspath(repo_root))
    target = os.path.normpath(os.path.abspath(target))

    # Block installing into a subfolder of the hub (e.g. .\test-project from inside the hub)
    if target == repo_root or target.startswith(repo_root + os.sep):
        print("Error: Target is inside the hub repo.", file=sys.stderr)
        print(f"  Target: {target}", file=sys.stderr)
        print(f"  Hub:    {repo_root}", file=sys.stderr)
        print("  Use a target outside the hub (e.g. ../my-project).", file=sys.stderr)
        return 1

    print(f"Target: {target}")

    try:
        pack_dirs = get_pack_dirs(repo_root, pack_names)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if not args.dry_run:
        os.makedirs(os.path.join(target, CURSOR_DIR), exist_ok=True)

    total_r, total_c, total_a = 0, 0, 0
    for pack_dir in pack_dirs:
        r, c, a = merge_cursor_dir(pack_dir, target, args.overwrite, args.dry_run)
        total_r += r
        total_c += c
        total_a += a

    ensure_design_log_dir(target, args.dry_run)

    copy_tools(repo_root, target, args.dry_run)

    if args.dry_run:
        print("Dry run complete. No files written.")
    else:
        print(f"Installed into: {target}")
        print(f"  Packs: _shared, {', '.join(pack_names)}")
        versions = []
        for pack_dir in pack_dirs:
            pack_name = os.path.basename(pack_dir)
            ver = read_pack_version(pack_dir)
            if ver:
                versions.append(f"{pack_name}={ver}")
        if versions:
            print(f"  Versions: {' '.join(versions)}")
        if total_r or total_c or total_a:
            print(f"  Added: {total_r} rules, {total_c} commands, {total_a} agents")
        else:
            print("  (No new files; target already had these. Use --overwrite to replace.)")
        print(f"  {CURSOR_DIR}/{DESIGN_LOG_DIR}/ created if missing.")
        # Verify and list so user can confirm location
        cursor_dir = os.path.join(target, CURSOR_DIR)
        if os.path.isdir(cursor_dir):
            for sub in (RULES, COMMANDS, AGENTS, DESIGN_LOG_DIR, TOOLS_DIR):
                subpath = os.path.join(cursor_dir, sub)
                if os.path.isdir(subpath):
                    n = len([f for f in os.listdir(subpath) if os.path.isfile(os.path.join(subpath, f))])
                    print(f"  -> {os.path.join(target, CURSOR_DIR, sub)} ({n} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
