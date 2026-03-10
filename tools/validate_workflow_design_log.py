#!/usr/bin/env python3
"""
Verify that a workflow step was recorded in the design log.
Run this after a workflow command (not after standalone commands) to check that
the design log was created or updated. Use --step to validate a specific step type.

Usage:
  python .cursor/tools/validate_workflow_design_log.py [--step STEP] [--dir DESIGN_LOG_DIR]
  From project root after running a workflow command.

Steps: design-review | implement | add-tests | investigation | proposed-solution | resolution
Exit: 0 if a design log was updated with the expected section; 1 otherwise.
"""
from __future__ import annotations

import argparse
import os
import sys
import time

# Sections we expect per step (substrings to look for in file content)
STEP_SECTIONS = {
    "design-review": ["Design discussion"],
    "implement": ["Implementation Results"],
    "add-tests": ["Test session"],
    "investigation": ["Investigation"],
    "proposed-solution": ["Proposed solution", "Trade-offs"],
    "resolution": ["Resolution"],
}

# All known section headers (for "any recent update" check)
ALL_SECTION_MARKERS = [
    "Design discussion",
    "Implementation Results",
    "Test session",
    "Investigation",
    "Proposed solution",
    "Trade-offs",
    "Resolution",
]

# Consider "recent" if modified within this many seconds (when --step not given)
RECENT_SECONDS = 300  # 5 minutes


def get_design_log_dir(dir_arg: str | None) -> str:
    """Resolve design log directory; default .cursor/design-log from cwd."""
    if dir_arg:
        return os.path.abspath(dir_arg)
    return os.path.abspath(os.path.join(os.getcwd(), ".cursor", "design-log"))


def most_recent_md_file(log_dir: str) -> tuple[str | None, float]:
    """Return (path, mtime) of the most recently modified .md file, or (None, 0)."""
    if not os.path.isdir(log_dir):
        return None, 0.0
    best_path = None
    best_mtime = 0.0
    for name in os.listdir(log_dir):
        if not name.endswith(".md"):
            continue
        path = os.path.join(log_dir, name)
        if not os.path.isfile(path):
            continue
        mtime = os.path.getmtime(path)
        if mtime > best_mtime:
            best_mtime = mtime
            best_path = path
    return best_path, best_mtime


def file_contains_sections(path: str, sections: list[str]) -> bool:
    """Return True if file at path contains all of the given section markers (substrings)."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError:
        return False
    return all(marker in content for marker in sections)


def file_contains_any_section(path: str) -> bool:
    """Return True if file contains at least one of the known section markers."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError:
        return False
    return any(marker in content for marker in ALL_SECTION_MARKERS)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify that a workflow step was recorded in the design log."
    )
    parser.add_argument(
        "--step",
        choices=list(STEP_SECTIONS.keys()),
        help="Workflow step that was just run (validates expected section is present).",
    )
    parser.add_argument(
        "--dir",
        metavar="DESIGN_LOG_DIR",
        help="Design log directory (default: .cursor/design-log from cwd).",
    )
    args = parser.parse_args()

    log_dir = get_design_log_dir(args.dir)
    path, mtime = most_recent_md_file(log_dir)

    if not path:
        print("validate_workflow_design_log: no design log file found.", file=sys.stderr)
        print(f"  Directory: {log_dir}", file=sys.stderr)
        return 1

    if args.step:
        sections = STEP_SECTIONS[args.step]
        if not file_contains_sections(path, sections):
            print(
                f"validate_workflow_design_log: expected section(s) for step '{args.step}' not found.",
                file=sys.stderr,
            )
            print(f"  Expected one of: {sections}", file=sys.stderr)
            print(f"  File: {path}", file=sys.stderr)
            return 1
        print(f"OK: design log updated with {args.step} step: {os.path.basename(path)}")
        return 0

    # No --step: require recent modification and at least one known section
    now = time.time()
    if now - mtime > RECENT_SECONDS:
        print(
            "validate_workflow_design_log: most recent design log is older than "
            f"{RECENT_SECONDS}s (run with --step to validate a specific step).",
            file=sys.stderr,
        )
        print(f"  File: {path}", file=sys.stderr)
        return 1
    if not file_contains_any_section(path):
        print(
            "validate_workflow_design_log: no known workflow section found in recent file.",
            file=sys.stderr,
        )
        print(f"  File: {path}", file=sys.stderr)
        return 1
    print(f"OK: recent design log with workflow section: {os.path.basename(path)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
