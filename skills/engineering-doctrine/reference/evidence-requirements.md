# Evidence requirements

## Epistemic status

Verified: 2026-10-05  
Scope: **POLICY** (cursor-hub agent behavior).  
Claim classes: POLICY (primary); references EMPIRICAL expectations

## Trigger

Any proposed merge that claims faster, smaller, more scalable, “cache-friendly,” or lower latency.

## Policy (cursor-hub)

**[POLICY]** Sources establish **mechanisms and API guarantees**; **measurements** establish application performance; **project doctrine** establishes objectives/invariants; **this file** establishes what agents must obtain before claims.

**[POLICY]** Project `.cursor/doctrine/` objectives and invariants **override** generic optimization preferences.

## Required minimum

- **Workload cite:** `workload.md` or explicit new assumptions.
- **Hypothesis:** Targeted limiter (CPU, memory, IO, lock, alloc, parse, etc.).
- **Method:** Test/benchmark/profile — command, profile, toolchain noted.
- **Result:** Metric delta with noise band.
- **Regression guard:** Test or benchmark when claim is durable.

## Reject when

**[POLICY]** Complexity class only; unrelated microbench; violates invariants; counter observation treated as proof of fix.

## Accept when

**[POLICY]** Evidence matches stated accept criteria; classified-path hook reads satisfied where installed.

## Relationship to hooks

Hooks record **file read at fingerprint** — not comprehension. Policy still requires using read material in the decision.

## Sources

- POLICY-CURSOR-HUB-EVIDENCE
- RUST-CARGO-PROFILES
- benchmarking.md (method tiers)
