# CPU caches

## Trigger

Multithreaded scaling fails, or single-thread perf stalls despite low instruction count.

## Questions

- False sharing on mutable counters or flags?
- Line size (typically 64 B) and cross-core writes?
- Read-mostly vs write-heavy shared state?

## Reasoning

- Separate hot mutable fields per thread; align contended atomics.
- Prefer immutable snapshots for cross-thread read paths when write rate is low.

## Evidence

`perf c2c` or equivalent false-sharing analysis; scaling curve vs core count.

## Accept when

Contention hypothesis confirmed or ruled out with measurement.
