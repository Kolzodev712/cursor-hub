#!/usr/bin/env python3
"""
Verify that a workflow step was recorded in the design log.
Run this after a workflow command (not after standalone commands) to check that
the design log was created or updated. Use --step to validate a specific step type.

Modern logs append an exact stamp line when a workflow step finishes:
  [cursor-hub workflow] step=<step-name>

Legacy logs are still accepted if they contain the old section titles (see STEP_LEGACY_MARKERS).

Usage:
  python .cursor/tools/validate_workflow_design_log.py [--step STEP] [--dir DESIGN_LOG_DIR]
  From project root after running a workflow command.

Steps: design-review | implement | add-tests | investigation | proposed-solution | resolution
Exit: 0 if validation passes; 1 otherwise.
"""
from __future__ import annotations

import argparse
import os
import sys
import time

WORKFLOW_STEP_STAMP_PREFIX = "[cursor-hub workflow] step="

# Legacy-only section sets (substring match): all markers in one inner list must appear.
STEP_LEGACY_MARKERS: dict[str, list[list[str]]] = {
    "design-review": [["Design discussion"]],
    "implement": [["Implementation Results"]],
    "add-tests": [["Test session"]],
    "investigation": [["Investigation"]],
    "proposed-solution": [["Proposed solution", "Trade-offs"]],
    "resolution": [["Resolution"]],
}

ALL_SECTION_MARKERS = [
    "Design discussion",
    "Investigation",
    "Proposed solution",
    "Trade-offs",
    "Resolution",
    "Problem / context",
    "Decision",
    "Alternatives",
    "Consequences",
    "Implementation results",
    "Impact",
    "Detection / repro",
    "Root cause",
    "Fix",
    "Caveats / follow-ups",
    "Verification",
    "Implementation Results",
    "Test session",
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


def file_contains_markers(path: str, markers: list[str]) -> bool:
    """Return True if file at path contains all of the given markers (substrings)."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError:
        return False
    return all(marker in content for marker in markers)


def file_matches_any_marker_set(path: str, marker_sets: list[list[str]]) -> bool:
    """Return True if file contains all markers for any acceptable set."""
    if not marker_sets:
        return False
    for markers in marker_sets:
        if file_contains_markers(path, markers):
            return True
    return False


def file_has_workflow_stamp_for_step(path: str, step_id: str) -> bool:
    """True if file contains an exact standalone line `[cursor-hub workflow] step=<step_id>`."""
    expected = f"{WORKFLOW_STEP_STAMP_PREFIX}{step_id}"
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip() == expected:
                    return True
    except OSError:
        return False
    return False


def file_contains_any_stamp_line(path: str) -> bool:
    """True if any line starts with WORKFLOW_STEP_STAMP_PREFIX after strip."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith(WORKFLOW_STEP_STAMP_PREFIX):
                    return True
    except OSError:
        return False
    return False


def file_matches_workflow_step(path: str, step_id: str) -> bool:
    """Stamp line for this step, or legacy markers for this step."""
    if file_has_workflow_stamp_for_step(path, step_id):
        return True
    legacy = STEP_LEGACY_MARKERS.get(step_id, [])
    return file_matches_any_marker_set(path, legacy)


def most_recent_matching_md_file_for_step(log_dir: str, step_id: str) -> tuple[str | None, float]:
    """Return most recently modified .md file that matches this workflow step."""
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
        if not file_matches_workflow_step(path, step_id):
            continue
        mtime = os.path.getmtime(path)
        if mtime > best_mtime:
            best_mtime = mtime
            best_path = path
    return best_path, best_mtime


def file_contains_any_section(path: str) -> bool:
    """Known design-log headers or any workflow stamp line."""
    if file_contains_any_stamp_line(path):
        return True
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError:
        return False
    return any(marker in content for marker in ALL_SECTION_MARKERS)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify that a workflow step was recorded in the design log.")
    parser.add_argument(
        "--step",
        choices=list(STEP_LEGACY_MARKERS.keys()),
        help="Workflow step that was just run.",
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
        match_path, _match_mtime = most_recent_matching_md_file_for_step(log_dir, args.step)
        if not match_path:
            print(
                f"validate_workflow_design_log: step '{args.step}' not recorded in any design log.",
                file=sys.stderr,
            )
            print(
                "  Expected an exact line: "
                f"`{WORKFLOW_STEP_STAMP_PREFIX}{args.step}` "
                "or legacy markers: "
                f"{STEP_LEGACY_MARKERS[args.step]}",
                file=sys.stderr,
            )
            print(f"  Most recent file: {path}", file=sys.stderr)
            return 1
        print(f"OK: design log updated with {args.step} step: {os.path.basename(match_path)}")
        return 0

    # No --step: require recent modification and workflow-related content
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
            "validate_workflow_design_log: no workflow-related content in recent file.",
            file=sys.stderr,
        )
        print(f"  File: {path}", file=sys.stderr)
        return 1
    print(f"OK: recent design log with workflow content: {os.path.basename(path)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
