# Refactor — execute (js-ts-refactor WF Step 2)

**Goal:** Execute the **Refactor assessment** recommendation in **phases** with lint, type-check, and test verification suited to JS/TS projects.

**Use after:** `/js-ts-refactor__wf-1-assess-fit-and-alternatives` (or retrospectively patched assessment summary).

## Steps

1. **Bind to log:** One paragraph recap of acceptance criteria vs plan; append minimal assessment if lacking.
2. **Plan phases:** 3–6 steps; branches stay green whenever possible (`npm/yarn/pnpm` scripts as emitted by repo).
3. **Per phase:** Scope tightly; verify with **lint** (e.g. `npm run lint`, `eslint .`), **typecheck** if used (`tsc --noEmit`, `npm run typecheck`), **tests** (`npm test`). Use project scripts (`pnpm biome`, `vite build --mode`, Playwright)—document what ran. Fix before next phase.
4. **Deviation note** in log if plan changes materially.
5. **Record:** **Refactor implementation** + `[cursor-hub workflow] step=refactor-implement`.
6. **Verify:** `python .cursor/tools/validate_workflow_design_log.py --step refactor-implement` until passes.

Blockers → annotate log and rerun wf‑1 rather than drifting silently.
