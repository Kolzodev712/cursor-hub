# Refactor — verify improvement (python-refactor WF Step 3)

**Goal:** Decide whether the outcome **actually improves** the situation versus Step 1’s criteria—not merely different.

**Use after:** `/python-refactor__wf-2-execute-refactor`.

## Steps

1. **Reload criteria:** From **Refactor assessment** vs **Refactor implementation**, list planned vs shipped.
2. **Before / after:** Qualitative API clarity/coupling; quantitative if committed (cold import time, test duration, LOC/cyclomatic, latency). Operational: semver/breakages, rollout/migration burden.
3. **Verdict:** **Improved**, **mixed** (list retained regressions), **not improved** / **premature**; prescribe iterate, rollback, or re-open wf-1.
4. **Alternatives residue:** Whether another wf-1 option would dominate now—and why.
5. **Record (mandatory):** Append **Refactor outcome review**. **Workflow stamp:** `[cursor-hub workflow] step=refactor-outcome-review`.
6. **Verify:** Run `python .cursor/tools/validate_workflow_design_log.py --step refactor-outcome-review` until it passes.

Avoid large new refactors here; start a new workstream or wf-1 if scope explodes.
