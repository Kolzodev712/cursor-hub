# Adapter contract — DRAFT, NOT ACTIVE

Name the adapter: observer, worker, action executor, evidence verifier or human control.

Define its schema version and inputs/outputs; authenticated caller/producer identity; approved resource scope; credential ownership; filesystem/network/tool permissions; immutable policy sources; operation and idempotency identifiers; target and policy preconditions; quota reservation and independent usage accounting; timeout/cancellation semantics; action receipt format; ambiguous-outcome reconciliation; retry policy; evidence and digest validation; audit retention; and dependency/version constraints.

Document what the supervisor can mechanically enforce and what remains an assumption. Include one success fixture, each bounded failure, an interruption test, an authorization-bypass test and an independent verification test. Do not describe a generic shell as a restricted action interface.
