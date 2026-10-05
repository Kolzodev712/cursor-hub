"""Guided,resumable engineering-doctrine repository setup."""
from __future__ import annotations

import os
import re
from typing import Callable

from cursor_hub.doctrine.inspect import inspect_repository, scan_component_hints
from cursor_hub.doctrine.model import (
    NOT_APPLICABLE,
    UNKNOWN,
    ComponentProfile,
    SetupAnswers,
    doctrine_paths,
)
from cursor_hub.doctrine.render import (
    load_answers_from_project,
    render_architecture,
    render_components_json,
    render_invariants,
    render_objectives,
    render_workload,
)
from cursor_hub.doctrine.setup_io import SetupIO
from cursor_hub.doctrine.routing import domains_for_component
from cursor_hub.doctrine.validate import (
    ValidationResult,
    finalize_setup_status,
    validate_doctrine_setup,
    write_setup_metadata,
)

_PERSIST_SECTION: dict[str, str] = {
    "architecture": "repository",
    "objectives": "objectives",
    "invariants": "invariants",
    "workload": "workload",
    "components": "components",
}

OBJECTIVE_CHOICES = [
    "Correctness",
    "Determinism",
    "Tail latency",
    "Mean latency",
    "Throughput",
    "Memory usage",
    "Availability",
    "Durability",
    "Responsiveness",
    "Maintainability",
    "Security",
    "Other",
]

WORKLOAD_FIELDS = [
    ("Deployment CPU architecture", "e.g. x86_64, aarch64"),
    ("Production CPU family", "e.g. Intel Xeon, AMD EPYC, Apple M-series"),
    ("Operating system", "e.g. Linux"),
    ("Rust/toolchain version constraints", "e.g. rustc 1.78+, edition 2021"),
    ("Typical event/request rate", "e.g. 50000 events/s"),
    ("Peak event/request rate", "e.g. 250000 events/s"),
    ("Typical active cardinality", "e.g. 200 instruments"),
    ("Maximum expected cardinality", "e.g. 5000 instruments"),
    ("Read/write balance", "e.g. read-heavy"),
    ("Burst behavior", "e.g. periodic bursts at open"),
    ("Latency target", "e.g. p99 < 2 ms"),
    ("Tail-latency target", "e.g. p99.9 < 5 ms"),
    ("Memory constraint", "e.g. < 512 MiB RSS"),
    ("Threading/runtime model", "e.g. dedicated threads per core"),
    ("Known allocation constraints", "e.g. no heap alloc on hot path"),
    ("Deployment topology", "e.g. single host, k8s pod"),
]

YNQ_PROMPT = "[Y] Yes  [N] No  [U] Unknown  [A] Not applicable"

# (attribute, question, when to use N/A)
COMPONENT_INTERVIEW: tuple[tuple[str, str, str], ...] = (
    (
        "correctness_critical",
        "If this component produces wrong results, could that cause incorrect trades, "
        "bad user-visible outcomes, data corruption, or violation of an external contract?",
        "Use N/A only if wrong answers here cannot meaningfully harm users or downstream systems.",
    ),
    (
        "latency_sensitive",
        "For this component, does response time (delay before a result is ready) materially "
        "affect whether the system meets its goals?",
        "Use N/A if this component is not on a time-sensitive path (e.g. offline tooling).",
    ),
    (
        "throughput_sensitive",
        "Does this component need to sustain a high volume of events, requests, or records "
        "per second without falling behind?",
        "Use N/A if volume is trivial or unbounded delay is acceptable.",
    ),
    (
        "mutable_state",
        "While running, does this component keep mutable state that changes over time "
        "(counters, caches, order books, session tables)?",
        "Use N/A if stateless or read-only after load.",
    ),
    (
        "concurrent_access",
        "Can that mutable state be accessed concurrently by multiple threads, async tasks, "
        "or processes without you serializing everything through one caller?",
        "Use N/A if there is no mutable state or access is strictly single-threaded.",
    ),
    (
        "explicit_sync",
        "Does the code rely on explicit synchronization (mutexes, atomics, lock-free structures) "
        "to protect shared state?",
        "Use N/A if there is no shared mutable state.",
    ),
    (
        "alloc_sensitive",
        "On the busiest code paths, could heap allocation (Box, Vec growth, string allocation) "
        "materially affect latency or throughput?",
        "Use N/A if allocation volume on hot paths is negligible.",
    ),
    (
        "numeric_compute",
        "Does this component spend substantial CPU time on numeric work (math, aggregation, "
        "indicators, pricing transforms) as opposed to mostly moving bytes or waiting on I/O?",
        "Use N/A if numeric work is negligible.",
    ),
    (
        "external_data",
        "Does this component parse, validate, or serialize data from outside the process "
        "(network, files, IPC, external APIs)?",
        "Use N/A if it only uses in-memory structures built elsewhere.",
    ),
    (
        "representation_sensitive",
        "Does this component repeatedly process enough data that choosing between structures "
        "(arrays, maps, trees, struct layout, cache-friendly batches) could materially affect "
        "latency, throughput, or memory?",
        "Use N/A if data volume is tiny or structure choice cannot affect goals.",
    ),
    (
        "persistent_storage",
        "Does this component read or write durable storage (disk, database, WAL) on paths that "
        "matter for correctness or performance?",
        "Use N/A if storage is absent or irrelevant to engineering tradeoffs here.",
    ),
    (
        "specialized_runtime",
        "Does this component depend on a specific runtime or hardware context (embedded, GPU, "
        "kernel module, WASM sandbox, pinned CPU features)?",
        "Use N/A if it runs as ordinary user-space code on generic servers.",
    ),
)


