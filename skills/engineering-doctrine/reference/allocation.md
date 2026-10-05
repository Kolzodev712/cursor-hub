# Allocation

## Trigger

Allocator time or GC pressure appears in profile; latency spikes correlate with churn.

## Questions

- Object lifetime: scoped, pooled, or global?
- Size distribution of allocations?
- Can stack or arena cover a request/work unit?

## Reasoning

- Remove allocations from inner loops before switching allocators.
- Pool when size classes stable and reuse is clear; avoid unbounded pool growth.
- Prefer passing buffers in/out over allocating return values on hot paths.

## Exceptions

Cold paths and one-time setup — clarity over pools.

## Evidence

Allocator flame graph or GC stats; before/after latency percentiles on load test.

## Accept when

Allocation count or bytes/op measurably drops or change deferred with documented non-hot path.
