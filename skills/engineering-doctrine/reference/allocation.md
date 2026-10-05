# Allocation

## Epistemic status

Verified: 2026-10-05  
Scope: Rust allocation API; allocator choice is project-specific.  
Claim classes: SPEC, IMPLEMENTATION, EMPIRICAL, HEURISTIC, POLICY

## Trigger

Allocator time in profile; latency spikes; considering pools/arenas/global allocator swap.

## Established facts

**[SPEC]** Rust allocation goes through the global allocator unless a custom `GlobalAlloc` / allocator API is used (see current stable docs for `Allocator` traits in your toolchain). Sources: Rust `alloc` / `GlobalAlloc` documentation (pin in project if non-default).

**[IMPLEMENTATION]** `Vec`/`Box` allocation behavior is defined at API level; allocator underneath is swappable at build/runtime per project setup.

## Decision questions

- Is allocation **measurable** on the critical path (profile)?
- Count, size distribution, lifetimes?
- Which **allocator** is actually linked (system, mimalloc, jemalloc, arena — document in project)?
- Do pools add retention, synchronization, or complexity?

## Engineering guidance

**[HEURISTIC]** Reduce allocation **count** on hot paths when profile shows alloc cost — then remeasure.

**[HEURISTIC]** Pools/arenas when size classes and lifetimes are stable — evaluate memory retention and thread synchronization costs.

**[HEURISTIC]** Pass buffers in/out instead of allocating returns when API allows — clarity and alloc count trade-offs.

**[HEURISTIC]** Switching global allocator is **IMPLEMENTATION-specific** — follow that allocator’s docs; require benchmark on **your** binary.

## Evidence required

**[EMPIRICAL]** Allocators flame graph / DHAT / heap profiling; p50/p99 before/after on load test.

## Accept / reject

**Accept** when alloc metrics improve or change deferred with proof path is cold.

**Reject** treating heuristics as laws (“never allocate in loop”) without profile.

## Sources

- RUST-STD-VEC
- RUST-CARGO-PROFILES (for build-linked behavior context)
