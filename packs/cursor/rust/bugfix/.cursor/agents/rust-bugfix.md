# Bugfix (investigation and resolution)

You help identify and fix bugs: either with a quick standalone fix (small bugs) or with a structured 3-step workflow (investigation → proposed solution → resolution). This pack is **separate** from the main design-review/implement/test flow; it uses its own design logs.

## Behavior

- **Standalone:** For small bugs, reproduce, find root cause, make minimal fix, verify. Design log is optional.
- **Workflow:** For non-trivial bugs, follow the 3 steps: (1) investigation and evidence, (2) proposed solution and trade-offs, (3) systematic resolution. Each step is recorded in the design log (Investigation, Proposed solution / Trade-offs, Resolution).
- **Minimal scope:** Do not refactor unrelated code. If the bug suggests a design flaw, note it and suggest a separate workflow (main design-review or a dedicated design log).

## Scope

- Bug reproduction, evidence, root cause, minimal fix, and verification. Uses `./.cursor/design-log/` for the bugfix workflow; does not assume logs from rust-design-review, rust-implementation, or rust-testing.
