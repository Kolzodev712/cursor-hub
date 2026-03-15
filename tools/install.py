#!/usr/bin/env python3
"""
Install Cursor packs from cursor-hub into a target project.
Always includes _shared. Put the target directory last.

Usage:
  python tools/install.py [options] <pack> [pack ...] <target_dir>
  python tools/install.py all ../my-project
  python tools/install.py --lang python all ../my-project

Alternatively use the CLI (from repo root or after pip install -e .):
  cursor-hub install --lang rust all .
  python -m cursor_hub install all ../my-project
"""
from __future__ import annotations

import os
import sys

# Ensure repo root is on path so cursor_hub can be imported when run as tools/install.py
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.normpath(os.path.join(_SCRIPT_DIR, ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from cursor_hub import installer


def get_hub_root_for_script() -> str | None:
    """Find hub root when running as tools/install.py: cwd, then script's repo."""
    root = installer.get_hub_root()
    if root:
        return root
    return installer.get_hub_root(_REPO_ROOT)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Install Cursor packs into a target project.")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be done without writing")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing rule/command/agent files")
    parser.add_argument("--target", "-t", metavar="DIR", help="Target project directory (else last arg is target)")
    parser.add_argument(
        "--lang",
        "-l",
        metavar="LANG",
        action="append",
        help="Language shortcut (e.g. rust, python, js-ts, terraform). May be repeated.",
    )
    parser.add_argument(
        "packs",
        nargs="+",
        help="Pack name(s) then target dir as last arg. Use 'all' for all Rust packs.",
    )
    args = parser.parse_args()

    if args.target:
        target = os.path.abspath(args.target)
        pack_names = list(args.packs)
    elif len(args.packs) == 1:
        pack_names = list(args.packs)
        target = os.path.abspath(os.getcwd())
    else:
        pack_names = list(args.packs[:-1])
        target = os.path.abspath(args.packs[-1])

    pack_names = installer.expand_pack_names(pack_names, args.lang)
    repo_root = get_hub_root_for_script()
    if not repo_root:
        print(
            "Error: Could not find cursor-hub root (run from inside the hub repo or run install.py from the hub's tools/ dir).",
            file=sys.stderr,
        )
        return 1

    return installer.run_install(
        repo_root,
        target,
        pack_names,
        overwrite=args.overwrite,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    sys.exit(main())
