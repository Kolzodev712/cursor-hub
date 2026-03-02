# Add Tests Only

Add or extend tests and fixtures only. No production code changes. Justify coverage.

## Steps

1. **Scope:** Identify what behavior or module needs more tests. Confirm with the user if unclear.
2. **Tests only:** Add or edit only test code and test fixtures (e.g. in `tests/`, `#[cfg(test)]` modules, or test helpers). Do not change production code.
3. **Justify coverage:** For each new test, state what it covers (e.g. "edge case: empty input", "round-trip of config"). Avoid adding tests that only repeat existing behavior without adding value.
4. **Verification:** Run `cargo test --all-features`. Ensure no existing tests break. Run `cargo fmt --all -- --check` (then `cargo fmt --all` if needed) and `cargo clippy --fix --allow-dirty --all-targets --all-features -- -D warnings` on the test code.

If the desired coverage requires production code changes (e.g. to make something testable), say so and suggest a separate task; do not make those changes in this command.
