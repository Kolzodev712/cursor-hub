# System orchestration construction kit

**Status: v0.1.0, opt-in, offline simulation only.** This feature supplies design/review workflows and executable building blocks for event-driven AI systems. It does not supply or activate a live autonomous runtime.

## What is implemented

The `system-orchestration` pack installs two standalone commands, one manually relevant non-always-on rule, a reviewer role and a progressively loaded skill. The Python package adds closed JSON contracts, validation, a deterministic event reducer, bounded fixture execution, and optional transactional SQLite checkpoints/replay. Two synthetic examples cover repository analysis and maintenance diagnostics.

`schema`, `validate`, `simulate` and `replay` are executable CLI commands. No model, shell, repository, network or machine action is dispatched by the simulator. Even its `execute` event only records a synthetic action receipt. Fixture `VERIFIED` means declared fixture checks passed; it proves neither a real artifact's provenance nor the correctness of an actual model finding.

## Install the design pack

```bash
cursor-hub install system-orchestration /path/to/project
```

This pack is absent from `all` and every language bundle. It adds no hooks and does not change engineering-doctrine or fault-first. Existing installer behavior still installs the shared foundation and hub tools. It never starts a service or creates a runtime journal. Skill templates/examples remain hub-managed references, not approved project operating configuration.

In Cursor use `/system-orchestration__design` or `/system-orchestration__review` with a named system. They produce/review a charter, transition/authority table, adapter contracts and evaluation plan. They do not authorize live execution or implementation.

## Install and exercise the offline tooling

From the hub checkout:

```bash
python -m pip install -e '.[orchestration]'
python -m cursor_hub orchestration schema mission
python -m cursor_hub orchestration validate skills/system-orchestration/examples/repository-analysis.json
python -m cursor_hub orchestration simulate skills/system-orchestration/examples/repository-analysis.json
python -m cursor_hub orchestration simulate skills/system-orchestration/examples/maintenance-diagnostics.json
```

The optional dependency is `jsonschema>=4.18,<5`. Ordinary installation/doctrine commands do not require this dependency. Schema output is generated from the same definitions used by validation, avoiding drifting copies. Pack installation distributes reference files; it does not pip-install the Python CLI into a target. Keep the hub CLI installed for validation/simulation. `python -m cursor_hub.orchestration` is an equivalent standalone entrypoint.

Default simulation is in memory. For an explicitly chosen local journal path:

```bash
python -m cursor_hub orchestration simulate skills/system-orchestration/examples/repository-analysis.json --journal /tmp/cursor-hub-example.sqlite --steps 3
python -m cursor_hub orchestration replay --journal /tmp/cursor-hub-example.sqlite
python -m cursor_hub orchestration simulate skills/system-orchestration/examples/repository-analysis.json --journal /tmp/cursor-hub-example.sqlite
```

Use an operator-owned directory and a new filename. Existing non-journal files, direct symlinks and multiply linked files are rejected; these checks are not a filesystem sandbox against hostile concurrent directory changes. Replay opens the journal read-only and does not advance it. Resume accepts only the same full scenario fingerprint. After changing fixture inputs, use a new journal. A failed initial creation can leave an empty file; inspect/remove that explicitly or choose a new name. There is no implicit repair or migration.

Exit codes: **0** successful validation/simulation/replay (a partial checkpoint is not completion); **1** completed fixture states differ from `expected`; **2** invalid input, dependency, journal or I/O error; **3** structurally valid mission/scenario has unresolved mission facts. Simulation reports `complete` and `expectations_met`; do not interpret exit 0 alone as completed work. `simulation_ready` concerns the narrow input contract, not deployment authorization.

## Reference lifecycle

`ADMITTED -> INVESTIGATING -> PROPOSED -> AUTHORIZED -> EXECUTED -> VERIFIED`, with explicit approval waiting, bounded worker retry, no-action, blocked, rejected, failed and cancelled outcomes. Unknown receipts enter `OUTCOME_UNKNOWN`: no blind retry and no cancellation that forgets the outstanding operation. Reconciliation binds the original operation ID. Stale target or policy prevents applying/confirming an obsolete proposal.

The mission bounds scenario events/runs and per-run worker calls, tokens and duration. Time and usage are recorded fixture assertions; no real-time timer, real model spend or global service quota is enforced. A future live runtime needs these enforcement points outside worker control.

Evidence must bind run, snapshot, mission, proposal and operation, name an allowed producer/check, and satisfy all declared checks. Missing/unknown evidence cannot produce success. Producer/approver names and artifact digests are NOT authenticated or fetched by this offline simulator. A second model's agreement, a read-credit hook or a design-log stamp is not an execution verification result.

## Ownership and compatibility

No new doctrine fields, hooks or setup schema are introduced. Project doctrine remains an engineering input, not action authorization. Fault-first remains read-only and does not acquire test execution, fault injection or edits. The ll-cache pilot remains disposable, one-component, human-led and no-code. No findings are auto-promoted to doctrine or logs.

The pack reuses existing recursive skill installation instead of inventing unsupported `.cursor/` merge directories or overloading `pack.yml` with a workflow language. The root CLI now consults the installer pack index for single-argument optional pack names; the legacy interpretation is retained. Project-owned missions belong outside the hub-managed skill tree and must not be overwritten on updates.

## Live integration deliberately not implemented

No event watcher, provider adapter, credential store, sandbox, authenticated approval channel, production executor, real artifact verifier, scheduler lease, transactional outbox or distributed recovery guarantee is shipped. The source includes design contracts for building these per project. Installing the kit is never activation. A future live adapter requires a separate design/approval and integration tests for the exact execution surface.

Start with offline contracts and recorded scenarios. Evaluate a separately authorized read-only live pilot before adding any mutating action. Industrial machine control and safety interlocks stay outside the proposed AI authority.

## Verification

```bash
python tools/validate_packs.py
python tools/validate_doctrine_sources.py
python -m unittest discover -s tests -v
```

CI installs the optional extra and runs the suite on Python 3.10, 3.11 and 3.12. Without the extra, orchestration-dependent tests explicitly skip; a skipped suite is not full feature verification. Tests cover schema rejection, fixture bindings, lifecycle failures, budgets, replay/corruption and opt-in installation. Live integration remains untested.

Primary references and claim limits: [skill SOURCES.md](../skills/system-orchestration/SOURCES.md).
