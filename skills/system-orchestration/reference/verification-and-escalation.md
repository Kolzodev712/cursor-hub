# Verification and escalation

## Epistemic status

POLICY/IMPLEMENTED: fixture checks test supervisor behavior, not model competence, external effects or production safety.

Evaluate usefulness per unit of human attention, false alarms, unsupported claims, duplicates, operating cost and recovery correctness. Finding count is not an objective. Include a well-supported no-action outcome.

The minimum failure suite includes duplicate and conflicting event IDs, self-triggering output, out-of-scope observations, stale snapshots/policy, expired or mismatched approval, disallowed action kinds, illegal transitions, cross-run/cross-operation evidence, missing/unknown/failed checks, bounded worker retries, deadlines, pause/resume/cancel and unknown action outcomes. Persistence tests must cover checkpoints, read-only replay, incompatible scenarios, corrupt records, and transaction failure.

Before live activation, require explicit ownership, an approved mission and threat model, authenticated control inputs, restricted credentials/sandboxing, measured model behavior, trusted evidence adapters, independent budget enforcement, action reconciliation, alert limits and a tested stop procedure. Offline fixture success does not satisfy this activation review.

Escalation should explain the blocked fact, supporting evidence, affected scope, authority needed and permitted alternatives. Do not invent facts to avoid interrupting a human; do not ask repeated questions when stored approved facts resolve them. Group related exceptions and define notification thresholds instead of optimizing for endless autonomous activity.

## Sources

See `../SOURCES.md`. Test and acceptance requirements here are POLICY.
