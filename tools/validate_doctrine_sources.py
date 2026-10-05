#!/usr/bin/env python3
"""
Structural validation for engineering-doctrine sources (no network, no claim proving).

Checks:
- skills/engineering-doctrine/SOURCES.md exists with required registry IDs
- Each reference/*.md has Epistemic status and Sources sections
- Source IDs cited in reference Sources sections exist in SOURCES.md
- Each SOURCES.md entry has Authority, Verified, URL (or in-repo policy marker)
"""
from __future__ import annotations

import argparse
import os
import re
import sys

_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SKILL_ROOT = os.path.join(_REPO_ROOT, "skills", "engineering-doctrine")
SOURCES_FILE = os.path.join(SKILL_ROOT, "SOURCES.md")
REFERENCE_DIR = os.path.join(SKILL_ROOT, "reference")

REQUIRED_SOURCE_IDS = [
    "RUST-REF-MEMORY-MODEL",
    "RUST-REF-TYPE-LAYOUT",
    "RUST-REF-TARGET-FEATURE",
    "RUST-STD-ATOMICS",
    "RUST-NOMICON-ATOMICS",
    "RUST-STD-VEC",
    "RUST-STD-COLLECTIONS",
    "RUST-STD-HASHMAP",
    "RUST-STD-BTREEMAP",
    "RUST-STD-ARCH",
    "RUST-CARGO-PROFILES",
    "RUST-RUSTC-CODEGEN",
    "LLVM-VECTORIZERS",
    "INTEL-OPT-MANUAL",
    "AMD-ZEN4-OPT",
    "AMD64-ARCH-MANUAL",
    "LINUX-FALSE-SHARING",
    "LINUX-PERF",
    "MARA-BOS-ATOMICS",
    "POLICY-CURSOR-HUB-EVIDENCE",
]

SECTION_EPISTEMIC = re.compile(r"^## Epistemic status\s*$", re.MULTILINE)
SECTION_SOURCES = re.compile(r"^## Sources\s*$", re.MULTILINE)
SOURCE_ID_HEAD = re.compile(r"^## ([A-Z0-9-]+)\s*$", re.MULTILINE)
SOURCE_ID_LINE = re.compile(r"^-\s+([A-Z0-9-]+)\s*$", re.MULTILINE)
SOURCE_ID_INLINE = re.compile(r"\b([A-Z]{2,}(?:-[A-Z0-9]+)+)\b")


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def parse_registry_ids(text: str) -> dict[str, str]:
    """Map source ID -> section body (rough)."""
    ids: dict[str, str] = {}
    parts = SOURCE_ID_HEAD.split(text)
    # parts[0] is preamble; then alternating id, body
    i = 1
    while i + 1 < len(parts):
        sid = parts[i].strip()
        body = parts[i + 1]
        ids[sid] = body
        i += 2
    return ids


def validate_registry(path: str) -> list[str]:
    errors: list[str] = []
    if not os.path.isfile(path):
        return [f"Missing {path}"]
    text = read_text(path)
    ids = parse_registry_ids(text)
    for req in REQUIRED_SOURCE_IDS:
        if req not in ids:
            errors.append(f"SOURCES.md missing required registry ID: {req}")
    for sid, body in ids.items():
        if "Verified:" not in body:
            errors.append(f"SOURCES.md [{sid}]: missing Verified date")
        if "Authority:" not in body:
            errors.append(f"SOURCES.md [{sid}]: missing Authority tier")
        if "URL:" not in body and sid != "POLICY-CURSOR-HUB-EVIDENCE":
            errors.append(f"SOURCES.md [{sid}]: missing URL")
        if "Does not establish:" not in body:
            errors.append(f"SOURCES.md [{sid}]: missing 'Does not establish' scope guard")
    return errors


def extract_sources_section(text: str) -> str:
    m = SECTION_SOURCES.search(text)
    if not m:
        return ""
    return text[m.end() :]


def validate_reference(path: str, registry_ids: set[str]) -> list[str]:
    errors: list[str] = []
    name = os.path.basename(path)
    text = read_text(path)
    if not SECTION_EPISTEMIC.search(text):
        errors.append(f"{name}: missing '## Epistemic status' section")
    src_block = extract_sources_section(text)
    if not src_block.strip():
        errors.append(f"{name}: missing '## Sources' section")
        return errors
    cited = set(SOURCE_ID_LINE.findall(src_block))
    if not cited:
        errors.append(f"{name}: Sources section has no '- ID' entries")
    for cid in cited:
        if cid not in registry_ids:
            errors.append(f"{name}: unknown source ID '{cid}' (not in SOURCES.md)")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate engineering-doctrine source structure")
    parser.add_argument("--skill-root", default=SKILL_ROOT)
    args = parser.parse_args()
    sources_path = os.path.join(args.skill_root, "SOURCES.md")
    ref_dir = os.path.join(args.skill_root, "reference")

    errors = validate_registry(sources_path)
    registry_ids = set(parse_registry_ids(read_text(sources_path)).keys()) if os.path.isfile(sources_path) else set()

    if os.path.isdir(ref_dir):
        for fname in sorted(os.listdir(ref_dir)):
            if not fname.endswith(".md"):
                continue
            errors.extend(validate_reference(os.path.join(ref_dir, fname), registry_ids))

    skill_md = os.path.join(args.skill_root, "SKILL.md")
    if os.path.isfile(skill_md) and "SOURCES.md" not in read_text(skill_md):
        errors.append("SKILL.md should mention SOURCES.md for maintainers")

    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    print("Doctrine source structure validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
