# Fault-first method: analyst procedure

## 1. Bound the investigation

State the requested target (design proposal, existing component, integration boundary, or named top-level failure). Name what is **not** being assessed. Identify environment, callers, inputs, outputs, trust boundaries, concurrency assumptions, resource limits, and lifecycle where supported by evidence. Avoid broad architecture reviews when the user names one function.

## 2. Establish contracts

Build a short contract ledger: ID, guarantee, source (user requirement, project doctrine, test, specification, or code observation), and status (`KNOWN`, `UNKNOWN`, `NOT_APPLICABLE`). **Code behavior is evidence of implementation, not necessarily evidence of intended requirements.** Project invariants outrank optimization heuristics. When sources conflict, expose the conflict; do not choose silently.

## 3. Define top events

For each important guarantee, invert it into an unacceptable outcome. Examples: invalid state accepted, required event lost, action duplicated, unbounded resource use, deadlock, inconsistent recovery, protocol boundary violation, or latency bound exceeded *when a bound is actually specified*. Do not assume all examples apply.

## 4. Choose one analysis lens

- **Failure-mode reasoning (FMEA-inspired)**: inspect operations and interfaces, ask how each can deviate and what propagates downstream. Useful for localized components. No numerical RPN unless defensible project data and an approved scoring scheme exist.
- **Fault-tree reasoning (FTA-inspired)**: start from one clearly defined top event, derive necessary/alternative contributing events with AND/OR semantics. Do not call a mere list of causes a rigorous fault tree. Label independence assumptions and common-cause dependencies.
- **Control-interaction reasoning (STPA-inspired)**: where a controller, feedback, timing, or authority matters, examine omitted/incorrect/early/late/too-long control actions. Do not claim a complete STPA without the required control structure and safety constraints.

Use one primary lens; add a second only if it exposes a distinct mechanism. These methods guide investigation and do not themselves prove defects.

## 5. Derive and challenge hypotheses

For each candidate, describe:

`trigger/precondition → internal state or interaction → violated guarantee → consequence`.

Then identify existing controls, evidence that supports the chain, counterevidence, and missing information. If a precondition is not established, the finding stays a hypothesis. An absent documented requirement is a `REQUIREMENT_GAP` until clarified.

Include ordinary faults (malformed/truncated inputs, bounds, state transitions, resource exhaustion) and interaction faults (ordering, retries, partial failure, cancellation, races) only when relevant to the actual component. Do not produce a generic checklist of all categories.

## 6. Prioritize qualitatively

Use a transparent rationale: consequence (catastrophic/high/moderate/low as locally meaningful), reachability or exposure (observed/plausible/unknown), detectability and existing controls, and confidence. Do not conflate severity and likelihood. Never fabricate a failure probability or numerical risk priority number.

## 7. Design discriminating checks

Each proposed test/experiment states:

- hypothesis and required setup;
- exact stimulus or failure condition;
- observable expected behavior under the contract;
- what would confirm versus falsify the hypothesis;
- constraints and side effects (especially network, storage, production, security);
- whether the check is already present, merely proposed, or actually executed.

Favor deterministic boundary cases, state-machine transitions, property-based generation, and controlled fault injection where justified. Existing test names are not proof of execution; distinguish inspected tests from observed test results. Do not run experiments with external effects without approval.

## 8. Stop and hand back control

Normally stop at 3–7 material findings and at most three next investigations. A useful outcome may be *no demonstrated defect*, a precise requirement gap, or a design constraint. Report residual risk and unexamined areas. Do not automatically edit project doctrine, generate tests, create design logs, or enter an implementation loop. Human approval is required for promotion into durable policy or code.
