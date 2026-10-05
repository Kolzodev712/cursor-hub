"""Doctrine setup data model (stdlib only)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

DOCTRINE_SETUP_SCHEMA_VERSION = 1

SetupStatus = Literal[
    "INCOMPLETE",
    "COMPLETE",
    "COMPLETE_WITH_UNKNOWNS",
    "INVALID",
    "STALE_SCHEMA",
]

SectionName = Literal["repository", "objectives", "invariants", "workload", "components"]
SectionState = Literal["incomplete", "complete"]

KNOWN = "KNOWN"
UNKNOWN = "UNKNOWN"
NOT_APPLICABLE = "NOT_APPLICABLE"

SECTIONS: tuple[SectionName, ...] = (
    "repository",
    "objectives",
    "invariants",
    "workload",
    "components",
)

DOCTRINE_REL = ".cursor/doctrine"
SETUP_FILE = f"{DOCTRINE_REL}/setup.json"
COMPONENTS_FILE = f"{DOCTRINE_REL}/components.json"
ARCHITECTURE_FILE = f"{DOCTRINE_REL}/architecture.md"
OBJECTIVES_FILE = f"{DOCTRINE_REL}/objectives.md"
INVARIANTS_FILE = f"{DOCTRINE_REL}/invariants.md"
WORKLOAD_FILE = f"{DOCTRINE_REL}/workload.md"
SKILL_PREFIX = ".cursor/skills/engineering-doctrine/decision"

VALID_SETUP_STATUSES: frozenset[str] = frozenset(
    {"INCOMPLETE", "COMPLETE", "COMPLETE_WITH_UNKNOWNS", "INVALID", "STALE_SCHEMA"}
)


@dataclass
class ComponentProfile:
    id: str
    patterns: list[str]
    responsibility: str = ""
    correctness_critical: str = UNKNOWN  # yes/no/u/na as stored strings
    latency_sensitive: str = UNKNOWN
    throughput_sensitive: str = UNKNOWN
    mutable_state: str = UNKNOWN
    concurrent_access: str = UNKNOWN
    explicit_sync: str = UNKNOWN
    alloc_sensitive: str = UNKNOWN
    numeric_compute: str = UNKNOWN
    external_data: str = UNKNOWN
    persistent_storage: str = UNKNOWN
    specialized_runtime: str = UNKNOWN
    representation_sensitive: str = UNKNOWN


@dataclass
class SetupAnswers:
    """In-memory wizard state; persisted via rendered markdown/json, not in setup.json."""

    repository_responsibility: str = ""
    objectives_selected: list[str] = field(default_factory=list)
    objectives_priority: list[str] = field(default_factory=list)
    objectives_per_component: str = UNKNOWN  # yes | no | unknown
    invariants: list[str] = field(default_factory=list)
    invariants_unknown: bool = False
    performance_importance: str = UNKNOWN  # yes | no | partial | unknown
    workload_fields: dict[str, str] = field(default_factory=dict)
    components: list[ComponentProfile] = field(default_factory=list)


def default_setup_metadata() -> dict[str, Any]:
    return {
        "schema_version": DOCTRINE_SETUP_SCHEMA_VERSION,
        "status": "INCOMPLETE",
        "sections": {s: "incomplete" for s in SECTIONS},
        "unknown_count": 0,
        "last_reviewed": None,
    }


def doctrine_paths(project_root: str) -> dict[str, str]:
    import os

    root = os.path.abspath(project_root)
    return {
        "setup": os.path.join(root, SETUP_FILE),
        "components": os.path.join(root, COMPONENTS_FILE),
        "architecture": os.path.join(root, ARCHITECTURE_FILE),
        "objectives": os.path.join(root, OBJECTIVES_FILE),
        "invariants": os.path.join(root, INVARIANTS_FILE),
        "workload": os.path.join(root, WORKLOAD_FILE),
    }
