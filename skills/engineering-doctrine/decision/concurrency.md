# Decision domain — concurrency structure

## Epistemic status

Verified: 2026-10-05 · Scope: threads/tasks/queues · Classes: HEURISTIC, POLICY, EMPIRICAL

## Questions before any technique

- Embarrassingly parallel vs **coordination-bound**?
- What mutable state is shared; can **one writer** own it?
- Latency vs throughput SLO; cancellation semantics?
- Which **runtime/library** (Tokio, crossbeam, std) — read **its** docs for queue/backpressure semantics?

## Possible next investigations

- Reduce shared mutable state; clarify ownership boundaries.
- Contention on locks/queues → measure under load before lock-free or micro-opts.
- **Atomics** domain when cross-thread ordering is the core question.
- Bounded vs unbounded buffering → **runtime-specific**; justify with overload behavior + SLO.

## Evidence

**[EMPIRICAL]** Stress/load tests; review deadlock/livelock; saturation behavior.

## Sources

- RUST-STD-ATOMICS
