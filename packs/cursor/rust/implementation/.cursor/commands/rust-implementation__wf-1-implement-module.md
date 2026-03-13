# Implement module (rust-implementation WF Step 1)

Implement from an approved design log when one exists. Cite the log; make stepwise edits; run the verification loop after each logical step. You can use this command on its own (e.g. after a design done elsewhere) — no requirement to run any other pack's workflow first.

## Steps

1. **Identify the design log:** Note which design log (e.g. `042-auth-refactor.md`) or log number is being implemented. If the user did not specify, ask or infer from context. If there is no log yet (e.g. implementing from chat only), you will create one when recording (step 6).
2. **Plan phases:** Break the implementation into 3–6 small phases (e.g. "add types", "wire API", then tests only if needed). Do not implement everything in one large edit.
3. **Tests:** Add or update tests only when (a) the design log specifies them, or (b) the behavior has non-obvious logic, edge cases, or invariants worth protecting. Do **not** add tests that only restate the implementation (e.g. asserting that a function returns a constant when the implementation is literally that constant); such tests do not catch regressions and are noise.
4. **Per phase:**
   - Make only the edits for that phase. Limit files changed per step where possible.
   - Run verification: `cargo fmt --all -- --check` (then `cargo fmt --all` if needed), `cargo clippy --fix --allow-dirty --all-targets --all-features -- -D warnings`, `cargo test --all-features`. Optionally `cargo audit` and `cargo check --all-targets --all-features` if the project uses them. Fix any failures.
   - Optionally summarize what changed before moving to the next phase.
5. **Deviations:** If implementation diverged from the design, document why in the log.
6. **Record in design log (mandatory):** Append the design log with an **Implementation Results** section: what was done, deviations from the plan, test/verification outcome. If no design log exists for this workstream, run `python .cursor/tools/new_design_log.py --slug <short-name>` (or fallback: list `./.cursor/design-log/`, take max NNN + 1, create the file), then append Implementation Results. Create logs only in `./.cursor/design-log/`. Do not consider the command complete until the log is updated. To create a log manually later, use `/design-log__create`.
7. **Verify:** Run `python .cursor/tools/validate_workflow_design_log.py --step implement` from the project root. If it fails, add the missing Implementation Results content and re-run the validator. Do not consider the command complete until the validator passes.

Do not add new dependencies or scope beyond the design log unless the user explicitly asks.
