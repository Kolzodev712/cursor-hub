---
name: fault-first
description: >-
  Explicit, bounded, read-only analysis of how a software design or existing component
  might violate requirements; uses fault trees, failure-mode reasoning, and test hypotheses.
  Invoke for pre-implementation risk review or investigation of failure boundaries, not routine edits.
---

# Fault-first: reverse engineering from unacceptable outcomes

## When to use

Use **only** on explicit request (for example `/fault-first__analyze`) or an unambiguous request to analyze failure modes. This is not an always-on gate. For ordinary edits, debugging, or code generation, use the existing workflows. Read `reference/method.md` for the complete procedure and `reference/report.md` for the output contract. Do not preload other technique catalogs.

## Core contract

- **Read-only by default**: no code edits, test creation, project-doctrine edits, design-log writes, destructive probes, external side effects, or live fault injection without separate authorization. Read source and existing tests to assess evidence. Non-mutating checks are allowed; when a command's side effects are uncertain, ask first.
- **Requirements first**: begin with actual user requirements, documented invariants, and observed architecture. Never infer performance or safety guarantees from a technology label alone.
- **Failure-first, not pessimism-first**: choose a bounded set of unacceptable outcomes and trace plausible contributing conditions. No endless lists of theoretical defects.
- **Epistemic labels**: `CONFIRMED_DEFECT` (reproducible or directly demonstrated violation), `CREDIBLE_HYPOTHESIS` (mechanism with untested assumptions), `REQUIREMENT_GAP` (behavior/limit not specified), `EXCLUDED` (ruled out by evidence or scope). `CONFIRMED_DEFECT` requires a concrete trace, test result, or direct proof from code and established requirements.
- **Evidence traceability**: each finding references exact requirement/invariant and source location or observation. If source cannot be inspected, say so and reduce confidence.
- **Risk ranking**: use qualitative consequence, exposure/trigger feasibility, existing controls, and uncertainty. Do not invent numerical probabilities, RPNs, or incident frequencies. Critical severity is not synonymous with likely occurrence.
- **Validation**: propose falsifiable checks with setup, stimulus, expected observation, and acceptance condition. Proposals are not executed tests.
- **Human boundary**: suggest new invariants/design constraints, but do not install them as policy without user approval. The user owns architecture and implementation decisions.

## Bounded workflow

1. Establish the scope: component, interfaces, trust boundaries, operating assumptions, lifecycle/state, and in-scope vs out-of-scope failures.
2. Extract guarantees and unacceptable outcomes; mark `KNOWN`, `UNKNOWN`, and `NOT_APPLICABLE` distinctly.
3. Choose the relevant lens: failure-mode analysis for component behaviors; fault-tree reasoning for one top event; control-interaction analysis for sequencing/feedback/control authority. They are different tools; do not force all three into every review.
4. Derive candidate causal paths (input → state/interaction → violation). Check existing controls and tests. Search for counterevidence before escalating.
5. Prioritize a small set (normally 3–7, fewer for tiny components). Do not turn an unknown requirement into a claimed defect.
6. Propose targeted experiments/tests and what would falsify each hypothesis. For design-only work, tests are proposals, not executed proof.
7. Stop when top consequences have credible coverage, residual uncertainty is explicit, and the next action is clear. If architecture evidence is too thin, stop with a precise knowledge-gap request rather than inventing a failure tree.

## Output

Use `reference/report.md`. Keep the report proportional to the component. At most three recommended next investigations. If no credible failures are found, report that the **analysis did not identify** one within scope, not that the system is safe.

## Methodology provenance

See `reference/sources.md` for official method starting points and limitations. FMEA, FTA, STPA, HAZOP, property-based testing, and chaos engineering are distinct approaches; this skill is an engineering adaptation, **not a certification of conformance** to any standard.