def _norm_ynu(raw: str, *, allow_na: bool = True) -> str:
    r = raw.strip().lower()
    if r in ("y", "yes", "1"):
        return "yes"
    if r in ("n", "no", "2"):
        return "no"
    if r in ("u", "unknown"):
        return UNKNOWN
    if allow_na and r in ("a", "na", "n/a", "not applicable", "not_applicable"):
        return NOT_APPLICABLE
    return UNKNOWN


def _persist(project_root: str, answers: SetupAnswers) -> None:
    paths = doctrine_paths(project_root)
    os.makedirs(os.path.dirname(paths["architecture"]), exist_ok=True)
    with open(paths["architecture"], "w", encoding="utf-8") as f:
        f.write(render_architecture(answers))
    with open(paths["objectives"], "w", encoding="utf-8") as f:
        f.write(render_objectives(answers))
    with open(paths["invariants"], "w", encoding="utf-8") as f:
        f.write(render_invariants(answers))
    with open(paths["workload"], "w", encoding="utf-8") as f:
        f.write(render_workload(answers))
    with open(paths["components"], "w", encoding="utf-8") as f:
        f.write(render_components_json(answers))
    result = validate_doctrine_setup(project_root)
    write_setup_metadata(project_root, result)


def _section_menu(io: SetupIO) -> str:
    io.writeln("\nExisting doctrine configuration found.")
    io.writeln("Choose section:")
    io.writeln("[1] Repository responsibility")
    io.writeln("[2] Objectives")
    io.writeln("[3] Invariants")
    io.writeln("[4] Workload/platform facts")
    io.writeln("[5] Components")
    io.writeln("[6] Unknown values only")
    io.writeln("[7] Full review")
    io.writeln("[8] Exit")
    return io.readline("> ").strip()


def run_section_repository(
    project_root: str, answers: SetupAnswers, io: SetupIO, report
) -> bool:
    io.writeln("\n────────────────────────────────────")
    io.writeln("1/5 — Repository responsibility")
    io.writeln("────────────────────────────────────")
    io.writeln(
        "\nWhat does this repository do in the larger system?\n"
        "Describe externally meaningful responsibility, not modules or file layout.\n"
        "Do not enter implementation trivia (e.g. 'contains structs and services').\n"
        "Your answer is saved in `.cursor/doctrine/architecture.md` for agents to read."
    )
    if report.readme_excerpt:
        io.writeln(f'\nDetected description from README:\n"{report.readme_excerpt}"')
        io.writeln("[A] Accept  [E] Edit  [U] Unknown")
        choice = io.readline("> ").strip().lower()
        if choice in ("a", "accept", ""):
            answers.repository_responsibility = report.readme_excerpt
        elif choice in ("u", "unknown"):
            answers.repository_responsibility = UNKNOWN
        else:
            answers.repository_responsibility = io.readline("Responsibility:\n> ").strip()
    else:
        cur = answers.repository_responsibility
        if cur and cur != UNKNOWN:
            io.writeln(f"\nCurrent:\n{cur}")
            io.writeln("[K] Keep  [E] Edit  [U] Unknown")
            c = io.readline("> ").strip().lower()
            if c in ("u", "unknown"):
                answers.repository_responsibility = UNKNOWN
            elif c not in ("k", "keep", ""):
                answers.repository_responsibility = io.readline("Responsibility:\n> ").strip()
        else:
            io.writeln("\nEnter repository responsibility (or U for unknown):")
            text = io.readline("> ").strip()
            answers.repository_responsibility = UNKNOWN if text.lower() in ("u", "unknown") else text
    if not answers.repository_responsibility:
        answers.repository_responsibility = UNKNOWN
    _persist_partial(project_root, answers, ("architecture",))
    return True


