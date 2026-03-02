# Using the packs day to day

After you run `python tools/install.py all ..\my-project`, your project has `.cursor/rules/`, `.cursor/commands/`, and `.cursor/agents/` full of files. Here’s how that turns into “use the right behavior for the task.”

---

## The three pieces

| Piece | What it does | How you “use” it |
|-------|----------------|-------------------|
| **Rules** (`.mdc`) | Set guardrails and defaults (design log, question-first, Rust style, etc.). | **Automatic.** Cursor includes them in context. You don’t pick them; they’re always on (or apply when you have certain files open). |
| **Commands** (slash `/`) | Define a concrete workflow for one task (e.g. “do a design review”, “fix a bug with TDR”). | **You choose.** Type `/` in chat and pick the command that matches what you’re doing. |
| **Agents** (`.md` in `agents/`) | Describe a **persona** (design critic, implementer, reviewer, test author). | **Indirect.** You get that behavior by running the **matching command** (or by saying “act as the design critic”). Commands are written so that running them *is* using that agent. |

So you don’t “manage” rules and agents by hand. You **choose the right command** for the task; the command plus the rules give you the right behavior (and the right “agent” in practice).

---

## Task → command (what to run when)

Use **one command per task**. The command loads the workflow and, in effect, the right “agent” for that job.

| You want to… | Use this command | In practice |
|--------------|------------------|-------------|
| **Review a design / get critical questions** | `/design-review` | Model follows the design-review steps and behaves like the design critic (challenge, alternatives, recommendation, verification). |
| **Start a new design log (ADR)** | `/adr-new` | Creates a new log via the script and fills the template. |
| **Summarise a decision** | `/decision-summary` | Summarises chosen option and why alternatives were rejected. |
| **Implement from an approved design log** | `/implement-module` | Stepwise implementation, cites the log, runs verification; behaves like the rust-implementer. |
| **Refactor safely** | `/refactor-safe` | 3–6 steps, tests after each step, no behavior change. |
| **Fix a bug (test-first)** | `/bugfix-tdr` | Failing test first, then fix, then fmt/clippy/test. |
| **Add tests only (no prod changes)** | `/add-tests-only` | Only tests/fixtures; justifies coverage. |
| **Review a PR / diff** | `/pr-review` | File-by-file, must-fix vs nice-to-have. |
| **Scan for risky patterns** | `/risky-changes-scan` | Flags unsafe, unwrap, panics, new deps, API breaks. |

So: **pick the task, then run the matching slash command.** You don’t have to “manage” the .mdc or agent files; the commands are the lever.

---

## Rules in the background

- **design-log** (shared): “Design first, log decisions, use the script for new logs, when to log” — applies to the whole chat when relevant.
- **senior-teacher**: On “how would you approach…?” type questions, first reply is questions only (unless you say “just do it” / “draft now”).
- **rust-design-review**, **rust-core**, **rust-anti-footguns**, **rust-testing**, **rust-review**: Rust standards and checklists; some are always-on, some when you have `.rs` (or similar) in context.

You don’t turn these on/off per task. They’re part of the environment. If you want a *task-specific* behavior, use the **command** for that task.

---

## Agents = “who” for that command

Each command is written so that running it gets you the right “agent” behavior:

- `/design-review` → **design critic** (skeptical, challenges assumptions).
- `/implement-module`, `/refactor-safe` → **rust-implementer** (small diffs, verification loop).
- `/bugfix-tdr`, `/add-tests-only` → **test author** (reproducible tests, no coverage theater).
- `/pr-review`, `/risky-changes-scan` → **reviewer** (correctness, must-fix vs nice-to-have).

So: **use the command for the task; the agent is built into that command.** If Cursor later adds an explicit “choose agent” UI, the same agent files can back that; until then, commands are how you “use” the right agent.

---

## Simple workflow

1. **Design / approach:** Ask in chat (“how would you add X?”). Senior-teacher rule gives questions first; when you’re ready, run `/adr-new` to create a log or `/design-review` for a one-off review.
2. **Implement:** Run `/implement-module` and tell it which design log; it will implement stepwise and run verification.
3. **Bugfix:** Run `/bugfix-tdr` and describe the bug; it will add a failing test, fix, then verify.
4. **Review:** Run `/pr-review` on the files or diff; use `/risky-changes-scan` for a quick risk check.
5. **Tests only:** Run `/add-tests-only` and say what you want covered.

You’re not “managing” rules or agents; you’re **choosing the right command** for the job. The rules and agent personas support those commands.
