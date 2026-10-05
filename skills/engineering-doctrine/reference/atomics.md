# Atomics

## Epistemic status

Verified: 2026-10-05  
Scope: Generic Rust atomics / memory orders (not a specific lock-free algorithm).  
Claim classes: SPEC, IMPLEMENTATION, HEURISTIC, EMPIRICAL, POLICY

## Trigger

Cross-thread synchronization via `std::sync::atomic`, lock-free structures, flags, refcounts, or ordering changes on shared atomics.

## Established facts

**[SPEC]** Rust exposes `Ordering::{Relaxed, Acquire, Release, AcqRel, SeqCst}` on atomic operations; each operation documents which orderings are valid. Source: RUST-STD-ATOMICS.

**[SPEC / IMPLEMENTATION]** Rust’s atomics model is aligned with the C++20 atomics model in practice; the Reference notes the overall Rust memory model is still evolving — do not claim complete formal coverage beyond documented material. Sources: RUST-REF-MEMORY-MODEL, RUST-NOMICON-ATOMICS.

**[HEURISTIC — Nomicon]** Sequential consistency is the **simplest** ordering to reason about. If you are **not confident** a weaker ordering is correct, prefer **SeqCst** (or redesign with clearer release/acquire pairing). Weakening orderings later requires a **documented synchronization argument**, not a benchmark alone. Source: RUST-NOMICON-ATOMICS.

**[IMPLEMENTATION]** On strongly ordered CPUs, some orderings may compile to fences differently than on weakly ordered CPUs — performance of orderings is **EMPIRICAL** on the deployment target. Source: RUST-NOMICON-ATOMICS.

## Decision questions

- What **synchronization relationship** must hold (release/acquire pair, publication, counter, lock guard)?
- Can the invariant be expressed with **mutex + data under lock** instead of bespoke atomics?
- For lock-free: what reclamation/ABA/lifetime rules apply (not covered by ordering names alone)?
- If considering weaker orderings: what is the **correctness proof sketch** (happens-before story)?

## Engineering guidance

**[HEURISTIC]** Prefer proven libraries/patterns over inventing lock-free algorithms.

**[HEURISTIC]** Correctness proof **precedes** ordering micro-optimization; benchmarks cannot prove an ordering correct.

**[POLICY]** Do not change `SeqCst` → `Relaxed` for speed without the correctness argument and, if performance is the motive, evidence that ordering cost matters on target hardware.

## Evidence required

**[EMPIRICAL]** Contention/latency comparisons vs mutex baseline — only after correctness is established.

**[EMPIRICAL]** Litmus or concurrency tests for interleavings the design relies on.

## Accept / reject

**Accept** when ordering choice is justified against RUST-STD-ATOMICS semantics, tests cover relied-upon behavior, and any performance-motivated weakening has both proof sketch and measurement.

**Reject** “Relaxed is faster” without synchronization analysis.

## Sources

- RUST-STD-ATOMICS
- RUST-NOMICON-ATOMICS
- RUST-REF-MEMORY-MODEL
- MARA-BOS-ATOMICS (secondary)
