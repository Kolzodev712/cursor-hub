# Systematic resolution (Bugfix WF Step 3)

**Use after:** Bugfix Step 2 — Proposed solution (`/python-bugfix__wf-2-proposed-solution`). Implement the fix and verify; keep the change minimal and aligned with the proposal.

## Steps

1. **Cite the proposal:** Reference the design log or the agreed solution and trade-offs. Implement only what was proposed; do not expand scope.
2. **Implement:** Make the code changes. Prefer: add or adjust a failing test first (TDR), then fix so the test passes. Keep the diff minimal.
3. **Verification:** Run format/lint (e.g. `black .`, `ruff check .`), type check if used, and tests (`pytest`). Fix any failures.
4. **Summarize:** Briefly state what was changed and how verification passed.
5. **Record in design log (mandatory):** Update the bugfix log with the final **Fix** (what shipped), any remaining **Caveats / follow-ups**, and the **Verification** outcome (tests run / checks). If no log exists, create one first: `python .cursor/tools/new_design_log.py --slug bugfix-<short-name> --kind bugfix`. Create logs only in `./.cursor/design-log/`. Do not ask — do it.
6. **Verify:** Run `python .cursor/tools/validate_workflow_design_log.py --step resolution` from the project root. If it fails, add the missing fix/verification content and re-run the validator. Do not consider the command complete until the validator passes.

Do not refactor unrelated code. If the fix reveals a larger design issue, note it in the Resolution section and suggest a separate design log or the main design-review workflow for follow-up.
