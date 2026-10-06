"""Setup staging, approval lifecycle, and atomic publication (schema v2)."""
from __future__ import annotations

import json
import os
import uuid
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any

from cursor_hub.doctrine.model import (
    DOCTRINE_SETUP_SCHEMA_VERSION,
    ComponentProfile,
    SetupAnswers,
    doctrine_paths,
)
from cursor_hub.doctrine.markdown_merge import merge_managed_markdown
from cursor_hub.doctrine.render import (
    MARKER_INVARIANTS,
    MARKER_OBJECTIVES,
    MARKER_REPO,
    MARKER_WORKLOAD,
    render_architecture,
    render_components_json,
    render_invariants,
    render_objectives,
    render_workload,
)

STAGING_REL = ".cursor/doctrine/.setup-staging.json"
JOURNAL_REL = ".cursor/doctrine/.setup-publication.journal.json"


def _trait_dict(comp: ComponentProfile) -> dict[str, str]:
    return {
        "correctness_critical": comp.correctness_critical,
        "latency_sensitive": comp.latency_sensitive,
        "throughput_sensitive": comp.throughput_sensitive,
        "mutable_state": comp.mutable_state,
        "concurrent_access": comp.concurrent_access,
        "explicit_sync": comp.explicit_sync,
        "atomics_usage": comp.atomics_usage,
        "alloc_sensitive": comp.alloc_sensitive,
        "numeric_compute": comp.numeric_compute,
        "external_data": comp.external_data,
        "persistent_storage": comp.persistent_storage,
        "specialized_runtime": comp.specialized_runtime,
        "representation_sensitive": comp.representation_sensitive,
    }


def answers_to_staging_dict(answers: SetupAnswers) -> dict[str, Any]:
    return {
        "repository_responsibility": answers.repository_responsibility,
        "objectives_selected": list(answers.objectives_selected),
        "objectives_priority": list(answers.objectives_priority),
        "objectives_per_component": answers.objectives_per_component,
        "invariants": list(answers.invariants),
        "invariants_unknown": answers.invariants_unknown,
        "performance_importance": answers.performance_importance,
        "workload_fields": dict(answers.workload_fields),
        "components": [
            {
                "id": c.id,
                "patterns": list(c.patterns),
                "responsibility": c.responsibility,
                "traits": _trait_dict(c),
                "extra_required_project_files": list(c.extra_required_project_files),
                "extra_required_doctrine_refs": list(c.extra_required_doctrine_refs),
            }
            for c in answers.components
        ],
    }


def answers_from_staging_dict(raw: dict[str, Any]) -> SetupAnswers:
    ans = SetupAnswers()
    ans.repository_responsibility = str(raw.get("repository_responsibility") or "")
    ans.objectives_selected = list(raw.get("objectives_selected") or [])
    ans.objectives_priority = list(raw.get("objectives_priority") or [])
    ans.objectives_per_component = str(raw.get("objectives_per_component") or "UNKNOWN")
    ans.invariants = list(raw.get("invariants") or [])
    ans.invariants_unknown = bool(raw.get("invariants_unknown"))
    ans.performance_importance = str(raw.get("performance_importance") or "UNKNOWN")
    ans.workload_fields = dict(raw.get("workload_fields") or {})
    comps: list[ComponentProfile] = []
    for item in raw.get("components") or []:
        traits = item.get("traits") or {}
        comps.append(
            ComponentProfile(
                id=str(item.get("id", "component")),
                patterns=[str(p) for p in item.get("patterns") or []],
                responsibility=str(item.get("responsibility") or ""),
                extra_required_project_files=[
                    str(x) for x in item.get("extra_required_project_files") or []
                ],
                extra_required_doctrine_refs=[
                    str(x) for x in item.get("extra_required_doctrine_refs") or []
                ],
                correctness_critical=str(traits.get("correctness_critical", "UNKNOWN")),
                latency_sensitive=str(traits.get("latency_sensitive", "UNKNOWN")),
                throughput_sensitive=str(traits.get("throughput_sensitive", "UNKNOWN")),
                mutable_state=str(traits.get("mutable_state", "UNKNOWN")),
                concurrent_access=str(traits.get("concurrent_access", "UNKNOWN")),
                explicit_sync=str(traits.get("explicit_sync", "UNKNOWN")),
                atomics_usage=str(traits.get("atomics_usage", traits.get("explicit_sync", "UNKNOWN"))),
                alloc_sensitive=str(traits.get("alloc_sensitive", "UNKNOWN")),
                numeric_compute=str(traits.get("numeric_compute", "UNKNOWN")),
                external_data=str(traits.get("external_data", "UNKNOWN")),
                persistent_storage=str(traits.get("persistent_storage", "UNKNOWN")),
                specialized_runtime=str(traits.get("specialized_runtime", "UNKNOWN")),
                representation_sensitive=str(traits.get("representation_sensitive", "UNKNOWN")),
            )
        )
    ans.components = comps
    return ans


