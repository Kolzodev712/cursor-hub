# Using the packs day to day

After you run `python tools/install.py all ../my-project` (or the Windows equivalent), your project has `.cursor/rules/`, `.cursor/commands/`, `.cursor/agents/`, `.cursor/design-log/`, and `.cursor/tools/`. Commands are used in one of two ways: **main workflow** (design, implement, test — use in any order or on their own; each pack has its own step numbers) or **standalone** (for a specific need).

---

## The three pieces

| Piece | What it does | How you "use" it |
|-------|----------------|------------------|
| **Rules** (`.mdc`) | Set guardrails and defaults (design log, question-first, Rust style, etc.). | **Automatic.** Cursor includes them in context. You don't pick them; they're always on (or apply when you have certain files open). |
| **Commands** (slash `/`) | Define a concrete workflow for one task (e.g. "do a design review", "create design log", "implement from log"). | **You choose.** Type `/` in chat and pick the command. Commands are namespaced: e.g. `/rust-design-review__wf-1-design-review`. |
| **Agents** (`.md` in `agents/`) | Describe a **persona** (design critic, implementer, reviewer, test author). | **Indirect.** You get that behavior by running the **matching command**. Commands are written so that running them *is* using that agent. |

So you don't "manage" rules and agents by hand. You **choose the right command** for the task; the command plus the rules give you the right behavior.

---

## Two ways to use commands

### 1. Main workflow (use in any order or on their own)

Each pack has its own step numbering. Use design review, implement, and/or add tests as needed — you are not forced to run all of them. **The design log is created or updated automatically** at the end of each command.

| Pack | Command | When to use it |
|------|---------|----------------|
| **rust-design-review** | `/rust-design-review__wf-1-design-review` | Get critical questions, alternatives, recommended option, risks, verification. Design log is created/updated automatically at the end. |
| **rust-implementation** | `/rust-implementation__wf-1-implement-module` | Implement from the design log; stepwise; verification loop; Implementation Results appended automatically. |
| **rust-testing** | `/rust-testing__wf-1-add-tests-only` | Add tests for new behavior. Test session recorded in the design log automatically. |

**Manual design log:** To create a new log without running a workflow step, use `/design-log__create`. To record a step manually, use `/design-log__record-step`.

The design log is the spine: each workflow command records into it automatically. You can run design, implement, or test on their own — no need to run all of them.

### 2. Standalone commands (specific needs)

Use when you have a **particular problem**, not the full design → implement → test flow.

**Gates (strict / dev-led)** — You provide all inputs; the model refuses to propose solutions or write code until you do. Use when you want maximum control.

| You want to… | Command |
|--------------|---------|
| Force design-first (you provide full architecture) | `/rust-design-review__gate-design` |
| Force API-first implementation (you provide types/signatures/wiring) | `/rust-implementation__gate-impl` |
| Force test-plan-first (you provide full test breakdown) | `/rust-testing__gate-test` |

**Other standalone**

| You want to… | Command |
|--------------|---------|
| Summarize a decision for a log/ADR | `/rust-design-review__standalone-decision-summary` |
| Refactor safely (no behavior change) | `/rust-implementation__standalone-refactor-safe` |
| Review a PR / diff | `/rust-review__standalone-pr-review` |
| Scan for risky patterns | `/rust-review__standalone-risky-changes-scan` |
| **Documentation** | |
| Architecture doc (general) | `/documentation__standalone-architecture-doc` |
| Feature doc (in-depth) | `/documentation__standalone-feature-doc` |
| Workflow doc (general) | `/documentation__standalone-workflow-doc` |
| Specific workflow doc (in-depth) | `/documentation__standalone-specific-workflow-doc` |
| Bug summary | `/documentation__standalone-bug-summary` |

So: **main workflow** = use design review, implement, and/or add tests in any order (each pack's step 1); **standalone** = pick the command that matches your immediate need (gates, refactor, review, etc.).

---

## Task → command (quick reference)

| You want to… | Use this command |
|--------------|------------------|
| **Main flow** | Design: `/rust-design-review__wf-1-design-review` → Implement: `/rust-implementation__wf-1-implement-module` → Test: `/rust-testing__wf-1-add-tests-only`. Use in any order or on their own. Design log updated automatically after each. Manual log: `/design-log__create`. |
| **Bugfix (separate)** | Small bug: `/rust-bugfix__standalone-fix-small-bug`. Non-trivial: wf-1-investigation → wf-2-proposed-solution → wf-3-resolution (`/rust-bugfix__wf-1-investigation`, etc.). |
| **Standalone — gate** | `/rust-design-review__gate-design`, `/rust-implementation__gate-impl`, `/rust-testing__gate-test` |
| **Standalone — other** | `/rust-design-review__standalone-decision-summary`, `/rust-implementation__standalone-refactor-safe`, `/rust-review__standalone-pr-review`, `/rust-review__standalone-risky-changes-scan`, `/documentation__standalone-*` (architecture, feature, workflow, specific workflow, bug summary) |

---

## Rules in the background

- **design-log** (shared): "Design first, log decisions, use `.cursor/tools/new_design_log.py` for new logs, when to log" — applies to the whole chat when relevant.
- **rust-bugfix**: When to use standalone fix vs 3-step workflow (only when that pack is installed).
- **senior-teacher**: On "how would you approach…?" type questions, first reply is questions only (unless you say "just do it" / "draft now").
- **rust-design-review**, **rust-core**, **rust-anti-footguns**, **rust-testing**, **rust-review**: Rust standards and checklists; some always-on, some when `.rs` (or similar) is in context.

You don't turn these on/off per task. They're part of the environment. Use the **command** for the task.

---

## Agents = "who" for that command

- **Structured:** wf-1-design-review → **design critic**; wf-1-implement-module → **rust-implementer**; wf-1-add-tests-only → **test author**. Design log recording is automatic (design-log pack). **Bugfix (separate flow):** standalone-fix-small-bug or wf-1/wf-2/wf-3 → **rust-bugfix**.
- **Standalone gates:** gate-design, gate-impl, gate-test → same agents with strict refusal until you provide inputs.
- **Standalone other:** standalone-refactor-safe → rust-implementer; standalone-pr-review, standalone-risky-changes-scan → **reviewer**; standalone-decision-summary → design critic; documentation commands → **documentation**.

Use the command for the task; the agent is built into that command.

---

## Simple workflow (main flow)

1. **Design:** Run `/rust-design-review__wf-1-design-review` and describe the problem; get questions, alternatives, recommendation. The design log is created or updated automatically at the end.
2. **Implement:** Run `/rust-implementation__wf-1-implement-module` and point to the design log; it implements stepwise and runs verification. Implementation Results are appended automatically.
3. **Test:** Run `/rust-testing__wf-1-add-tests-only` for coverage. Test session is recorded in the design log automatically.
4. **Bugfix (separate flow):** For a small bug use `/rust-bugfix__standalone-fix-small-bug`. For a non-trivial bug use the 3-step workflow: `/rust-bugfix__wf-1-investigation` → `/rust-bugfix__wf-2-proposed-solution` → `/rust-bugfix__wf-3-resolution` (each step records in the design log).
5. **Review (optional):** Run `/rust-review__standalone-pr-review` or `/rust-review__standalone-risky-changes-scan` on the changes.

To create a design log manually (without running a workflow step): `/design-log__create`. You can run design, implement, or test on their own — no need to run all of them.
