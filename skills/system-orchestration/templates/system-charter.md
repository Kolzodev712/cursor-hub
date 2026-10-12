# System charter — DRAFT, NOT ACTIVE

## Objective and non-goals

State the standing responsibility, measurable desired outcome, named scope, and explicit non-goals. Why does this require model judgment rather than ordinary application logic?

## Observations and trust

Name event sources, authentication, snapshot composition, freshness rules, deduplication keys and data treated as untrusted. Mark unresolved facts explicitly.

## Authority

Name policy owner, allowed actions, prohibited actions, approval conditions/expiry and protected policy/credential storage. Installation and editing this document do not activate a service.

## Lifecycle and bounds

Provide the state/transition table; define no action, waiting, blocked, failed and uncertain outcomes. Specify per-run and global budgets, deadlines, queue/concurrency limits, retries, pause, cancellation and restart semantics.

## Evidence and verification

Define acceptance checks, authoritative evidence producers, artifact identity, operation receipts, stale-decision checks and what each success claim does NOT prove.

## Adapters and human controls

Attach adapter contracts and specify isolated permissions, escalation thresholds, review interface, operation reconciliation and a stop procedure.

## Evaluation and activation decision

Record offline scenarios, expected outcomes, model-evaluation criteria, live integration gaps, and explicit operator approval requirements. Unresolved authority or safety facts block activation. Keep this design separate from deployed configuration.