def write_staging(project_root: str, answers: SetupAnswers) -> None:
    path = os.path.join(project_root, STAGING_REL)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    payload = {
        "schema_version": DOCTRINE_SETUP_SCHEMA_VERSION,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "answers": answers_to_staging_dict(answers),
    }
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")
    os.replace(tmp, path)


def load_staging(project_root: str) -> SetupAnswers | None:
    path = os.path.join(project_root, STAGING_REL)
    if not os.path.isfile(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(raw, dict):
        return None
    ans = raw.get("answers")
    if not isinstance(ans, dict):
        return None
    return answers_from_staging_dict(ans)


def is_approved(meta: dict[str, Any]) -> bool:
    return bool(meta.get("approved_at")) and not meta.get("awaiting_final_approval")


def mark_awaiting_final_approval(meta: dict[str, Any]) -> None:
    meta["awaiting_final_approval"] = True
    meta["approved_at"] = None


def mark_approved(meta: dict[str, Any]) -> None:
    meta["awaiting_final_approval"] = False
    meta["approved_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    meta["approval_revision"] = int(meta.get("approval_revision") or 0) + 1


def publish_answers(project_root: str, answers: SetupAnswers) -> tuple[bool, str | None]:
    """Write canonical doctrine files atomically; return (ok, error)."""
    paths = doctrine_paths(project_root)
    os.makedirs(os.path.dirname(paths["architecture"]), exist_ok=True)
    pub_id = str(uuid.uuid4())
    journal_path = os.path.join(project_root, JOURNAL_REL)
    journal: dict[str, Any] = {"publications": []}
    if os.path.isfile(journal_path):
        try:
            with open(journal_path, encoding="utf-8") as f:
                journal = json.load(f)
        except (OSError, json.JSONDecodeError):
            journal = {"publications": []}
    pending = {
        "id": pub_id,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "files": [],
    }
    def _merge(path: str, new_text: str, *, header: str, marker: str) -> str:
        existing: str | None = None
        if os.path.isfile(path):
            try:
                with open(path, encoding="utf-8") as f:
                    existing = f.read()
            except OSError:
                existing = None
        return merge_managed_markdown(existing, new_text, section_header=header, marker=marker)

    files_to_write = {
        paths["architecture"]: _merge(
            paths["architecture"],
            render_architecture(answers),
            header="# Repository responsibility",
            marker=MARKER_REPO,
        ),
        paths["objectives"]: _merge(
            paths["objectives"],
            render_objectives(answers),
            header="# Engineering objectives",
            marker=MARKER_OBJECTIVES,
        ),
        paths["invariants"]: _merge(
            paths["invariants"],
            render_invariants(answers),
            header="# Invariants",
            marker=MARKER_INVARIANTS,
        ),
        paths["workload"]: _merge(
            paths["workload"],
            render_workload(answers),
            header="# Workload and platform facts",
            marker=MARKER_WORKLOAD,
        ),
        paths["components"]: render_components_json(answers),
    }
    temps: list[tuple[str, str]] = []
    try:
        for final, content in files_to_write.items():
            tmp = final + f".{pub_id}.tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(content)
            temps.append((tmp, final))
            pending["files"].append(final)
        for tmp, final in temps:
            os.replace(tmp, final)
        pending["completed_at"] = datetime.now(timezone.utc).isoformat()
        journal.setdefault("publications", []).append(pending)
        with open(journal_path + ".tmp", "w", encoding="utf-8") as f:
            json.dump(journal, f, indent=2)
            f.write("\n")
        os.replace(journal_path + ".tmp", journal_path)
        return True, None
    except OSError as e:
        for tmp, _ in temps:
            try:
                os.remove(tmp)
            except OSError:
                pass
        pending["error"] = str(e)
        journal.setdefault("publications", []).append(pending)
        try:
            with open(journal_path, "w", encoding="utf-8") as f:
                json.dump(journal, f, indent=2)
        except OSError:
            pass
        return False, str(e)
