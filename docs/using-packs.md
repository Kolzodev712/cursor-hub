# Using the packs day to day

After you run `python tools/install.py all ../my-project` (or the Windows equivalent), your project has `.cursor/rules/`, `.cursor/commands/`, and `.cursor/agents/` full of files. Here's how that turns into "use the right behavior for the task."

---

## The three pieces

| Piece | What it does | How you "use" it |
|-------|----------------|------------------|
| **Rules** (`.mdc`) | Set guardrails and defaults (design log, question-first, Rust style, etc.). | **Automatic.** Cursor includes them in context. You don't pick them; they're always on (or apply when you have certain files open). |
| **Commands** (slash `/`) | Define a concrete workflow for one task (e.g. "do a design review", "fix a bug with TDR"). | **You choose.** Type `/` in chat and pick the command that matches what you're doing. Commands are namespaced: e.g. `/rust-design-review__design-review`. |
| **Agents** (`.md` in `agents/`) | Describe a **persona** (design critic, implementer, reviewer, test author). | **Indirect.** You get that behavior by running the **matching command** (or by saying "act as the design critic"). Commands are written so that running them *is* using that agent. |

So you don't "manage" rules and agents by hand. You **choose the right command** for the task; the command plus the rules give you the right behavior (and the right "agent" in practice).

---

## Task → command (what to run when)

Use **one command per task**. The command loads the workflow and, in effect, the right "agent" for that job.

| You want to… | Use this command | In practice |
|--------------|------------------|-------------|
| **Review a design / get critical questions** | `/rust-design-review__design-review` | Model follows the design-review steps and behaves like the design critic (challenge, alternatives, recommendation, verification). |
| **Force design-first (hard gate)** | `/rust-design-review__design-gate` | Refuses to propose a solution until you provide complete architecture; responds with BLOCKED + MISSING + questions; then outputs PROPOSED PLAN only. |
| **Start a new design log (ADR)** | `/rust-design-review__adr-new` | Creates a new log via the script and fills the template. |
| **Summarise a decision** | `/rust-design-review__decision-summary` | Summarises chosen option and why alternatives were rejected. |
| **Implement from an approved design log** | `/rust-implementation__implement-module` | Stepwise implementation, cites the log, runs verification; behaves like the rust-implementer. |
| **Force API-first implementation (hard gate)** | `/rust-implementation__impl-gate` | Refuses to write code until you provide types, signatures, error types, and wiring; then implements only function bodies. |
| **Refactor safely** | `/rust-implementation__refactor-safe` | 3–6 steps, tests after each step, no behavior change. |
| **Fix a bug (test-first)** | `/rust-testing__bugfix-tdr` | Failing test first, then fix, then fmt/clippy/test. |
| **Add tests only (no prod changes)** | `/rust-testing__add-tests-only` | Only tests/fixtures; justifies coverage. |
| **Force test-plan-first (hard gate)** | `/rust-testing__test-gate` | Refuses to write test code until you provide full test breakdown; then implements tests exactly as specified. |
| **Review a PR / diff** | `/rust-review__pr-review` | File-by-file, must-fix vs nice-to-have. |
| **Scan for risky patterns** | `/rust-review__risky-changes-scan` | Flags unsafe, unwrap, panics, new deps, API breaks. |

So: **pick the task, then run the matching slash command.** You don't have to "manage" the .mdc or agent files; the commands are the lever.

---

## Rules in the background

- **design-log** (shared): "Design first, log decisions, use the script for new logs, when to log" — applies to the whole chat when relevant.
- **senior-teacher**: On "how would you approach…?" type questions, first reply is questions only (unless you say "just do it" / "draft now").
- **rust-design-review**, **rust-core**, **rust-anti-footguns**, **rust-testing**, **rust-review**: Rust standards and checklists; some are always-on, some when you have `.rs` (or similar) in context.

You don't turn these on/off per task. They're part of the environment. If you want a *task-specific* behavior, use the **command** for that task.

---

## Agents = "who" for that command

Each command is written so that running it gets you the right "agent" behavior:

- `/rust-design-review__design-review`, `/rust-design-review__design-gate` → **design critic** (skeptical, challenges assumptions; design-gate adds a hard refusal until architecture is complete).
- `/rust-implementation__implement-module`, `/rust-implementation__impl-gate`, `/rust-implementation__refactor-safe` → **rust-implementer** (small diffs, verification loop; impl-gate adds refusal until types/signatures/wiring are provided).
- `/rust-testing__bugfix-tdr`, `/rust-testing__add-tests-only`, `/rust-testing__test-gate` → **test author** (reproducible tests, no coverage theater; test-gate adds refusal until full test breakdown is provided).
- `/rust-review__pr-review`, `/rust-review__risky-changes-scan` → **reviewer** (correctness, must-fix vs nice-to-have).

So: **use the command for the task; the agent is built into that command.** If Cursor later adds an explicit "choose agent" UI, the same agent files can back that; until then, commands are how you "use" the right agent.

---

## Simple workflow

1. **Design / approach:** Ask in chat ("how would you add X?"). Senior-teacher rule gives questions first; when you're ready, run `/rust-design-review__adr-new` to create a log or `/rust-design-review__design-review` for a one-off review.
2. **Implement:** Run `/rust-implementation__implement-module` and tell it which design log; it will implement stepwise and run verification.
3. **Bugfix:** Run `/rust-testing__bugfix-tdr` and describe the bug; it will add a failing test, fix, then verify.
4. **Review:** Run `/rust-review__pr-review` on the files or diff; use `/rust-review__risky-changes-scan` for a quick risk check.
5. **Tests only:** Run `/rust-testing__add-tests-only` and say what you want covered.

You're not "managing" rules or agents; you're **choosing the right command** for the job. The rules and agent personas support those commands.
