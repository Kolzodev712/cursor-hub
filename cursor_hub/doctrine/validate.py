"""Doctrine setup validation and setup.json maintenance."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from cursor_hub.doctrine.model import (
    DOCTRINE_SETUP_SCHEMA_VERSION,
    SECTIONS,
    doctrine_paths,
    default_setup_metadata,
)
from cursor_hub.doctrine_setup_gate import compute_setup_status


@dataclass
class ValidationResult:
    status: str
    issues: list[str]
    sections: dict[str, str]
    unknown_count: int

    @property
    def ok_for_install(self) -> bool:
        return self.status in ("COMPLETE", "COMPLETE_WITH_UNKNOWNS")

    @property
    def exit_code(self) -> int:
        return 0 if self.ok_for_install else 1


def finalize_setup_status(
    sections: dict[str, str],
    unknown_count: int,
    *,
    issues: list[str] | None = None,
) -> str:
    if issues:
        return "INVALID"
    if any(sections.get(s) != "complete" for s in SECTIONS):
        return "INCOMPLETE"
    if unknown_count > 0:
        return "COMPLETE_WITH_UNKNOWNS"
    return "COMPLETE"


def validate_doctrine_setup(project_root: str) -> ValidationResult:
    status, detail = compute_setup_status(project_root)
    return ValidationResult(
        status=status,
        issues=list(detail.get("issues") or []),
        sections=dict(detail.get("sections") or {}),
        unknown_count=int(detail.get("unknown_count") or 0),
    )


def write_setup_metadata(project_root: str, result: ValidationResult) -> None:
    paths = doctrine_paths(project_root)
    meta = default_setup_metadata()
    if os.path.isfile(paths["setup"]):
        try:
            with open(paths["setup"], encoding="utf-8") as f:
                existing = json.load(f)
            if isinstance(existing, dict):
                meta.update({k: v for k, v in existing.items() if k != "status"})
        except (OSError, json.JSONDecodeError):
            pass
    meta["schema_version"] = DOCTRINE_SETUP_SCHEMA_VERSION
    meta["status"] = result.status
    meta["sections"] = result.sections
    meta["unknown_count"] = result.unknown_count
    if result.ok_for_install:
        meta["last_reviewed"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if "awaiting_final_approval" not in meta:
        meta["awaiting_final_approval"] = False
    if "approval_revision" not in meta:
        meta["approval_revision"] = 0
    os.makedirs(os.path.dirname(paths["setup"]), exist_ok=True)
    with open(paths["setup"], "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
        f.write("\n")


def format_validation_report(project_root: str, result: ValidationResult) -> str:
    lines = [
        "Engineering Doctrine validation",
        "",
        f"Status: {result.status}",
        f"Schema: {DOCTRINE_SETUP_SCHEMA_VERSION}",
        "",
        "Sections:",
    ]
    for s in SECTIONS:
        st = result.sections.get(s, "incomplete")
        mark = "✓" if st == "complete" else "✗"
        lines.append(f"  {mark} {s}")
    if result.unknown_count:
        lines.append(f"\nUnknown facts: {result.unknown_count}")
    if result.issues:
        lines.append("\nIssues:")
        for issue in result.issues:
            lines.append(f"  - {issue}")
    if not result.ok_for_install:
        lines.append("\nRemediation:")
        lines.append("  cursor-hub doctrine setup .")
    return "\n".join(lines)
