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
from cursor_hub.doctrine.setup import run_setup
from cursor_hub.doctrine.setup_io import ConsoleIO
from cursor_hub.doctrine.validate import (
    format_validation_report,
    validate_doctrine_setup,
)


def _get_hub_root() -> str | None:
    """Hub root: from cwd, then from parent of this package (repo root when run as CLI)."""
    root = installer.get_hub_root()
    if root:
        return root
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    return installer.get_hub_root(os.path.normpath(os.path.join(pkg_dir, "..")))


def cmd_doctrine_setup(args: argparse.Namespace) -> int:
    target = os.path.abspath(args.target)
    return run_setup(
        target,
        ConsoleIO(),
        review=args.review,
        review_unknowns=args.review_unknowns,
    )


def cmd_doctrine_status(args: argparse.Namespace) -> int:
    target = os.path.abspath(args.target)
    result = validate_doctrine_setup(target)
    lines = [
        "Engineering Doctrine",
        "",
        f"Installed: {'yes' if os.path.isfile(os.path.join(target, '.cursor', 'rules', 'engineering-doctrine-ambient.mdc')) else 'no'}",
        "",
        f"Setup status:\n{result.status}",
        "",
        f"Schema: 2",
        "",
        "Sections:",
    ]
    for name, st in result.sections.items():
        mark = "✓" if st == "complete" else "✗"
        lines.append(f"{mark} {name}")
    lines.append(f"\nUnknown facts:\n{result.unknown_count}")
    if result.ok_for_install and result.unknown_count:
        lines.append("\nSuggested next command:\ncursor-hub doctrine setup --review-unknowns .")
    elif not result.ok_for_install:
        lines.append("\nSuggested next command:\ncursor-hub doctrine setup .")
    print("\n".join(lines))
    return 0


def cmd_doctrine_validate(args: argparse.Namespace) -> int:
    target = os.path.abspath(args.target)
    result = validate_doctrine_setup(target)
    print(format_validation_report(target, result))
    return result.exit_code


def cmd_install(args: argparse.Namespace) -> int:
    target = args.target
    pack_names = installer.expand_pack_names(args.packs, args.lang)
    repo_root = _get_hub_root()
    if not repo_root:
        print(
            "Error: Could not find cursor-hub pack source (directory containing packs/cursor/_shared).",
            file=sys.stderr,
        )
        print(
            "  Install merges rules from this repository; run from a hub clone or use "
            "`pip install -e .` at the hub root. A standalone wheel without bundled packs "
            "cannot install commands and rules.",
            file=sys.stderr,
        )
        return 1
    return installer.run_install(
        repo_root,
        target,
        pack_names,
        overwrite=args.overwrite,
        dry_run=args.dry_run,
        refresh_design_log_readme=args.refresh_design_log_readme,
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
        "--refresh-design-log-readme",
        action="store_true",
        help="Overwrite .cursor/design-log/README.md with the hub template; never touches NNN-*.md or other logs.",
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
        help="Pack name(s), language shorthand (rust/python/js-ts/terraform), or 'all' (default Rust set if no --lang). "
        "With --lang, positional 'all' is optional. If target is omitted, last arg is used as target.",
    )
    install_parser.set_defaults(func=cmd_install)

    doctrine_parser = subparsers.add_parser(
        "doctrine",
        help="Engineering doctrine repository setup and validation",
    )
    doctrine_sub = doctrine_parser.add_subparsers(dest="doctrine_cmd", required=True)

    def _doctrine_target(p: argparse.ArgumentParser) -> None:
        p.add_argument(
            "target",
            nargs="?",
            default=".",
            help="Project directory (default: current directory)",
        )

    setup_p = doctrine_sub.add_parser(
        "setup",
        help="Run or resume guided repository doctrine setup",
    )
    _doctrine_target(setup_p)
    setup_p.add_argument(
        "--review",
        action="store_true",
        help="Review or edit existing setup section-by-section",
    )
    setup_p.add_argument(
        "--review-unknowns",
        action="store_true",
        help="Review fields explicitly marked UNKNOWN",
    )
    setup_p.set_defaults(func=cmd_doctrine_setup)

    status_p = doctrine_sub.add_parser("status", help="Show doctrine setup status (read-only)")
    _doctrine_target(status_p)
    status_p.set_defaults(func=cmd_doctrine_status)

    validate_p = doctrine_sub.add_parser("validate", help="Validate doctrine setup files")
    _doctrine_target(validate_p)
    validate_p.set_defaults(func=cmd_doctrine_validate)

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
            # One arg: either pack name / language shorthand (target=cwd) or path (packs=all, target=arg)
            one = packs[0]
            if (
                one == "all"
                or one in installer.LANGUAGE_PACK_SETS
                or one.startswith(
                    (
                        "rust-",
                        "python-",
                        "js-ts-",
                        "terraform-",
                        "design-log",
                        "documentation",
                        "security",
                        "engineering-doctrine",
                    )
                )
            ):
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
