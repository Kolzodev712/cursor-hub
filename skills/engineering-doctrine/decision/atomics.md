# Decision domain — atomics and ordering

## Epistemic status

Verified: 2026-10-05 · Scope: memory orders · Classes: SPEC, HEURISTIC, POLICY, EMPIRICAL

## Questions before any technique

- What **happens-before** relationship must hold?
- Can a **mutex** + invariants express this more simply?
- If lock-free: reclamation/ABA/lifetime rules understood?

## Established facts

**[SPEC]** Valid `Ordering` per operation — RUST-STD-ATOMICS.

**[HEURISTIC — Nomicon]** If unsure about weaker orders, prefer **SeqCst** or clearer release/acquire pairing; weaken only with a **correctness argument** (benchmarks do not prove correctness). Source: RUST-NOMICON-ATOMICS.

## Possible next investigations

- Proven library patterns vs bespoke lock-free.
- Performance-motivated weakening → proof first, then contention measurement.

## Evidence

**[EMPIRICAL]** Tests/litmus; perf only after correctness established.

## Sources

- RUST-STD-ATOMICS
- RUST-NOMICON-ATOMICS
- RUST-REF-MEMORY-MODEL
