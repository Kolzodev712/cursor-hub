"""Render canonical project doctrine files from setup answers."""
from __future__ import annotations

import json
import re
from typing import Any

from cursor_hub.doctrine.model import (
    NOT_APPLICABLE,
    UNKNOWN,
    SetupAnswers,
    ComponentProfile,
)
from cursor_hub.doctrine.routing import (
    doctrine_refs_for_component,
    required_project_files_for_component,
    suggested_doctrine_refs_for_component,
)

TRAIT_KEYS = (
    "correctness_critical",
    "latency_sensitive",
    "throughput_sensitive",
    "mutable_state",
    "concurrent_access",
    "explicit_sync",
    "atomics_usage",
    "alloc_sensitive",
    "numeric_compute",
    "external_data",
    "persistent_storage",
    "specialized_runtime",
    "representation_sensitive",
)

MARKER_REPO = "<!-- doctrine-setup:repository -->"
MARKER_OBJECTIVES = "<!-- doctrine-setup:objectives -->"
MARKER_INVARIANTS = "<!-- doctrine-setup:invariants -->"
MARKER_WORKLOAD = "<!-- doctrine-setup:workload -->"


def render_architecture(answers: SetupAnswers) -> str:
    body = answers.repository_responsibility.strip() or UNKNOWN
    return (
        "# Repository responsibility\n\n"
        f"{body}\n\n"
        f"{MARKER_REPO}\n"
    )


def render_objectives(answers: SetupAnswers) -> str:
    lines = ["# Engineering objectives", "", "## Selected properties", ""]
    if answers.objectives_selected:
        for o in answers.objectives_selected:
            lines.append(f"- {o}")
    else:
        lines.append(f"- {UNKNOWN}")
    lines.extend(["", "## Priority (when goals conflict)", ""])
    if answers.objectives_priority:
        for i, o in enumerate(answers.objectives_priority, 1):
            lines.append(f"{i}. {o}")
    else:
        lines.append(UNKNOWN)
    lines.extend(["", "## Scope", ""])
    scope = answers.objectives_per_component.lower()
    if scope in ("yes", "y"):
        lines.append("Applies repository-wide: yes")
    elif scope in ("no", "n"):
        lines.append("Applies repository-wide: no — individual components differ")
    else:
        lines.append(f"Applies repository-wide: {UNKNOWN}")
    lines.extend(["", MARKER_OBJECTIVES, ""])
    return "\n".join(lines)


def render_invariants(answers: SetupAnswers) -> str:
    lines = ["# Invariants", ""]
    if answers.invariants_unknown:
        lines.append(f"No known invariants yet: {UNKNOWN}")
    elif answers.invariants:
        for inv in answers.invariants:
            lines.append(f"- {inv.strip()}")
    else:
        lines.append(f"- {UNKNOWN}")
    lines.extend(["", MARKER_INVARIANTS, ""])
    return "\n".join(lines)


def render_workload(answers: SetupAnswers) -> str:
    lines = [
        "# Workload and platform facts",
        "",
        "## Performance importance",
        "",
        _fmt_perf_importance(answers.performance_importance),
        "",
        "## Workload facts",
        "",
    ]
    for key, val in sorted(answers.workload_fields.items()):
        lines.append(f"{key}: {val}")
    if not answers.workload_fields:
        lines.append(f"(no detailed workload facts recorded): {NOT_APPLICABLE}")
    lines.extend(["", MARKER_WORKLOAD, ""])
    return "\n".join(lines)


def _fmt_perf_importance(val: str) -> str:
    v = val.lower()
    if v in ("yes", "y", "1"):
        return "Performance materially important: yes"
    if v in ("no", "n", "2"):
        return "Performance materially important: no"
    if v in ("partial", "only certain components", "3"):
        return "Performance materially important: only certain components"
    return f"Performance materially important: {UNKNOWN}"


def _component_item(comp: ComponentProfile) -> dict[str, Any]:
    traits = {k: getattr(comp, k) for k in TRAIT_KEYS}
    suggested = suggested_doctrine_refs_for_component(comp)
    return {
        "id": comp.id,
        "patterns": comp.patterns,
        "required_project_files": required_project_files_for_component(comp),
        "required_doctrine_refs": doctrine_refs_for_component(comp),
        "interview": {
            "responsibility": comp.responsibility,
            "traits": traits,
            "extra_required_project_files": list(comp.extra_required_project_files),
            "extra_required_doctrine_refs": list(comp.extra_required_doctrine_refs),
            "suggested_doctrine_refs": suggested,
        },
    }


def render_components_json(answers: SetupAnswers) -> str:
    items = [_component_item(c) for c in answers.components]
    return json.dumps({"components": items}, indent=2) + "\n"


def count_unknowns_in_text(*texts: str) -> int:
    n = 0
    for text in texts:
        for line in text.splitlines():
            if re.search(r":\s*UNKNOWN\s*$", line) or line.strip() == UNKNOWN:
                n += 1
            elif re.search(r"\bUNKNOWN\b", line) and "NOT_APPLICABLE" not in line:
                if line.startswith("- ") and line.endswith(UNKNOWN):
                    n += 1
    return n


