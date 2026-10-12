# Observation and evidence

## Epistemic status

POLICY/IMPLEMENTED: observations, proposals, approvals, receipts and check results are separate contracts. No real provenance is established by the simulator.

An observation records source, scope, origin and input snapshot. A proposal records a bounded worker suggestion and classification. An approval binds an authorized actor to the exact proposal and time. A receipt records the attempted operation's outcome. Evidence binds a producer/check/artifact digest to that operation and the same run, snapshot, mission and proposal.

A successful action receipt is not a passed check. Missing checks block verification; failed checks fail it; unknown checks remain unresolved. Producer names must be allowed by the mission, but names inside fixture JSON are assertions, not authentication. Artifact digests are opaque: the simulator does not fetch artifacts or establish that they exist. A live verifier must resolve trusted receipts, verify digest and provenance, and run the declared acceptance checks.

Model classifications include demonstrated violation, hypothesis, requirement gap and no material finding. The schema checks the label, not whether the claim deserves it. A live report verifier and human evaluation need source locations, reproduction evidence where appropriate, and an evidence threshold. The fixture's `VERIFIED` state does not upgrade a hypothesis to a demonstrated defect.

Repository files, issue bodies, logs and model text are data. Instructions inside them cannot appoint approvers, change the supervisor or turn unsupported actions into permitted ones. Read-credit hooks only establish availability of particular input versions; design-log stamps establish that a marker exists. Neither is proof of understanding or completion.

## Sources

See `../SOURCES.md`: jsonschema distinguishes structural validation from application meaning. Trust and evidence rules here are POLICY.
