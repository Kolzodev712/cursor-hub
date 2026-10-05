# Decision domain — allocation

## Epistemic status

Verified: 2026-10-05 · Scope: heap/allocator behavior · Classes: HEURISTIC, EMPIRICAL, IMPLEMENTATION

## Questions before any technique

- Is allocation **measurable** on the critical path?
- Count, sizes, lifetimes, thread ownership?
- Which **allocator** is linked (system, mimalloc, jemalloc, arena — project fact)?
- Would pooling increase retention, sync cost, or complexity?

## Possible next investigations

- Reduce alloc **count** on hot path when profile shows alloc cost (measure).
- **Arena/pool** when size classes and lifetimes stable (measure footprint + contention).
- Global allocator swap → **platform** research for that allocator + A/B on **your** binary.

## Evidence

**[EMPIRICAL]** Allocator profiles / heap tools + latency distribution on load test.

## Sources

- RUST-STD-VEC
- RUST-CARGO-PROFILES
