# Refactor — assess fit and alternatives (python-refactor WF Step 1)

**Goal:** Decide whether this package boundary, subsystem, or dependency **still earns its place** using **engineering best practices** and **idiomatic Python**, and whether **better alternatives** exist (different libs, layering, consolidating/splitting packages). **Analysis only** unless the user asks for a spike; defer large edits to Step 2.

**Follow with:** `/python-refactor__wf-2-execute-refactor` after agreement to refactor or replace.

## Steps

1. **Check existing logs:** Read `./.cursor/design-log/`; extend one workstream log when it already covers this refactor.
2. **Scope:** Package, module cluster, abstraction, or pinned dependency chain. State the problem it solves today.
3. **Systems / tech assessment:** Lifecycle, coupling, observability, security boundaries (unsafe deserialization, subprocess/shell boundaries), rollout and pinning strategy, CI cost. Note gaps vs norms for apps vs libraries.
4. **Python idioms and API quality:** Typing discipline, asyncio vs threading, packaging/import graph, duplication, settings patterns, structured errors/logging, frameworks vs seams you own, dependency weight and pinning policy.
5. **Usefulness verdict:** **Keep with minor refactor**, **reshape internally**, **replace dependency/pattern**, **split/merge/remove package**, **needs spike** (time-box proof).
6. **Alternatives (concrete):** List 1–3 with **pros/cons**, **estimated effort**, **risks**, and **when each wins**. Prefer specific libs/patterns evidenced in the repo.
7. **Recommendation:** Preferred path for Step 2; **acceptance criteria** for success; **signals** that would abort the direction.
8. **Record in design log (mandatory):** Append **Refactor assessment** with verdict, alternatives, recommendation, and verification plan (before/after measurements). Create log via `python .cursor/tools/new_design_log.py --slug <short-name>` if needed. **Workflow stamp:** Append exactly one standalone line `[cursor-hub workflow] step=refactor-assessment`.
9. **Verify:** Run `python .cursor/tools/validate_workflow_design_log.py --step refactor-assessment` from the project root until it passes.

Do **not** start a broad implementation here unless the user explicitly requests a bounded spike to inform the assessment.
