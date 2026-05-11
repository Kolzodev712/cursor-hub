# Proposed solution and design trade-offs (Bugfix WF Step 2)

**Use after:** Bugfix Step 1 — Investigation (`/rust-bugfix__wf-1-investigation`). Propose how to fix the bug and document trade-offs before implementing.

**Follow with:** Bugfix Step 3 — Resolution (`/rust-bugfix__wf-3-resolution`).

## Steps

1. **Context:** Briefly reference the investigation (evidence, root cause, scope). If a design log exists for this bugfix, cite it.
2. **Proposed solution:** Describe the fix: what will change, where, and why it addresses the root cause. Be specific (files, types, behavior).
3. **Alternatives:** Note 0–2 alternative approaches and why they were not chosen (e.g. narrower fix, broader refactor).
4. **Trade-offs:** Call out any trade-offs: performance, complexity, backward compatibility, risk of regressions.
5. **Verification plan:** How we will verify the fix (tests to add or run, manual checks, invariants).
6. **Record in design log (mandatory):** Update the bugfix log with the proposed **Fix**, **Caveats / follow-ups** (trade-offs), and **Verification** plan. If no log exists, create one first: `python .cursor/tools/new_design_log.py --slug bugfix-<short-name> --kind bugfix`. Create logs only in `./.cursor/design-log/`. Do not ask — do it. **Workflow stamp:** After recording, append exactly one standalone line `[cursor-hub workflow] step=proposed-solution` (required so the validator accepts slim logs; legacy logs with old section headings only still pass without it).
7. **Verify:** Run `python .cursor/tools/validate_workflow_design_log.py --step proposed-solution` from the project root. If it fails, add the missing fix/caveats/verification content and/or the workflow stamp line and re-run the validator. Do not consider the command complete until the validator passes.

Do not implement the fix in this command; that is Step 3.
