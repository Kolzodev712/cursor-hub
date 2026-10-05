# Algorithm selection

## Trigger

You need asymptotic or constant-factor behavior on a **dominant operation** (lookup, insert, scan, join, rank).

## Questions

- What are **N**, growth rate, and **bounded vs unbounded** domain?
- Is the key space **dense** enough for direct indexing?
- Read-heavy vs write-heavy vs mixed? Delete frequency?
- Need ordering, range queries, or only point lookup?
- Worst-case latency vs average throughput — which matters?

## Reasoning

- **Dense, small, stable domain:** Compare direct table / bitmap vs hash — measure cache footprint, not just O().
- **Sparse string/struct keys:** Hash map only after ruling out interning / perfect hashing when inputs are constrained.
- **Ordering/range:** Tree or sorted array + binary search — pay log factor only when queries require order.
- **Batching:** Amortize structure maintenance when updates arrive in bursts.

## Exceptions

- Correctness or invariant checks dominate — prefer clarity until profile shows otherwise.
- N is tiny and fixed — complexity notation is irrelevant; measure constants.

## Evidence

- Identify hot call site in profile or trace.
- Compare candidates on **representative** size distribution from `workload.md`.
- Regression test for functional equivalence before/after.

## Accept when

Chosen structure matches workload facts and measurement (or explicit lack of hot path) is documented.
