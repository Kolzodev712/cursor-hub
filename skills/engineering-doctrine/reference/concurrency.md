# Concurrency

## Trigger

Parallelism, async, or shared mutable state enters the design.

## Questions

- Is the problem **embarrassingly parallel** or coordination-bound?
- Invariants across threads — what must be atomic?
- Latency vs throughput goal?
- Failure modes: partial progress, cancellation?

## Reasoning

- Start with **ownership** (one writer) before locks.
- Match model to runtime (OS threads vs async tasks) using project architecture constraints.
- Prefer bounded queues and backpressure over unbounded buffering.

## Evidence

Stress tests, deadlock/livelock review, saturation behavior under load.

## Accept when

Model matches invariants and load test shows required SLO or explicit gap documented.
