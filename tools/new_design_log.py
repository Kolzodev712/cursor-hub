#!/usr/bin/env python3
"""
Create the next design log file in .cursor/design-log/ with deterministic numbering.
Run from project root, or use --dir to point at a repo's .cursor/design-log (works for any repo).

Usage:
  python .cursor/tools/new_design_log.py --slug <short-name>   # from project root
  python .cursor/tools/new_design_log.py --slug <short-name> --dir /path/to/repo/.cursor/design-log

Prints the created file path on stdout. Exit non-zero on error.
OS-independent; no external deps.
"""
from __future__ import annotations

import argparse
import os
import re
import sys


DEFAULT_DIR = ".cursor/design-log"
TEMPLATE_HEADER = """# {title}

## Background

## Problem

## Questions and Answers

## Design

## Implementation Plan

## Examples

## Trade-offs

## Verification

## Implementation Results

"""


def find_project_root(start: str) -> str | None:
    """Walk up from start to find a directory that contains .cursor. Returns None if not found."""
    current = os.path.abspath(start)
    while current and current != os.path.dirname(current):
        if os.path.isdir(os.path.join(current, ".cursor")):
            return current
        current = os.path.dirname(current)
    return None


def slug_to_title(slug: str) -> str:
    """Convert kebab-case slug to Title Case."""
    return slug.replace("-", " ").title()


def find_next_number(log_dir: str) -> int:
    """Scan log_dir for NNN-*.md, return next number (1-based)."""
    if not os.path.isdir(log_dir):
        return 1
    pattern = re.compile(r"^(\d{3})-.*\.md$")
    max_n = 0
    for name in os.listdir(log_dir):
        m = pattern.match(name)
        if m:
            max_n = max(max_n, int(m.group(1)))
    return max_n + 1


def ensure_readme(log_dir: str) -> None:
    """Create README.md in log_dir if missing."""
    readme = os.path.join(log_dir, "README.md")
    if os.path.isfile(readme):
        return
    os.makedirs(log_dir, exist_ok=True)
    with open(readme, "w", encoding="utf-8") as f:
        f.write("# Design Log\n\nDesign decisions and implementation notes live here as `NNN-short-name.md`.\n")
        f.write("Create new entries with: `python .cursor/tools/new_design_log.py --slug <short-name>`\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create next design log file with deterministic NNN.")
    parser.add_argument("--slug", required=True, help="Short kebab-case name (e.g. risk-cache)")
    parser.add_argument("--dir", default=None, help=f"Design log directory (default: <project root>/{DEFAULT_DIR})")
    parser.add_argument("--title", default=None, help="Human-readable title (default: derived from slug)")
    args = parser.parse_args()

    slug = args.slug.strip().lower().replace(" ", "-")
    if not slug:
        print("Error: --slug must be non-empty", file=sys.stderr)
        return 1
    if not re.match(r"^[a-z0-9][a-z0-9-]*$", slug):
        print("Error: --slug should be kebab-case (letters, numbers, hyphens)", file=sys.stderr)
        return 1

    if args.dir is not None:
        log_dir = args.dir
    else:
        root = find_project_root(os.getcwd())
        if root:
            log_dir = os.path.join(root, DEFAULT_DIR)
        else:
            log_dir = DEFAULT_DIR

    title = args.title or slug_to_title(slug)
    ensure_readme(log_dir)
    next_n = find_next_number(log_dir)
    filename = f"{next_n:03d}-{slug}.md"
    filepath = os.path.join(log_dir, filename)

    content = TEMPLATE_HEADER.format(title=title)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    # Print path (absolute so caller can use it from any cwd)
    print(os.path.abspath(filepath))
    return 0


if __name__ == "__main__":
    sys.exit(main())
