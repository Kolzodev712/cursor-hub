"""Deterministic component traits → engineering-doctrine decision paths."""
from __future__ import annotations

from cursor_hub.doctrine.model import SKILL_PREFIX, ComponentProfile, UNKNOWN, NOT_APPLICABLE

DECISION_FILES: dict[str, str] = {
    "algorithm-selection": f"{SKILL_PREFIX}/algorithm-selection.md",
    "data-layout": f"{SKILL_PREFIX}/data-layout.md",
    "memory": f"{SKILL_PREFIX}/memory.md",
    "allocation": f"{SKILL_PREFIX}/allocation.md",
    "concurrency": f"{SKILL_PREFIX}/concurrency.md",
    "atomics": f"{SKILL_PREFIX}/atomics.md",
    "cpu-execution": f"{SKILL_PREFIX}/cpu-execution.md",
    "io": f"{SKILL_PREFIX}/io.md",
    "benchmarking": f"{SKILL_PREFIX}/benchmarking.md",
    "evidence": f"{SKILL_PREFIX}/evidence.md",
}

ORDER = (
    "algorithm-selection",
    "data-layout",
    "memory",
    "allocation",
    "concurrency",
    "atomics",
    "cpu-execution",
    "io",
    "benchmarking",
    "evidence",
)


def _yes(val: str) -> bool:
    return val.lower() in ("yes", "y", "true", "1")


def _active(val: str) -> bool:
    return val not in (UNKNOWN, NOT_APPLICABLE, "", "no", "n", "false", "0")


def domains_for_component(comp: ComponentProfile) -> list[str]:
    domains: set[str] = set()
    perf = _yes(comp.latency_sensitive) or _yes(comp.throughput_sensitive)
    if _active(comp.representation_sensitive) or _yes(comp.representation_sensitive):
        domains.add("algorithm-selection")
        domains.add("data-layout")
    if perf or _yes(comp.alloc_sensitive):
        domains.add("memory")
    if _yes(comp.alloc_sensitive):
        domains.add("allocation")
    if _yes(comp.concurrent_access) or _yes(comp.mutable_state):
        domains.add("concurrency")
    if _yes(comp.explicit_sync):
        domains.add("atomics")
    if _yes(comp.numeric_compute):
        domains.add("cpu-execution")
    if _yes(comp.external_data):
        domains.add("io")
    if perf:
        domains.add("benchmarking")
        domains.add("evidence")
    if _yes(comp.correctness_critical):
        domains.add("evidence")
    return [d for d in ORDER if d in domains]


def doctrine_refs_for_component(comp: ComponentProfile) -> list[str]:
    return [DECISION_FILES[d] for d in domains_for_component(comp)]


def default_project_context() -> list[str]:
    return [
        ".cursor/doctrine/objectives.md",
        ".cursor/doctrine/invariants.md",
        ".cursor/doctrine/workload.md",
    ]
