#!/usr/bin/env python3
"""
Optional stub: read design-log/*.md, extract metadata, output JSON lines.
Future: if MONGO_URI (and optionally MONGO_DB) are set, insert into MongoDB.
Do not overbuild; this is a placeholder for v2. See docs/ or README for purpose.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys


def extract_metadata(content: str, filename: str) -> dict:
    """Extract number, slug, title, and optional date from design log content."""
    number = None
    slug = None
    m = re.match(r"^(\d{3})-([^.]+)\.md$", filename)
    if m:
        number = int(m.group(1))
        slug = m.group(2)
    title = None
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("# ") and len(line) > 2:
            title = line[2:].strip()
            break
    # Optional: look for date in frontmatter or first lines
    date = None
    if content.strip().startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 2:
            for line in parts[1].splitlines():
                if line.strip().lower().startswith("date:"):
                    date = line.split(":", 1)[1].strip()
                    break
    return {
        "number": number,
        "slug": slug,
        "title": title,
        "date": date,
        "filename": filename,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Export design log metadata to JSON lines (Mongo insert stub).")
    parser.add_argument("--dir", default="design-log", help="Design log directory (default: design-log)")
    parser.add_argument("--output", default="-", help="Output file (default: stdout)")
    args = parser.parse_args()

    log_dir = args.dir
    if not os.path.isdir(log_dir):
        print(f"Error: {log_dir} is not a directory", file=sys.stderr)
        return 1

    out = sys.stdout if args.output == "-" else open(args.output, "w", encoding="utf-8")
    try:
        for name in sorted(os.listdir(log_dir)):
            if not name.endswith(".md"):
                continue
            path = os.path.join(log_dir, name)
            if not os.path.isfile(path):
                continue
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            meta = extract_metadata(content, name)
            print(json.dumps(meta), file=out)
        # Optional: if os.environ.get("MONGO_URI"): ... insert ... (stub, not implemented)
    finally:
        if out is not sys.stdout:
            out.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
