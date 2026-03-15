# Refactor safe (Standalone)

Plan 3–6 steps; limit files per step; run tests after each step; stop and show a short diff summary between steps.

## Steps

1. **Scope:** Identify the refactor goal and the set of files/modules affected. List them.
2. **Plan steps:** Define 3–6 steps so that after each step the project still passes format/lint/tests. Prefer additive steps (new interfaces, then migrate call sites, then remove old) over big-bang edits.
3. **Execute step by step:**
   - For each step: edit only the files needed for that step.
   - Run tests (`npm test`) and any lint/format the project uses after the step.
   - If tests fail, fix before continuing.
   - Optionally show a one-line summary or short diff summary of what changed in that step.
4. **Final check:** Run full verification (format, lint, type check if used, npm test). Summarize the refactor outcome.

Do not change behavior; refactor only structure, naming, or duplication. If behavior changes are required, call that out and get explicit approval.
