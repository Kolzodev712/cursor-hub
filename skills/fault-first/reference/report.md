# Fault-first report contract

Keep sections short for small components. Do not create a repository artifact unless explicitly requested.

## Scope and evidence

- Target, revision/branch if known, analysis mode (`proposed design` or `existing implementation`), interfaces, and exclusions.
- Inspected requirements, project facts, code/tests, and unavailable evidence.
- Contract ledger: `ID | Guarantee | Source | Status (KNOWN/UNKNOWN/N/A)`.

## Unacceptable outcomes and causal analysis

Name 1–3 primary top events. For each, give an explicit causal chain or small AND/OR tree where meaningful; mark unsupported assumptions. Distinguish observed behavior from intended behavior.

## Prioritized findings

Use this table for each material finding:

| ID | Status | Guarantee | Trigger → mechanism → effect | Existing controls/counterevidence | Consequence / exposure / confidence | Verification |
| --- | --- | --- | --- | --- | --- | --- |

Statuses: `CONFIRMED_DEFECT`, `CREDIBLE_HYPOTHESIS`, `REQUIREMENT_GAP`, `EXCLUDED`. A confirmed defect needs an inspectable trace/test or direct contradiction with an established contract. Avoid invented metrics, probabilities, and citations.

## Proposed validation

For each non-excluded material hypothesis: exact setup/stimulus, expected observable result, falsifying result, side-effect risk, and whether the check is **PROPOSED**, **INSPECTED_NOT_RUN**, or **EXECUTED**. Only use `EXECUTED` with actual observed results.

## Decision and stop condition

- At most three prioritized next investigations (with owner decisions when needed).
- Explicit unknowns and residual risks; do not claim completeness.
- `STOP`: scope sufficiently investigated, or `BLOCKED`: missing essential contract/evidence. Do not proceed into implementation without new authorization.

## Optional design implications

Propose candidate invariants, architecture constraints, or design-log decisions for **human approval only**. No automatic writes.
