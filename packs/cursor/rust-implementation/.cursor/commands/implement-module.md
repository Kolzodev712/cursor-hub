# Implement Module

Implement from an approved design log. Cite the log number; make stepwise edits; run the verification loop after each logical step.

## Steps

1. **Identify the design log:** Note which design log (e.g. `042-auth-refactor.md`) or log number is being implemented. If the user did not specify, ask or infer from context.
2. **Plan phases:** Break the implementation into 3–6 small phases (e.g. "add types", "wire API", then tests only if needed). Do not implement everything in one large edit.
3. **Tests:** Add or update tests only when (a) the design log specifies them, or (b) the behavior has non-obvious logic, edge cases, or invariants worth protecting. Do **not** add tests that only restate the implementation (e.g. asserting that a function returns a constant when the implementation is literally that constant); such tests do not catch regressions and are noise.
4. **Per phase:**
   - Make only the edits for that phase. Limit files changed per step where possible.
   - Run verification: `cargo fmt --all -- --check` (then `cargo fmt --all` if needed), `cargo clippy --fix --allow-dirty --all-targets --all-features -- -D warnings`, `cargo test --all-features`. Fix any failures.
   - Optionally summarize what changed before moving to the next phase.
5. **Implementation Results:** After implementation, append the design log with an "Implementation Results" section: what was done, any deviations from the plan, and test/verification outcome. If there was no design log (direct request), and you suggest the user record this later, tell them to use the **/adr-new** command with a slug (or run `python tools/new_design_log.py --slug <name>`); do not say "via design-log/" or mention a "/design-log" command.
6. **Deviations:** If implementation diverged from the design, document why in the log.

Do not add new dependencies or scope beyond the design log unless the user explicitly asks.
