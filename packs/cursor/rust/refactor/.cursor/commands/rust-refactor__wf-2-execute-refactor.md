# Refactor — execute (rust-refactor WF Step 2)

**Goal:** Carry out the **refactor or replacement** aligned with **Refactor assessment** from `/rust-refactor__wf-1-assess-fit-and-alternatives` (same design-log workstream). Use phased edits and the Rust verification loop.

**Use after:** Assessment step completed and recommendation agreed (or user explicitly skips assessment and points to prior context—still record assessment summary in log first if missing).

## Steps

1. **Bind to the log:** Open the relevant design log; restate in one paragraph the recommendation and acceptance criteria from **Refactor assessment**. If absent, summarize what you are executing and append a minimal **Refactor assessment** retrospectively before implementing.
2. **Plan phases:** Break into 3–6 phases (e.g. introduce new types, migrate call sites, delete old path). Each phase should leave the tree buildable and tests passing when possible.
3. **Per phase:**
   - Edit only what that phase needs; avoid scope creep beyond the assessment.
   - Run verification: `cargo fmt --all -- --check` (then `cargo fmt --all` if needed), `cargo clippy --fix --allow-dirty --all-targets --all-features -- -D warnings`, `cargo test --all-features`. Optionally `cargo audit` and `cargo check --all-targets --all-features` if the project uses them. If the project has a justfile, `just` recipes may substitute. Fix failures before continuing.
4. **Deviations:** If you diverge from the assessment, document **why** in the log before finishing.
5. **Record in design log (mandatory):** Append **Refactor implementation** — what changed (modules, APIs, dependency changes), deviations, verification outcome (commands run, pass/fail). **Workflow stamp:** Append exactly one standalone line `[cursor-hub workflow] step=refactor-implement`.
6. **Verify:** Run `python .cursor/tools/validate_workflow_design_log.py --step refactor-implement` from the project root until it passes.

If the assessment concluded “replace with X” but implementation reveals a blocker, stop, append a short note to the log, and return to Step 1 for a revised assessment rather than silently changing direction.
