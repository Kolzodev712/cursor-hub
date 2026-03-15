"""
cursor-hub CLI: install Cursor packs into a project.

Usage:
  cursor-hub install [options] [packs...] [target]
  cursor-hub install --lang rust all .
  cursor-hub install --lang python all ../my-project
"""
from __future__ import annotations

import argparse
import os
import sys

from . import installer


def _get_hub_root() -> str | None:
    """Hub root: from cwd, then from parent of this package (repo root when run as CLI)."""
    root = installer.get_hub_root()
    if root:
        return root
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    return installer.get_hub_root(os.path.normpath(os.path.join(pkg_dir, "..")))


def cmd_install(args: argparse.Namespace) -> int:
    target = args.target
    pack_names = installer.expand_pack_names(args.packs, args.lang)
    repo_root = _get_hub_root()
    if not repo_root:
        print(
            "Error: Could not find cursor-hub root (run from inside the hub repo or install cursor-hub from the repo).",
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


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="cursor-hub",
        description="Install Cursor packs (rules, commands, agents) into a project.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Command")

    # install
    install_parser = subparsers.add_parser("install", help="Install packs into a target directory")
    install_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be done without writing",
    )
    install_parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing rule/command/agent files",
    )
    install_parser.add_argument(
        "--target",
        "-t",
        metavar="DIR",
        help="Target project directory (default: current directory if no packs/target given)",
    )
    install_parser.add_argument(
        "--lang",
        "-l",
        metavar="LANG",
        action="append",
        help="Language shortcut (rust, python, js-ts, terraform). May be repeated.",
    )
    install_parser.add_argument(
        "packs",
        nargs="*",
        help="Pack name(s) or 'all' for full set. If target is omitted, last arg is used as target.",
    )
    install_parser.set_defaults(func=cmd_install)

    parsed = parser.parse_args()

    # Resolve target for install: --target, or last positional if multiple, or cwd
    if parsed.command == "install":
        packs = parsed.packs
        if parsed.target is not None:
            parsed.target = os.path.abspath(parsed.target)
        elif len(packs) == 0:
            parsed.target = os.path.abspath(os.getcwd())
            parsed.packs = ["all"]
        elif len(packs) == 1:
            # One arg: either "all"/pack name (target=cwd) or path (packs=all, target=arg)
            one = packs[0]
            if one in ("all", "rust") or one in installer.LANGUAGE_PACK_SETS or one.startswith(("rust-", "python-", "js-ts-", "terraform-", "design-log", "documentation", "security")):
                parsed.target = os.path.abspath(os.getcwd())
            else:
                parsed.target = os.path.abspath(one)
                parsed.packs = ["all"]
        else:
            parsed.target = os.path.abspath(packs[-1])
            parsed.packs = packs[:-1]

    return parsed.func(parsed)


if __name__ == "__main__":
    sys.exit(main())
