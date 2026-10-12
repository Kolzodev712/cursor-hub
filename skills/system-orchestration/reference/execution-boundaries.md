# Execution boundaries and future adapters

## Epistemic status

POLICY: live execution must be separately designed and approved. UNVERIFIED: this kit ships no live Cursor/model/repository/machine adapter, authenticated approval channel or sandbox.

The reference reducer consumes fixtures. An `execute` event records a synthetic receipt; it does not execute a command. The only modeled action names are `emit_report` and `request_human_review`. Changing the enum is not sufficient to add a safe executor.

A live implementation needs adapters for observation ingestion, bounded worker calls, restricted actions, evidence verification and human controls. Each adapter must define input/output schemas, actor identity, credentials, target isolation, preconditions, deadlines, quota reservations, receipts, idempotency semantics, failure modes and cancellation behavior. Follow `../templates/adapter-contract.md`.

For a coding-agent adapter, restrict filesystem, network, subprocess and external-tool capabilities outside the model's writable context. An outer supervisor cannot constrain a broadly privileged inner agent merely by adding instructions. Verify the exact execution surface's rules, skills and hook semantics with integration tests. Do not assume editor, headless and hosted environments share coverage.

For an initial repository pilot, use a disposable snapshot of one component and trusted pre-existing evidence. No source/test edits, no generated test execution, no commits, no doctrine promotion, no design-log writes and no production credentials. Reports belong in a separate approved output store. The ll-cache no-code learning workflow is not permission to automate implementation.

For industrial use, start with diagnostic reporting. Keep machine motion, real-time control, emergency stops and safety interlocks outside this AI layer. This document does not authorize wiring, commissioning, or machine access.

## Sources

See `../SOURCES.md`: Anthropic workflow composition. Adapter restrictions are POLICY, not verified platform guarantees.
