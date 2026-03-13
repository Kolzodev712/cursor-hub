# PR review (Standalone)

File-by-file review with "must-fix" vs "nice-to-have" findings.

## Steps

1. **Scope:** Identify the set of files or diffs to review (e.g. from a PR description, or the user will point to files).
2. **Per file:** Walk through each changed file. For each:
   - **Correctness:** Any logic errors, type misuse, or undefined behavior?
   - **API:** Are public API changes intentional and backward-compatible?
   - **Error handling:** Unwrap/expect in production paths? Missing error propagation?
   - **Performance:** Unnecessary allocations or work?
   - **Security:** Input validation, invariants, sensitive data?
   - **Unsafe:** Any `unsafe` with a clear invariant comment?
   - **Tests:** Is new behavior tested? Are edge cases covered?
3. **Classify:** For each finding, label **must-fix** (correctness, safety, API contract) or **nice-to-have** (style, minor perf, clarity).
4. **Summary:** List must-fix items first, then nice-to-have. Suggest concrete changes where helpful.

Keep the review actionable. Quote file/line or snippet when referring to a finding.

