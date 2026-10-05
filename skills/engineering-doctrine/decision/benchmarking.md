# Decision domain — benchmarking and profiling

## Epistemic status

Verified: 2026-10-05 · Scope: measurement design · Classes: HEURISTIC, POLICY, IMPLEMENTATION

## Questions before any technique

- What **claim** needs proof (throughput, p99, alloc rate, correctness)?
- Which tier: microbench, component, load test, production telemetry?
- Environment **appropriate to claim** (not always identical to prod)?
- Toolchain/profile pinned?

## Benchmark tiers

| Tier | Answers |
|------|---------|
| Microbench | Local constants (isolation risk) |
| Component | Subsystem + realistic deps |
| Load | Saturation, queues |
| Telemetry | Real skew/tails |

## Possible next investigations

- Smallest benchmark that still includes **dominant dependencies** from production path.
- Hardware counters → **hypothesis only** until A/B intervention.

## Evidence

**[POLICY]** observation → hypothesis → intervention → measurement → accept/reject.

## Sources

- RUST-CARGO-PROFILES
- RUST-STD-HINT-BLACK-BOX
- LINUX-PERF
