# Refactor — verify improvement (js-ts-refactor WF Step 3)

**Goal:** Decide if the refactor **actually improved** the situation versus wf‑1’s criteria—with evidence—including bundle/tsc churn or API churn when relevant.

**Use after:** `/js-ts-refactor__wf-2-execute-refactor`.

## Steps

1. Reload **Refactor assessment** expectations vs **Refactor implementation** reality.
2. **Before / after:** Readability/coupling; bundle size/dist output if pledged; flake rate; runtime perf if pledged; semver/migrations.
3. **Verdict:** **Improved**, **mixed**, **not improved**; next moves (iterate, rollback, rethink alternative).
4. **Residual alternatives:** Whether another wf‑1 path now dominates.
5. **Record:** **Refactor outcome review** + `[cursor-hub workflow] step=refactor-outcome-review`.
6. **Verify:** `python .cursor/tools/validate_workflow_design_log.py --step refactor-outcome-review` until passes.

No large new refactors—spawn new wf‑1 if needed.
