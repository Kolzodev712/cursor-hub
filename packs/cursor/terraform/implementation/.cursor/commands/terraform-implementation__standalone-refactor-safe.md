# Refactor safe (Standalone)

Plan 3–6 steps; limit files per step; run tests after each step; stop and show a short diff summary between steps.

## Steps

1. **Scope:** Identify the refactor goal and the set of files/modules affected. List them.
2. **Plan steps:** Define 3–6 steps so that after each step the config still passes `terraform fmt` and `terraform validate`. Prefer additive steps (new resources/modules, then migrate references, then remove old) over big-bang edits.
3. **Execute step by step:**
   - For each step: edit only the files needed for that step.
   - Run `terraform fmt -recursive` and `terraform validate` after the step. Optionally `terraform plan` to confirm no unexpected changes.
   - If validation fails, fix before continuing.
   - Optionally show a one-line summary or short diff summary of what changed in that step.
4. **Final check:** Run full verification (`terraform fmt -recursive`, `terraform validate`, and optionally `terraform plan`). Summarize the refactor outcome.

Do not change behavior; refactor only structure, naming, or duplication. If behavior changes are required, call that out and get explicit approval.
