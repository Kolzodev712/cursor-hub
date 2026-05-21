# Refactor — verify improvement (rust-refactor WF Step 3)

**Goal:** **Objectively** decide whether the new solution **is an improvement** against the acceptance criteria set in Step 1, not merely “different.” Address residual risks and whether **better alternatives** still exist.

**Use after:** `/rust-refactor__wf-2-execute-refactor`.

## Steps

1. **Reload criteria:** From **Refactor assessment**, list the verdict, acceptance criteria, and risks. From **Refactor implementation**, note what actually shipped vs planned.
2. **Before / after:**
   - **Qualitative:** API clarity, coupling, module boundaries, error story, duplication removed/added.
   - **Quantitative** (if criteria included them): benchmarks, LOC/complexity, compile time, latency—use the same methodology as baseline when possible.
   - **Operational:** Breaking changes (semver), migration path for callers, rollout risk.
3. **Improvement verdict:** Answer explicitly: **improved**, **mixed** (summarize regressions retained), **not improved** / **premature**. If mixed or negative, propose next actions (iterate, rollback, reconsider alternative from Step 1).
4. **Alternatives residue:** Confirm whether Step 2’s recommendation still dominates or another option now looks better—and why.
5. **Record in design log (mandatory):** Append **Refactor outcome review** — criteria vs evidence, verdict, regressions/follow-ups, optional future work. **Workflow stamp:** Append exactly one standalone line `[cursor-hub workflow] step=refactor-outcome-review`.
6. **Verify:** Run `python .cursor/tools/validate_workflow_design_log.py --step refactor-outcome-review` from the project root until it passes.

This step is **analysis and documentation**; do not land large new refactors here—spawn a new workstream or return to Step 1 if major rework is needed.