def parse_architecture(text: str) -> str:
    if MARKER_REPO in text:
        chunk = text.split(MARKER_REPO)[0]
    else:
        chunk = text
    m = re.search(r"# Repository responsibility\s*\n+(.*?)(?:\n#|\Z)", chunk, re.DOTALL)
    if m:
        return m.group(1).strip()
    # Legacy architecture template
    if "<!-- Replace" in text:
        return ""
    body = re.sub(r"^# Architecture\s*\n+", "", text, count=1).strip()
    return body if body and "<!--" not in body[:80] else ""


def parse_objectives(text: str) -> tuple[list[str], list[str], str]:
    selected: list[str] = []
    priority: list[str] = []
    scope = UNKNOWN
    if "## Selected properties" in text:
        block = text.split("## Selected properties", 1)[1]
        if "## Priority" in block:
            sel_part = block.split("## Priority", 1)[0]
        else:
            sel_part = block
        for line in sel_part.splitlines():
            if line.startswith("- "):
                val = line[2:].strip()
                if val != UNKNOWN:
                    selected.append(val)
    if "## Priority" in text:
        block = text.split("## Priority", 1)[1]
        if "## Scope" in block:
            block = block.split("## Scope", 1)[0]
        for line in block.splitlines():
            m = re.match(r"^\d+\.\s*(.+)$", line.strip())
            if m and m.group(1).strip() != UNKNOWN:
                priority.append(m.group(1).strip())
    if "## Scope" in text:
        scope_line = text.split("## Scope", 1)[1].splitlines()
        for line in scope_line:
            if "repository-wide" in line.lower():
                if "no" in line.lower():
                    scope = "no"
                elif "yes" in line.lower():
                    scope = "yes"
                else:
                    scope = UNKNOWN
    return selected, priority, scope


def parse_invariants(text: str) -> tuple[list[str], bool]:
    if f"No known invariants yet: {UNKNOWN}" in text:
        return [], True
    inv: list[str] = []
    for line in text.splitlines():
        if line.startswith("- ") and UNKNOWN not in line:
            inv.append(line[2:].strip())
    return inv, False


def parse_workload(text: str) -> tuple[str, dict[str, str]]:
    perf = UNKNOWN
    fields: dict[str, str] = {}
    m = re.search(r"Performance materially important:\s*(.+)", text)
    if m:
        perf = m.group(1).strip()
    if "## Workload facts" in text:
        block = text.split("## Workload facts", 1)[1]
        if MARKER_WORKLOAD in block:
            block = block.split(MARKER_WORKLOAD)[0]
        for line in block.splitlines():
            if ":" not in line or line.startswith("#"):
                continue
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            if key.startswith("("):
                continue
            fields[key] = val
    return perf, fields


def parse_components_json(text: str) -> list[ComponentProfile]:
    raw = json.loads(text)
    out: list[ComponentProfile] = []
    for item in raw.get("components") or []:
        interview = item.get("interview") if isinstance(item.get("interview"), dict) else {}
        traits = interview.get("traits") if isinstance(interview.get("traits"), dict) else {}
        comp = ComponentProfile(
            id=str(item.get("id", "component")),
            patterns=[str(p) for p in item.get("patterns") or []],
            responsibility=str(interview.get("responsibility") or ""),
            extra_required_project_files=[
                str(x) for x in interview.get("extra_required_project_files") or []
            ],
            extra_required_doctrine_refs=[
                str(x) for x in interview.get("extra_required_doctrine_refs") or []
            ],
        )
        for k in TRAIT_KEYS:
            if k in traits:
                setattr(comp, k, str(traits[k]))
        if comp.atomics_usage == UNKNOWN and comp.explicit_sync not in (UNKNOWN, NOT_APPLICABLE, ""):
            # Legacy files without atomics_usage
            comp.atomics_usage = comp.explicit_sync
        out.append(comp)
    return out


def load_answers_from_project(paths: dict[str, str], *, project_root: str | None = None) -> SetupAnswers:
    import os

    if project_root:
        from cursor_hub.doctrine.staging import load_staging

        setup_path = paths.get("setup") or os.path.join(project_root, ".cursor", "doctrine", "setup.json")
        use_staging = True
        if os.path.isfile(setup_path):
            try:
                with open(setup_path, encoding="utf-8") as f:
                    meta = json.load(f)
                if isinstance(meta, dict) and meta.get("approved_at") and not meta.get(
                    "awaiting_final_approval"
                ):
                    use_staging = False
            except (OSError, json.JSONDecodeError):
                pass
        if use_staging:
            staged = load_staging(project_root)
            if staged is not None:
                return staged

    ans = SetupAnswers()
    if os.path.isfile(paths["architecture"]):
        with open(paths["architecture"], encoding="utf-8") as f:
            ans.repository_responsibility = parse_architecture(f.read())
    if os.path.isfile(paths["objectives"]):
        with open(paths["objectives"], encoding="utf-8") as f:
            sel, pri, scope = parse_objectives(f.read())
            ans.objectives_selected = sel
            ans.objectives_priority = pri
            ans.objectives_per_component = scope
    if os.path.isfile(paths["invariants"]):
        with open(paths["invariants"], encoding="utf-8") as f:
            inv, unk = parse_invariants(f.read())
            ans.invariants = inv
            ans.invariants_unknown = unk
    if os.path.isfile(paths["workload"]):
        with open(paths["workload"], encoding="utf-8") as f:
            perf, fields = parse_workload(f.read())
            ans.performance_importance = perf
            ans.workload_fields = fields
    if os.path.isfile(paths["components"]):
        with open(paths["components"], encoding="utf-8") as f:
            ans.components = parse_components_json(f.read())
    return ans
