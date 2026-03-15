# Add tests only (terraform-testing WF Step 1)

Add or extend tests and fixtures only. No production code changes. Justify coverage. You can use this command on its own (e.g. to add tests for existing code) — no requirement to run design-review or implementation first.

## Steps

1. **Scope:** Identify what behavior or module needs more tests. Confirm with the user if unclear.
2. **Tests only:** Add or edit only test code and test fixtures (e.g. in `tests/`, test modules). Do not change production code.
3. **Justify coverage:** For each new test, state what it covers (e.g. "edge case: empty input", "round-trip of config"). Avoid adding tests that only repeat existing behavior without adding value.
4. **Verification:** Run `terraform validate` and any project test/check (e.g. terratest, check blocks, policy). Ensure no existing checks break. Run `terraform fmt -recursive` if needed.
5. **Record in design log (mandatory):** Append a **Test session** section to the design log for this workstream: what was covered, how tests were run, any failures fixed. If no log exists, run `python .cursor/tools/new_design_log.py --slug <short-name>` (or fallback: create the file in `./.cursor/design-log/`), then add the Test session content. Create logs only in `./.cursor/design-log/`. Do not ask — do it.
6. **Verify:** Run `python .cursor/tools/validate_workflow_design_log.py --step add-tests` from the project root. If it fails, add the missing Test session content and re-run the validator. Do not consider the command complete until the validator passes.

If the desired coverage requires production code changes (e.g. to make something testable), say so and suggest a separate task; do not make those changes in this command.
