# Data layout

## Epistemic status

Verified: 2026-10-05  
Scope: Rust layout + generic locality reasoning.  
Claim classes: SPEC, EMPIRICAL, HEURISTIC, POLICY

## Trigger

Struct/ buffer representation change; SoA vs AoS question; FFI layout; padding for concurrency.

## Established facts

**[SPEC]** `repr(Rust)` does **not** guarantee field order matches source declaration order; use `repr(C)` / explicit `repr(align)` when layout guarantees are required. Source: RUST-REF-TYPE-LAYOUT.

**[SPEC]** `Vec<T>` stores elements in one contiguous buffer (API documentation). Source: RUST-STD-VEC.

**[EMPIRICAL]** SoA vs AoS performance depends on access pattern, size, hardware, and compiler — vendor manuals discuss locality mechanisms; **“SoA is faster”** is never generic doctrine. Sources: INTEL-OPT-MANUAL (x86 tuning), project measurement.

## Decision questions

- Which fields are accessed together in the **hot loop**?
- Are layout guarantees required for FFI/serialization/on-disk format?
- Does false sharing apply (see cpu-caches.md)?
- What does **profile** show: memory bound vs compute bound?

## Engineering guidance

**[HEURISTIC]** Evaluate SoA when repeatedly scanning one field across many records; evaluate AoS when processing most fields per record — then **measure**.

**[HEURISTIC]** Reduce pointer chasing with indices into contiguous storage when invariants allow.

**[HEURISTIC]** Pad/separate fields for sharing only with measured contention (cpu-caches.md).

## Evidence required

**[EMPIRICAL]** Cache/ bandwidth counters or A/B benchmark on representative sizes from `workload.md`.

## Accept / reject

**Accept** layout change with measured bottleneck link or explicit non-hot-path deferral.

**Reject** declaration-order assumptions under `repr(Rust)` for correctness or performance.

## Sources

- RUST-REF-TYPE-LAYOUT
- RUST-STD-VEC
- INTEL-OPT-MANUAL
- AMD-ZEN4-OPT
