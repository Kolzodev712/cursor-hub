# Data layout

## Trigger

Hot loop touches many fields or many records; cache misses dominate.

## Questions

- Which fields are read together in the hot loop?
- Record count fixed at compile time vs runtime?
- Mutation vs mostly read-only?
- Cross-language / FFI boundary layout constraints?

## Reasoning

- **SoA** when iterating one field across many elements; **AoS** when processing whole records together.
- Reduce pointer chasing: prefer inline storage or indices into contiguous buffers.
- Pad to avoid false sharing only when measured contention on cache lines.

## Exceptions

API stability or serde/schema compatibility may force suboptimal layout — document trade-off.

## Evidence

Cache miss counters or `perf` / equivalent on representative input sizes.

## Accept when

Layout change is tied to a measured bottleneck or explicit future hot-path plan with invariants preserved.
