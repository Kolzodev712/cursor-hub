# Refactor — execute (python-refactor WF Step 2)

**Goal:** Carry out the **refactor or replacement** aligned with **Refactor assessment** from `/python-refactor__wf-1-assess-fit-and-alternatives` (same design-log workstream). Phased edits plus the usual Python verification loop.

**Use after:** Assessment agreed (or retrospective **Refactor assessment** if genuinely missing).

## Steps

1. **Bind to the log:** Restate recommendation and acceptance criteria from **Refactor assessment** in one paragraph. If missing, append a minimal **Refactor assessment** before implementing.
2. **Plan phases:** Break into 3–6 phases; each phase should keep format/lint/tests passing when practical.
3. **Per phase:**
   - Scope edits to the phase only.
   - Run verification: format (e.g. `black .`, `ruff format .`), lint (e.g. `ruff check .`), type check if used (e.g. `mypy .`), tests (`pytest`). Use project equivalents (Makefile, Poetry, Hatch, uv, tox) when present. Fix failures before continuing.
4. **Deviations:** Document **why** when diverging from the assessment.
5. **Record (mandatory):** Append **Refactor implementation** — what changed, deviations, verification (commands + outcome). **Workflow stamp:** `[cursor-hub workflow] step=refactor-implement`.
6. **Verify:** Run `python .cursor/tools/validate_workflow_design_log.py --step refactor-implement` until it passes.

If “replace with X” hits a blocker, stop, note in the log, return to wf-1.
