# Catalog of packs

Packs live under `packs/cursor/`. Each has a `pack.yml` and optional `.cursor/rules/`, `.cursor/commands/`, `.cursor/agents/`. Command filenames use the `pack-name__command-name` convention so installing multiple packs does not collide.

There are **two ways** to use commands:

1. **Main workflow** — Use design review, implement, and/or add tests in any order or on their own. Each pack numbers its own workflow steps (e.g. rust-design-review has wf-1, rust-implementation has wf-1, rust-testing has wf-1). The **design log is created or updated automatically** at the end of each workflow command. To create a log manually, use `/design-log__create`.
2. **Standalone commands** — Use when you have a specific need (strict gates, refactor, PR review, decision summary); not part of a linear flow.

---

## _shared (foundation)

**Purpose:** Design-log methodology: design first, log decisions, append results. Always included when installing any other pack.

**Contents:**

- **Rules:** `design-log.mdc` — when to log, log structure (Background → Problem → Q/A → Design → Plan → Examples → Trade-offs → Verification → Implementation Results), deterministic creation via `.cursor/tools/new_design_log.py --slug <name>`; logs live in `.cursor/design-log/`. `present-before-writing.mdc` — for new rules, commands, or design-log sections beyond the template: present full draft and wait for explicit approval before writing files (applies when working on the hub or generating hub artifacts).

**No commands or agents.** Other packs add those.

---

## Main workflow (use in any order or on their own)

Each pack has its own workflow step numbering. Use design review, implement, and/or add tests as needed — you are not forced to run all of them. **The design log is created or updated automatically** at the end of each command.

| Pack | Command | Description |
|------|---------|-------------|
| **rust-design-review** | `/rust-design-review__wf-1-design-review` | Strict design review: critical questions, alternatives, recommended option, risks, verification. Design log created or updated automatically. |
| **rust-implementation** | `/rust-implementation__wf-1-implement-module` | Implement from the design log; cite log; stepwise phases; verification loop; Implementation Results appended automatically. |
| **rust-testing** | `/rust-testing__wf-1-add-tests-only` | Add or extend tests only; no prod code changes; justify coverage. Test session recorded in the design log automatically. |

**Design log (manual):** To create a new log without running a workflow step, use `/design-log__create`. To record a step manually, use `/design-log__record-step`.

---

## Bugfix workflow (separate)

**Not connected to the main design → implement → test flow.** Use for non-trivial bugs that need investigation and a proposed solution before coding. Each step records in its own design log (e.g. `bugfix-<name>.md`).

| Step | Command | Description |
|------|---------|-------------|
| **Standalone** | `/rust-bugfix__standalone-fix-small-bug` | Point the agent to identify and fix a small bug; minimal workflow, design log optional. |
| **1. Investigation** | `/rust-bugfix__wf-1-investigation` | Bug investigation and evidence collection. Design log: Investigation section (reproduction, evidence, scope, hypotheses). |
| **2. Proposed solution** | `/rust-bugfix__wf-2-proposed-solution` | Proposed solution and design trade-offs. Design log: Proposed solution, Trade-offs, Verification plan. |
| **3. Resolution** | `/rust-bugfix__wf-3-resolution` | Systematic resolution: implement fix, verification. Design log: Resolution section. |

---

## Standalone commands

Use when you have a specific need. **Not** intended to be followed in the structured order above.

### Gates (strict / dev-led)

You drive the inputs; the model refuses to propose solutions or write code until you provide the required shape. Use when you want maximum control.

| Command | Description |
|--------|-------------|
| `/rust-design-review__gate-design` | Refuse to propose a solution until you provide complete architecture (modules, data flow, alternatives); BLOCKED + MISSING + questions → then PROPOSED PLAN only. |
| `/rust-implementation__gate-impl` | Refuse to write code until you provide types, error types, function signatures, and wiring; then implement only function bodies. |
| `/rust-testing__gate-test` | Refuse to write test code until you provide full test breakdown; then implement tests exactly as specified. |

### Design / decisions

| Command | Description |
|--------|-------------|
| `/rust-design-review__standalone-decision-summary` | Summarize final decision and why alternatives were rejected (paste into log or ADR). |

### Refactor / review

