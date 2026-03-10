# Test gate (Standalone — strict / dev-led)

TESTING MODE (HARD GATE). You are **NOT** allowed to write any test code until the user provides a detailed test breakdown including:

- List of test cases (happy paths + edge cases + failure cases)
- What each test asserts (expected outputs/effects)
- Unit vs integration split
- Any fixtures/mocks needed and where they come from
- Any concurrency/failure scenarios that must be exercised (if applicable)

## Rules

1. If the breakdown is incomplete, respond **only** with:
   - "BLOCKED: test plan incomplete"
   - "MISSING:" list (exact missing parts)
   - 3–7 targeted questions to complete the test plan
2. **Unblock criteria:** Once the user provides the full test plan (cases, assertions, unit/integration split, fixtures, and any concurrency/failure scenarios), implement tests **exactly** as specified.
3. You may **not** add extra tests unless the user explicitly asks. If you notice a missing test case, do **not** implement it; instead respond with "Suggested addition: [brief description]" and wait for the user's approval.
4. **Scope of the gate:** After you deliver the tests, this gate no longer applies for this task unless the user invokes this command again.
5. **ALSO:** Do not refactor, rename, or introduce new abstractions unless the user explicitly requests it. Keep changes minimal and localized.

