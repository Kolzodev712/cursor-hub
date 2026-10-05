# Benchmarking

## Epistemic status

Verified: 2026-10-05  
Scope: Methodology; tool choice is project-specific.  
Claim classes: HEURISTIC, EMPIRICAL, POLICY, IMPLEMENTATION

## Trigger

Before/after optimization; regression guard; interpreting profiles.

## Established facts

**[IMPLEMENTATION]** Cargo profiles control `opt-level`, debug info, LTO separately. Source: RUST-CARGO-PROFILES.

**[SPEC]** `std::hint::black_box` inhibits certain compiler optimizations in microbenchmarks. Source: RUST-STD-HINT-BLACK-BOX.

**[IMPLEMENTATION]** LLVM vectorization behavior depends on compiler version and flags — document toolchain when comparing asm/vectorization. Source: LLVM-VECTORIZERS, RUST-RUSTC-CODEGEN.

## Benchmark kinds (different questions)

| Kind | Answers |
|------|---------|
| Microbenchmark | Local algorithm/constants (high isolation risk) |
| Component benchmark | Subsystem with realistic deps |
| Load / soak test | Throughput, saturation, queues |
| Production telemetry | Tail latency, real skew |
| Hardware counters | Hypothesis about limiter — not automatic fix |

**[POLICY]** Environment must be **appropriate to the claim**, not necessarily identical to every production machine (e.g. microbench on dev CPU vs tail-latency claim on prod topology).

## Decision questions

- What claim are we proving (p99 latency, throughput, alloc count)?
- Input distribution matches `workload.md`?
- Warmup, variance, pinned toolchain/profile?
- Does microbench include dependencies that dominate in production?

## Engineering guidance

**[HEURISTIC]** Report distributions (p50/p99), not single runs.

**[HEURISTIC]** Prefer the **smallest benchmark that still includes dependencies that matter** — if microbench omits them, escalate benchmark tier.

**[POLICY]** observation (perf) → hypothesis → intervention → remeasure → accept/reject.

## Evidence required

**[EMPIRICAL]** Stored commands, profile flags, results, thresholds in CI or design log.

## Accept / reject

**Accept** reproducible methodology and claim/benchmark tier alignment.

**Reject** production tail-latency claims from unrepresentative microbenches alone.

## Sources

- RUST-CARGO-PROFILES
- RUST-STD-HINT-BLACK-BOX
- LLVM-VECTORIZERS
- LINUX-PERF