def _persist_partial(project_root: str, answers: SetupAnswers, keys: tuple[str, ...]) -> None:
    paths = doctrine_paths(project_root)
    os.makedirs(os.path.dirname(paths["architecture"]), exist_ok=True)
    if "architecture" in keys:
        with open(paths["architecture"], "w", encoding="utf-8") as f:
            f.write(render_architecture(answers))
    if "objectives" in keys:
        with open(paths["objectives"], "w", encoding="utf-8") as f:
            f.write(render_objectives(answers))
    if "invariants" in keys:
        with open(paths["invariants"], "w", encoding="utf-8") as f:
            f.write(render_invariants(answers))
    if "workload" in keys:
        with open(paths["workload"], "w", encoding="utf-8") as f:
            f.write(render_workload(answers))
    if "components" in keys:
        with open(paths["components"], "w", encoding="utf-8") as f:
            f.write(render_components_json(answers))
    _write_progress_metadata(project_root, keys)


def _write_progress_metadata(project_root: str, completed_keys: tuple[str, ...]) -> None:
    result = validate_doctrine_setup(project_root)
    sections = dict(result.sections)
    for key in completed_keys:
        sec = _PERSIST_SECTION.get(key)
        if sec:
            sections[sec] = "complete"
    status = finalize_setup_status(sections, result.unknown_count, issues=result.issues or None)
    write_setup_metadata(
        project_root,
        ValidationResult(
            status=status,
            issues=result.issues,
            sections=sections,
            unknown_count=result.unknown_count,
        ),
    )


def run_section_objectives(project_root: str, answers: SetupAnswers, io: SetupIO) -> bool:
    io.writeln("\n────────────────────────────────────")
    io.writeln("2/5 — Engineering objectives")
    io.writeln("────────────────────────────────────")
    io.writeln(
        "Which properties materially determine engineering quality in this repository?\n"
        "Select all that apply. Saved to `.cursor/doctrine/objectives.md` for tradeoff decisions."
    )
    for i, name in enumerate(OBJECTIVE_CHOICES, 1):
        io.writeln(f"  [{i}] {name}")
    io.writeln(
        "\nEnter numbers separated by commas (e.g. 1,3,5).\n"
        "Enter U if you have not chosen objectives yet (stored as UNKNOWN)."
    )
    raw = io.readline("> ").strip()
    if raw.lower() in ("u", "unknown"):
        answers.objectives_selected = []
    else:
        picks: list[str] = []
        for part in re.split(r"[,\\s]+", raw):
            if not part.isdigit():
                continue
            idx = int(part) - 1
            if 0 <= idx < len(OBJECTIVE_CHOICES):
                label = OBJECTIVE_CHOICES[idx]
                if label == "Other":
                    io.writeln(
                        "\nName the additional engineering objective.\n"
                        "Use a short property, not an implementation technique.\n"
                        "Examples: startup time, energy consumption, reproducibility\n"
                        "Objective:"
                    )
                    custom = io.readline("> ").strip()
                    if custom:
                        picks.append(custom)
                else:
                    picks.append(label)
        answers.objectives_selected = picks
    if answers.objectives_selected:
        io.writeln(
            "\nWhen these objectives conflict, rank the selected ones (most important first).\n"
            "Use list numbers from above (e.g. 1,3,2) or type names.\n"
            "Enter U if priority order is unknown."
        )
        rank = io.readline("> ").strip()
        if rank.lower() in ("u", "unknown"):
            answers.objectives_priority = []
        else:
            order: list[str] = []
            for part in re.split(r"[,\\s]+", rank):
                if part.isdigit():
                    idx = int(part) - 1
                    if 0 <= idx < len(answers.objectives_selected):
                        order.append(answers.objectives_selected[idx])
                elif part in answers.objectives_selected:
                    order.append(part)
            answers.objectives_priority = order
    io.writeln(
        "\nDo these objectives and priorities apply the same way to the whole repository?\n"
        "[Y] Yes — repository-wide\n"
        "[N] No — important components differ (you will classify components later)\n"
        "[U] Unknown"
    )
    scope = io.readline("> ").strip().lower()
    if scope in ("y", "yes"):
        answers.objectives_per_component = "yes"
    elif scope in ("n", "no"):
        answers.objectives_per_component = "no"
    else:
        answers.objectives_per_component = UNKNOWN
    _persist_partial(project_root, answers, ("objectives",))
    return True


