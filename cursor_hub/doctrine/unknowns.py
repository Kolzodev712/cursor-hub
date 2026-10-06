"""Stable UNKNOWN field identity for doctrine setup review."""
from __future__ import annotations

from dataclasses import dataclass
from cursor_hub.doctrine.model import NOT_APPLICABLE, UNKNOWN, ComponentProfile, SetupAnswers
from cursor_hub.doctrine.render import TRAIT_KEYS


@dataclass(frozen=True)
class UnknownFieldRef:
    field_id: str
    label: str
    persist_keys: tuple[str, ...]


def _is_unknown(val: str) -> bool:
    return val.strip() == UNKNOWN or not val.strip()


def collect_unknown_fields(answers: SetupAnswers) -> list[UnknownFieldRef]:
    out: list[UnknownFieldRef] = []
    if _is_unknown(answers.repository_responsibility):
        out.append(
            UnknownFieldRef(
                "repository.responsibility",
                "Repository responsibility",
                ("architecture",),
            )
        )
    if not answers.objectives_selected:
        out.append(
            UnknownFieldRef(
                "objectives.selected",
                "Engineering objectives (selected properties)",
                ("objectives",),
            )
        )
    if answers.objectives_selected and not answers.objectives_priority:
        out.append(
            UnknownFieldRef(
                "objectives.priority",
                "Objective priority order",
                ("objectives",),
            )
        )
    if _is_unknown(answers.objectives_per_component):
        out.append(
            UnknownFieldRef(
                "objectives.scope",
                "Objectives apply repository-wide",
                ("objectives",),
            )
        )
    if answers.invariants_unknown or not answers.invariants:
        out.append(
            UnknownFieldRef(
                "invariants.list",
                "Invariants",
                ("invariants",),
            )
        )

    if _is_unknown(answers.performance_importance):
        out.append(
            UnknownFieldRef(
                "workload.performance_importance",
                "Performance materially important",
                ("workload",),
            )
        )
    for key, val in sorted(answers.workload_fields.items()):
        if val == UNKNOWN:
            out.append(
                UnknownFieldRef(
                    f"workload.field.{key}",
                    f"Workload fact: {key}",
                    ("workload",),
                )
            )

    for comp in answers.components:
        if _is_unknown(comp.responsibility):
            out.append(
                UnknownFieldRef(
                    f"component.{comp.id}.responsibility",
                    f"Component {comp.id}: responsibility",
                    ("components",),
                )
            )
        for trait in TRAIT_KEYS:
            val = getattr(comp, trait)
            if val == UNKNOWN:
                out.append(
                    UnknownFieldRef(
                        f"component.{comp.id}.trait.{trait}",
                        f"Component {comp.id}: {trait.replace('_', ' ')}",
                        ("components",),
                    )
                )
    return out


def apply_unknown_resolution(
    answers: SetupAnswers,
    field_id: str,
    raw: str,
) -> tuple[bool, str | None]:
    """Update exactly one field. raw may be U to keep UNKNOWN."""
    val = raw.strip()
    if val.lower() in ("u", "unknown"):
        return True, None
    if val.lower() in ("n/a", "na", "not applicable"):
        normalized = NOT_APPLICABLE
    else:
        normalized = val

    if field_id == "repository.responsibility":
        answers.repository_responsibility = normalized
        return True, None
    if field_id == "objectives.selected":
        answers.objectives_selected = [normalized]
        return True, None
    if field_id == "objectives.priority":
        answers.objectives_priority = [normalized]
        return True, None
    if field_id == "objectives.scope":
        low = normalized.lower()
        if low in ("yes", "y"):
            answers.objectives_per_component = "yes"
        elif low in ("no", "n"):
            answers.objectives_per_component = "no"
        else:
            answers.objectives_per_component = normalized
        return True, None
    if field_id == "invariants.list":
        answers.invariants_unknown = False
        answers.invariants = [normalized]
        return True, None
    if field_id == "workload.performance_importance":
        answers.performance_importance = normalized
        return True, None
    if field_id.startswith("workload.field."):
        key = field_id[len("workload.field.") :]
        answers.workload_fields[key] = normalized
        return True, None
    if field_id.startswith("component.") and ".trait." in field_id:
        _, rest = field_id.split("component.", 1)
        cid, trait = rest.split(".trait.", 1)
        comp = _find_component(answers, cid)
        if not comp:
            return False, f"Unknown component {cid}"
        if trait not in TRAIT_KEYS:
            return False, f"Unknown trait {trait}"
        setattr(comp, trait, normalized)
        return True, None
    if field_id.startswith("component.") and field_id.endswith(".responsibility"):
        cid = field_id[len("component.") : -len(".responsibility")]
        comp = _find_component(answers, cid)
        if not comp:
            return False, f"Unknown component {cid}"
        comp.responsibility = normalized
        return True, None
    return False, f"Unknown field id {field_id}"


def _find_component(answers: SetupAnswers, cid: str) -> ComponentProfile | None:
    for c in answers.components:
        if c.id == cid:
            return c
    return None
