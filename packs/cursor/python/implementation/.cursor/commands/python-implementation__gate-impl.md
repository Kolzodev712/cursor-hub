# Implementation gate (Standalone — strict / dev-led)

IMPLEMENTATION MODE (HARD GATE). You are **NOT** allowed to write any code until the user provides **all** of the following:

- The data types / interfaces (classes, dataclasses, or types) that will exist
- The exception types or error handling approach (if relevant)
- Function/method signatures for the feature (inputs/outputs)
- How it wires into the system (who calls what, where it is invoked)

## Rules

1. If any item above is missing, respond **only** with:
   - "BLOCKED: API shape incomplete"
   - "MISSING:" list (exact missing items)
   - 3–7 targeted questions to complete the API/wiring
2. **Unblock criteria:** Once the user provides the full API shape + wiring (types, error handling, signatures, wiring), you may implement **only** function/method bodies.
3. You may **NOT** change the types, signatures, or wiring. If you think changes are necessary, **STOP** and respond:
   - "BLOCKED: shape change required"
   - The minimal change list + reason
   - Wait for the user's approval. If they approve, treat the updated shape as the new gate and proceed.
4. **Scope of the gate:** After you deliver the implementation (bodies), this gate no longer applies for this task unless the user invokes this command again.
5. **ALSO:** Do not refactor, rename, or introduce new abstractions unless the user explicitly requests it. Keep changes minimal and localized.