def run_section_invariants(project_root: str, answers: SetupAnswers, io: SetupIO) -> bool:
    io.writeln("\n────────────────────────────────────")
    io.writeln("3/5 — Invariants")
    io.writeln("────────────────────────────────────")
    io.writeln(
        "An invariant must stay true regardless of implementation.\n"
        "Breaking it means incorrect, unsafe, corrupt, or contract-violating behavior.\n"
        "Not invariants: style choices, HashMap vs BTreeMap, 'keep functions small'."
    )
    answers.invariants_unknown = False
    answers.invariants = []
    while True:
        io.writeln(
            "\nAdd one invariant per line.\n"
            "Enter U if no known invariants yet."
        )
        line = io.readline("> ").strip()
        if line.lower() in ("u", "unknown"):
            answers.invariants_unknown = True
            answers.invariants = []
            break
        if not line:
            break
        answers.invariants.append(line)
        io.writeln("[A] Add another  [D] Done")
        if io.readline("> ").strip().lower() in ("d", "done", ""):
            break
    _persist_partial(project_root, answers, ("invariants",))
    return True


def run_section_workload(project_root: str, answers: SetupAnswers, io: SetupIO) -> bool:
    io.writeln("\n────────────────────────────────────")
    io.writeln("4/5 — Workload and platform facts")
    io.writeln("────────────────────────────────────")
    io.writeln(
        "When you design or change code here, do speed, latency, throughput, or memory limits "
        "materially affect whether a change is acceptable?\n"
        "[1] Yes — for most of the repository\n"
        "[2] No — performance is not a primary concern\n"
        "[3] Only for some components (you will mark which ones later)\n"
        "[4] Unknown — not decided yet\n"
        "Saved to `.cursor/doctrine/workload.md`."
    )
    p = io.readline("> ").strip()
    if p == "1":
        answers.performance_importance = "yes"
    elif p == "2":
        answers.performance_importance = "no"
    elif p == "3":
        answers.performance_importance = "partial"
    else:
        answers.performance_importance = UNKNOWN

    answers.workload_fields = dict(answers.workload_fields)
    if answers.performance_importance.lower() in ("yes", "partial"):
        for label, hint in WORKLOAD_FIELDS:
            io.writeln(
                f"\n{label}\n"
                f"Enter a value with units where relevant. Example: {hint}\n"
                "[U] Unknown — matters but not known yet  [N] Not applicable — does not apply here"
            )
            val = io.readline("> ").strip()
            if val.lower() in ("u", "unknown"):
                answers.workload_fields[label] = UNKNOWN
            elif val.lower() in ("n", "na", "n/a", "not applicable"):
                answers.workload_fields[label] = NOT_APPLICABLE
            else:
                answers.workload_fields[label] = val or UNKNOWN
    else:
        answers.workload_fields = {
            "Detailed performance facts": NOT_APPLICABLE,
        }
    _persist_partial(project_root, answers, ("workload",))
    return True


def _interview_component(comp: ComponentProfile, io: SetupIO, root: str) -> None:
    io.writeln(
        f"\nComponent: {comp.id}\n"
        f"Paths: {', '.join(comp.patterns)}\n"
        "Short responsibility — what this component does in the system (one or two sentences):"
    )
    resp = io.readline("> ").strip()
    comp.responsibility = resp or UNKNOWN
    for attr, question, na_hint in COMPONENT_INTERVIEW:
        io.writeln(f"\n{question}\n{YNQ_PROMPT}\n({na_hint})")
        setattr(comp, attr, _norm_ynu(io.readline("> "), allow_na=True))

    if comp.patterns:
        hints = scan_component_hints(root, comp.patterns[0])
        if any(hints.values()):
            io.writeln("\nStatic scan suggestions (may be wrong):")
            for k, v in hints.items():
                if v:
                    io.writeln(f"  {k}: {v}")
            io.writeln("Apply concurrency/external-data hints from scan? [Y/N/U]")
            apply = io.readline("> ").strip().lower()
            if apply in ("y", "yes"):
                if hints.get("atomic") or hints.get("mutex"):
                    comp.concurrent_access = "yes"
                    comp.explicit_sync = "yes"
                if hints.get("serde") or hints.get("network"):
                    comp.external_data = "yes"


