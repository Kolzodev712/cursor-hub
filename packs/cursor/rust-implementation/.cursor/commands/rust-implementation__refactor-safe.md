# Refactor Safe

Plan 3–6 steps; limit files per step; run tests after each step; stop and show a short diff summary between steps.

## Steps

1. **Scope:** Identify the refactor goal and the set of files/types affected. List them.
2. **Plan steps:** Define 3–6 steps so that after each step the project still builds and tests pass. Prefer additive steps (new types, then migrate call sites, then remove old) over big-bang edits.
3. **Execute step by step:**
   - For each step: edit only the files needed for that step.
   - Run `cargo test --all-features` (and if desired `cargo clippy --fix --allow-dirty --all-targets --all-features -- -D warnings`) after the step.
   - If tests fail, fix before continuing.
   - Optionally show a one-line summary or short diff summary of what changed in that step.
4. **Final check:** Run full verification: `cargo fmt --all -- --check` (then `cargo fmt --all` if needed), `cargo clippy --fix --allow-dirty --all-targets --all-features -- -D warnings`, `cargo test --all-features`. Summarize the refactor outcome.

Do not change behavior; refactor only structure, naming, or duplication. If behavior changes are required, call that out and get explicit approval.
