# State and recovery

## Epistemic status

MECHANISM: controllers compare observed and desired state; SQLite supports transactional local state. POLICY/IMPLEMENTED: this kit uses a bounded offline reducer and explicit SQLite checkpoints. It is not a live scheduler.

## Lifecycle

`ADMITTED -> INVESTIGATING -> PROPOSED -> AUTHORIZED -> EXECUTED -> VERIFIED` is the normal fixture path. Approval-required actions can wait at `AWAITING_APPROVAL`. Failed worker attempts can return to `ADMITTED` only within the recorded budget. `NO_ACTION`, `BLOCKED`, `REJECTED`, `FAILED`, `CANCELLED` and `VERIFIED` are terminal for this v1 run. Resolving a blocked condition requires a new explicitly revised scenario/run, not silent revival.

An uncertain action receipt creates `OUTCOME_UNKNOWN`. Do not resend the action or erase the uncertainty with cancellation. Reconcile the original operation identifier; record its outcome even if the target changed. A stale proposal cannot then be verified against the changed target. Cancellation never reverses an action already performed.

Pause prevents new progress but permits explicit resume, cancellation, changes of target/policy, and reconciliation. Deadlines use fixture integer timestamps, not wall-clock timers; the simulator has no autonomous timer events. Recorded model-call/token limits are checked against fixture usage. A live worker needs pre-dispatch reservations, cancellation/timeouts and independent accounting.

## Identity and deduplication

Event IDs bind to exact event content. Repeated exact events are ignored; conflicting reuse is invalid. Different observations of the same mission fingerprint, scope and snapshot are deduplicated. The snapshot must represent ALL relevant inputs, including test evidence and doctrine versions where required. New evidence with an unchanged snapshot will intentionally not create fresh work. Keep event timestamps nondecreasing in scenario files.

The mission's run/event limits bound one scenario/journal. Worker budgets and duration are per run. A live service additionally needs global quotas, queue limits, concurrency ownership and admission fairness; none are claimed here.

## Checkpoints and replay

An optional journal stores the scenario and each event/decision/state fingerprint. One invocation commits its processed prefix atomically. On failure the transaction rolls back; a subsequent call reconstructs the last committed prefix before appending. `--steps N` limits additional events. The default is in-memory SQLite with no persistent journal.

Replay recomputes decisions from recorded events. It never invokes a model and never pretends a new model result is a replay. A changed scenario or mission requires a new journal. Format changes fail closed; there is no automatic migration. Fingerprints detect inconsistency, not malicious rewriting by someone with file access. Use operator-owned local storage, not a worker-writable or untrusted shared directory; this is not a filesystem sandbox or multi-tenant database.

## Sources

See `../SOURCES.md`: Kubernetes controllers and Python sqlite3. Specific states and limits are POLICY.