def run_section_components(
    project_root: str, answers: SetupAnswers, io: SetupIO, report
) -> bool:
    io.writeln("\n────────────────────────────────────")
    io.writeln("5/5 — Components")
    io.writeln("────────────────────────────────────")
    io.writeln(
        "Which parts of the repository deserve their own engineering classification?\n"
        "This controls which areas trigger doctrine read checks before edits — you are not "
        "choosing internal doctrine filenames."
    )
    candidates = list(report.candidate_components)
    selected: list[ComponentProfile] = []
    if candidates:
        for i, (cid, pat) in enumerate(candidates, 1):
            io.writeln(f"  [{i}] {pat}  ({cid})")
        io.writeln("Enter numbers to include (comma-separated), or S to skip all:")
        raw = io.readline("> ").strip().lower()
        if raw not in ("s", "skip"):
            for part in re.split(r"[,\\s]+", raw):
                if part.isdigit():
                    idx = int(part) - 1
                    if 0 <= idx < len(candidates):
                        cid, pat = candidates[idx]
                        selected.append(ComponentProfile(id=cid, patterns=[pat]))
    io.writeln("\nAdd custom component? [Y/N]")
    if io.readline("> ").strip().lower() in ("y", "yes"):
        io.writeln("Short label for this component (e.g. market-data):")
        cid = io.readline("> ").strip() or "custom"
        io.writeln("Path glob — files under this path belong to the component (e.g. crates/foo/**):")
        pat = io.readline("> ").strip()
        if pat:
            selected.append(ComponentProfile(id=cid, patterns=[pat]))
    for comp in selected:
        _interview_component(comp, io, project_root)
    answers.components = selected
    _persist_partial(project_root, answers, ("components",))
    return True


def _summary(project_root: str, answers: SetupAnswers, status: str) -> str:
    lines = [
        "════════════════════════════════════",
        "Engineering Doctrine Setup Summary",
        "════════════════════════════════════",
        "",
        f"Responsibility:\n{answers.repository_responsibility}",
        "",
        "Objectives:",
    ]
    if answers.objectives_priority:
        for i, o in enumerate(answers.objectives_priority, 1):
            lines.append(f"  {i}. {o}")
    else:
        lines.append(f"  {UNKNOWN}")
    lines.append(f"\nInvariants: {len(answers.invariants)} configured")
    lines.append(f"Components: {len(answers.components)}")
    for comp in answers.components:
        lines.append(f"\n  {comp.id}")
        lines.append(f"    patterns: {', '.join(comp.patterns)}")
        domains = domains_for_component(comp)
        if not domains:
            from cursor_hub.doctrine.routing import DECISION_FILES

            refs = doctrine_refs_for_component(comp)
            if not refs:
                import json

                comp_path = doctrine_paths(project_root)["components"]
                if os.path.isfile(comp_path):
                    try:
                        raw = json.load(open(comp_path, encoding="utf-8"))
                        for item in raw.get("components") or []:
                            if item.get("id") == comp.id:
                                refs = item.get("required_doctrine_refs") or []
                                break
                    except (OSError, json.JSONDecodeError):
                        pass
            domains = [
                k
                for k, v in DECISION_FILES.items()
                if v in refs
            ]
        if domains:
            lines.append(f"    derived decision topics: {', '.join(domains)}")
        else:
            lines.append("    derived decision topics: (none — minimal gate refs)")
    lines.append(f"\nSetup result:\n{status}")
    lines.append("\n[W] Write/update  [B] Back  [C] Cancel")
    return "\n".join(lines)