| Command | Description |
|--------|-------------|
| `/rust-implementation__standalone-refactor-safe` | Plan 3–6 steps; limit files per step; run tests after each step; no behavior change. |
| `/rust-review__standalone-pr-review` | File-by-file review with must-fix vs nice-to-have. |
| `/rust-review__standalone-risky-changes-scan` | Flag unsafe, unwrap, panics, new deps, public API breaks. |

### Documentation

| Command | Description |
|--------|-------------|
| `/documentation__standalone-architecture-doc` | General-level architecture doc: components, boundaries, data flow, tech stack. |
| `/documentation__standalone-feature-doc` | In-depth feature-specific doc: behavior, APIs, examples, edge cases. |
| `/documentation__standalone-workflow-doc` | General-level workflow doc: how work gets done, phases, tooling, conventions. |
| `/documentation__standalone-specific-workflow-doc` | In-depth specific workflow doc: step-by-step guide for one workflow, with examples. |
| `/documentation__standalone-bug-summary` | Bug summary: what was wrong, root cause, fix, verification (for tickets or handoffs). |

### Security

| Command | Description |
|--------|-------------|
| `/security__standalone-audit` | One-pass security review: vulnerabilities, deps, secrets, auth, crypto, misconfiguration, CI/CD; report with severity and recommendations. |

---

## Pack reference (by pack)

### design-log

**Purpose:** Create and update design logs. Main workflow (wf-1 in each of design-review, implementation, testing) and bugfix workflow (wf-1, wf-2, wf-3) record automatically at the end of each step; this pack provides the manual commands and the recording rule.

**Rules:** `design-log-record.mdc` — how to create/append after each workflow step.

**Commands:** design-log__create (create new log with template), design-log__record-step (manually record a step).

**Workflow verification:** Workflow commands (not standalone) run `python .cursor/tools/validate_workflow_design_log.py --step <step>` after recording; the script checks that the expected section is present in the design log. If it fails, the model is instructed to add the missing content and re-run until it passes.

**Agents:** `design-log.md`.

### rust-design-review

**Purpose:** Question-first design, design review bar, design log creation, decision summaries.

**Rules:** `senior-teacher.mdc`, `rust-design-review.mdc`.

**Commands (structured):** wf-1-design-review (step 1).  
**Commands (standalone):** gate-design, standalone-decision-summary.

**Agents:** `design-critic.md`.

### rust-implementation

**Purpose:** Small diffs, verification loop, Rust anti-footguns.

**Rules:** `rust-core.mdc`, `rust-anti-footguns.mdc`.

**Commands (structured):** wf-1-implement-module (step 1).  
**Commands (standalone):** gate-impl, standalone-refactor-safe.

**Agents:** `rust-implementer.md`.

### rust-testing

**Purpose:** TDR, deterministic tests, fixtures.

**Rules:** `rust-testing.mdc`.

**Commands (structured):** wf-1-add-tests-only (step 1).  
**Commands (standalone):** gate-test.

**Agents:** `test-author.md`.

### rust-review

**Purpose:** PR review, risky-changes scan.

**Rules:** `rust-review.mdc`.

**Commands (standalone):** standalone-pr-review, standalone-risky-changes-scan.

**Agents:** `reviewer.md`.

### rust-bugfix

**Purpose:** Bugfix: standalone fix for small bugs, or 3-step workflow (investigation → proposed solution → resolution). Separate from the main design/implement/test flow; uses its own design logs.

**Rules:** `rust-bugfix.mdc` — when to use standalone vs workflow.

**Commands (standalone):** standalone-fix-small-bug.  
**Commands (workflow):** wf-1-investigation, wf-2-proposed-solution, wf-3-resolution.

**Agents:** `rust-bugfix.md`.

### documentation

**Purpose:** Produce documentation on demand — architecture, feature, workflow, and bug summaries. All commands are standalone; no workflow or design log required.

**Commands (standalone):** standalone-architecture-doc, standalone-feature-doc, standalone-workflow-doc, standalone-specific-workflow-doc, standalone-bug-summary.

**Agents:** `documentation.md`.

### security

**Purpose:** Security review: code vulnerabilities, dependency audit, secrets, auth, crypto, misconfiguration, CI/CD. Severity levels and report format.

**Commands (standalone):** security__standalone-audit.

**Agents:** `security.md`.

---

## Installing

From the cursor-hub repo root:

```bash
python tools/install.py <pack> [pack ...] <target_dir>
# or, to use a language profile:
python tools/install.py --lang rust all <target_dir>
```

Example: `python tools/install.py --lang rust all /path/to/your/project`
