# Benchmarking

## Trigger

Before/after comparison for an optimization or regression guard.

## Questions

- Same hardware, CPU governor, and background load as production?
- Input distribution matches `workload.md`?
- Warmup sufficient? Variance across runs?

## Reasoning

- Benchmark the **smallest unit** that still includes real dependencies.
- Report distribution (p50/p99), not single runs.
- Pin versions and disable unrelated logging in microbench.

## Evidence

Stored results or CI benchmark job with thresholds.

## Accept when

Methodology documented and numbers reproducible within stated variance.
