---
name: system-orchestration
description: Design or review event-driven AI systems with explicit missions, bounded authority, state transitions, evidence and recovery. Use for system construction, not unattended activation.
---

# System orchestration construction kit

## Purpose and boundary

Build a system that owns a standing responsibility instead of depending on a continuing chat. The supervisor owns lifecycle and authority; models return bounded proposals. Use deterministic application logic wherever judgment is not required.

This skill and pack are design-time assistance. The hub CLI implements **offline simulation only**. Neither installation nor a slash command starts workers, schedules jobs, grants credentials, changes project policy, calls a model, or executes a real action. Simulation `VERIFIED` means the fixture's declared check outcomes satisfied its contract, not that a real system is correct.

## Progressive loading

Read only the relevant references:

- Mission, ownership, scope and approval questions: `reference/mission-and-authority.md`.
- Event lifecycle, duplicate delivery, bounds and restart: `reference/state-and-recovery.md`.
- Observation trust, model proposals, action receipts and check results: `reference/observation-and-evidence.md`.
- Live adapter design and deployment boundary: `reference/execution-boundaries.md`.
- Acceptance tests and independent review: `reference/verification-and-escalation.md`.

`contracts/README.md` explains the versioned machine-readable contracts and their CLI export. `templates/system-charter.md` and `templates/adapter-contract.md` are design scaffolds, not approved operating configuration. Examples are synthetic fixtures, not evidence about ll-cache or real machines. Source-backed mechanisms and project policies are distinguished in `SOURCES.md`.

## Design workflow

Read the named project facts without changing them. Identify its desired outcomes, observations and actors; challenge whether a model is necessary. Keep unknowns explicit. Produce four reviewed outputs: a system charter; transition/authority table; adapter contracts; and an evaluation plan.

Define what starts work, what counts as no action, what remains awaiting review, what can be retried, what must be reconciled, which actions are prohibited, and what ends the run. Specify checkable acceptance criteria and bounded cost/retry/deadline limits. A prose objective alone is insufficient.

Present drafts before writing new artifacts. Record a design decision with the existing deterministic design-log tool only when authorized. Never let the proposed runtime edit its own authority or automatically promote worker claims into project doctrine. Do not silently fill budget, owner, evidence, safety or deployment gaps with the example values.

## Review workflow

Trace a normal run and failure cases through executable boundaries. Demand an enforcement point and evidence for each guarantee. Distinguish simulation coverage, mechanism evidence, proposed policy, assumptions and untested live behavior. Explain the consequence and smallest repair for each supported finding. An acceptable review can find no material new issue.

## Integration with existing packs

Engineering-doctrine contributes verified knowledge, objectives and invariants; it does not grant action permission. Its setup/write gates remain unchanged. Fault-first remains a read-only investigation and does not acquire autonomous test execution, injection or repair. Language packs keep their current bundles and workflows. The ll-cache pilot remains disposable, one-component, human-led and no-code unless separately authorized.

## Offline checks

With the hub CLI installed using `python -m pip install -e '.[orchestration]'`, run `cursor-hub orchestration validate --kind scenario <fixture.json>` and `cursor-hub orchestration simulate <fixture.json>`. Omit `--journal` for in-memory operation. `replay --journal <existing.sqlite>` reconstructs committed simulation state without advancing it. Record exact commands, versions, outcomes and limitations; do not claim a live integration was tested.
