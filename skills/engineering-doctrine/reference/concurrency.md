# Concurrency (Rust std and project runtime)

## Epistemic status

Verified: 2026-10-05  
Scope: Generic Rust threading/sync; **async runtimes are project-specific**.  
Claim classes: HEURISTIC, POLICY, EMPIRICAL, SPEC

## Trigger

Threads, shared state, channels, async tasks, backpressure design.

## Established facts

**[SPEC]** `Mutex`, `RwLock`, atomics, and `thread` APIs have documented semantics in `std`. Sources: RUST-STD-ATOMICS, std sync docs.

**[IMPLEMENTATION]** Tokio/async runtimes, `crossbeam`, `rayon`, etc. have **their own** queue/fairness/backpressure semantics — read **that** library’s docs; do not generalize.

## Decision questions

- Embarrassingly parallel vs coordination-bound?
- Latency vs throughput SLO?
- Cancellation/partial-failure semantics (runtime-specific)?
- Can **one writer** own mutable state (type system + architecture)?

## Engineering guidance

**[HEURISTIC — cursor-hub policy bias]** Prefer clear **ownership** and minimal shared mutable state before layered locking.

**[HEURISTIC — cursor-hub policy bias]** Prefer **bounded** queues/backpressure when unbounded buffering risks memory/latency failure — **verify** against your runtime’s queue API (bounded vs unbounded).

**[HEURISTIC]** Match OS threads vs async tasks to project architecture (`architecture.md`).

## Evidence required

**[EMPIRICAL]** Stress tests, deadlock review, saturation/load behavior on representative topology.

## Accept / reject

**Accept** when model matches invariants and load evidence meets SLO or gap is documented.

**Reject** universal claims about “always use lock-free” or “always unbounded channel.”

## Sources

- RUST-STD-ATOMICS
- RUST-NOMICON-ATOMICS
- (Project) runtime docs — not in SOURCES.md until pinned per project
