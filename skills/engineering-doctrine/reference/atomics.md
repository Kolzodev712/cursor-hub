# Atomics

## Trigger

Lock-free structures, flags, refcounts, or cross-thread counters.

## Questions

- Required ordering: relaxed vs acquire/release vs seq_cst?
- ABA or reclamation hazards?
- Is a lock simpler and fast enough at this contention level?

## Reasoning

- Use the **weakest order** that preserves invariants; seq_cst by default is a smell.
- Prefer proven algorithms or libraries over bespoke lock-free.

## Evidence

Litmus tests where applicable; contention benchmarks vs mutex baseline.

## Accept when

Ordering documented per field/operation and tests cover interleavings you rely on.
