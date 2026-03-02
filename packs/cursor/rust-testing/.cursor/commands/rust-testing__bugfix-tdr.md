# Bugfix TDR (Test-Driven Repair)

Failing test first, then fix, then clean fmt/clippy/test loop.

## Steps

1. **Reproduce:** Identify the bug (from issue, user description, or stack trace). Locate the relevant code and behavior.
2. **Write a failing test:** Add or modify a test that clearly fails due to the bug. The test should describe the expected behavior. Run `cargo test --all-features` and confirm the new test fails.
3. **Fix:** Make the minimal code change that makes the test pass. Do not refactor unrelated code unless necessary.
4. **Verification:** Run `cargo fmt --all -- --check` (then `cargo fmt --all` if needed), `cargo clippy --fix --allow-dirty --all-targets --all-features -- -D warnings`, `cargo test --all-features`. Fix any failures.
5. **Summarize:** Briefly state what was wrong and what change fixed it.

Keep the fix minimal. If the bug suggests a design flaw, note it and consider suggesting a design log for a larger change; do not expand scope in this command unless asked.
