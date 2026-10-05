"""Post-install doctrine setup integration (shared by CLI install paths)."""
from __future__ import annotations

import sys

from cursor_hub.doctrine.setup import run_setup
from cursor_hub.doctrine.setup_io import ConsoleIO
from cursor_hub.doctrine.validate import validate_doctrine_setup


def post_install_doctrine_setup(
    target: str,
    pack_names: list[str],
    *,
    dry_run: bool = False,
    interactive: bool | None = None,
) -> int:
    if "engineering-doctrine" not in pack_names:
        return 0

    result = validate_doctrine_setup(target)

    if dry_run:
        print(
            "Would install/refresh engineering-doctrine assets.\n"
            f"Doctrine setup status: {result.status}.\n"
            + (
                "A real install would require interactive setup."
                if not result.ok_for_install
                else "Existing setup is sufficient."
            )
        )
        return 0

    if result.ok_for_install:
        print(f"Engineering doctrine setup: {result.status}")
        if result.unknown_count:
            print("Suggested: cursor-hub doctrine setup --review-unknowns .")
        return 0

    if interactive is None:
        interactive = sys.stdin.isatty() and sys.stdout.isatty()

    if not interactive:
        print(
            "Engineering doctrine was installed but requires repository setup.\n\n"
            "Run interactively:\n\n"
            f"    cursor-hub doctrine setup {target}\n\n"
            "No project facts were guessed.",
            file=sys.stderr,
        )
        return 1

    rc = run_setup(target, ConsoleIO())
    if rc != 0:
        return rc
    result = validate_doctrine_setup(target)
    return 0 if result.ok_for_install else 1
