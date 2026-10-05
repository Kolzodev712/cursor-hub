# Decision domain — data layout

## Epistemic status

Verified: 2026-10-05 · Scope: struct/buffer representation · Classes: SPEC, EMPIRICAL, HEURISTIC

## Questions before any technique

- Which fields are accessed **together** in the hot loop?
- FFI/on-disk/API layout guarantees required (`repr`)?
- Is the limiter **memory traffic**, **false sharing**, or **compute** (profile)?
- What does project **workload** say about record count and access pattern?

## Established facts

**[SPEC]** `repr(Rust)` does **not** guarantee source field order; `Vec<T>` is contiguous per API docs. Source: RUST-REF-TYPE-LAYOUT, RUST-STD-VEC.

## Possible next investigations

- Repeated scan of one field across many records → evaluate **SoA vs AoS** (EMPIRICAL — see **memory** domain).
- Cross-thread hot writes → **memory** domain (coherence / false sharing).
- Pointer chasing → indices into contiguous buffers if invariants allow.

## Evidence

**[EMPIRICAL]** Layout changes require before/after measurement on representative sizes.

## Sources

- RUST-REF-TYPE-LAYOUT
- RUST-STD-VEC