def run_review_unknowns(project_root: str, answers: SetupAnswers, io: SetupIO) -> int:
    paths = doctrine_paths(project_root)
    unknowns: list[tuple[str, str]] = []
    for label, path in (
        ("Repository responsibility", paths["architecture"]),
        ("Objectives priority", paths["objectives"]),
        ("Workload", paths["workload"]),
    ):
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        for line in text.splitlines():
            if ": UNKNOWN" in line or line.strip() == "UNKNOWN":
                unknowns.append((line.strip(), label))
    if not unknowns:
        io.writeln("No UNKNOWN fields found.")
        return 0
    io.writeln("Outstanding doctrine knowledge gaps:\n")
    for i, (line, _) in enumerate(unknowns, 1):
        io.writeln(f"{i}. {line}")
    io.writeln("\n[R] Resolve first  [K] Keep  [S] Skip/exit")
    choice = io.readline("> ").strip().lower()
    if choice.startswith("r"):
        io.writeln("Enter new value (or U to keep unknown):")
        new = io.readline("> ").strip()
        if new and new.lower() not in ("u", "unknown"):
            # Only handle workload field lines key: UNKNOWN
            if ":" in unknowns[0][0]:
                key = unknowns[0][0].split(":", 1)[0].strip()
                answers.workload_fields[key] = new
                _persist_partial(project_root, answers, ("workload",))
    return 0


SECTION_RUNNERS: dict[str, Callable[..., bool]] = {}


def _run_setup_body(
    project_root: str,
    io: SetupIO,
    *,
    review: bool,
    review_unknowns: bool,
) -> int:
    answers = load_answers_from_project(doctrine_paths(project_root))
    report = inspect_repository(project_root)

    if review_unknowns:
        return run_review_unknowns(project_root, answers, io)

    if review:
        while True:
            choice = _section_menu(io)
            if choice == "8":
                return 0
            if choice == "6":
                return run_review_unknowns(project_root, answers, io)
            if choice == "7":
                review = False
                break
            mapping = {
                "1": "repository",
                "2": "objectives",
                "3": "invariants",
                "4": "workload",
                "5": "components",
            }
            sec = mapping.get(choice)
            if sec == "repository":
                run_section_repository(project_root, answers, io, report)
            elif sec == "objectives":
                run_section_objectives(project_root, answers, io)
            elif sec == "invariants":
                run_section_invariants(project_root, answers, io)
            elif sec == "workload":
                run_section_workload(project_root, answers, io)
            elif sec == "components":
                run_section_components(project_root, answers, io, report)
            answers = load_answers_from_project(doctrine_paths(project_root))

    order = [
        ("repository", lambda: run_section_repository(project_root, answers, io, report)),
        ("objectives", lambda: run_section_objectives(project_root, answers, io)),
        ("invariants", lambda: run_section_invariants(project_root, answers, io)),
        ("workload", lambda: run_section_workload(project_root, answers, io)),
        ("components", lambda: run_section_components(project_root, answers, io, report)),
    ]
    result = validate_doctrine_setup(project_root)
    for name, fn in order:
        if result.sections.get(name) == "complete" and not review:
            continue
        if not fn():
            io.writeln("\nSetup cancelled. Resume with:\n  cursor-hub doctrine setup .")
            write_setup_metadata(project_root, validate_doctrine_setup(project_root))
            return 1
        answers = load_answers_from_project(doctrine_paths(project_root))

    result = validate_doctrine_setup(project_root)
    io.writeln(_summary(project_root, answers, result.status))
    final = io.readline("> ").strip().lower()
    if final in ("c", "cancel"):
        io.writeln("\nSetup cancelled. Partial progress saved.")
        write_setup_metadata(project_root, validate_doctrine_setup(project_root))
        return 1
    if final in ("b", "back"):
        return run_setup(project_root, io, review=True)

    _persist(project_root, answers)
    result = validate_doctrine_setup(project_root)
    write_setup_metadata(project_root, result)
    io.writeln(f"\nSetup finished: {result.status}")
    return 0 if result.ok_for_install else 1


def run_setup(
    project_root: str,
    io: SetupIO,
    *,
    review: bool = False,
    review_unknowns: bool = False,
) -> int:
    project_root = os.path.abspath(project_root)
    try:
        return _run_setup_body(
            project_root,
            io,
            review=review,
            review_unknowns=review_unknowns,
        )
    except KeyboardInterrupt:
        io.writeln(
            "\n\nSetup interrupted (Ctrl+C). Completed sections were saved.\n"
            "Resume with:\n  cursor-hub doctrine setup ."
        )
        write_setup_metadata(project_root, validate_doctrine_setup(project_root))
        return 130
