# Memory locality

## Trigger

Profile shows memory-bound behavior or unpredictable latency on sequential work.

## Questions

- Access pattern: sequential, strided, random?
- Working set vs last-level cache size?
- Allocator-induced scatter?

## Reasoning

- Improve **sequential** access before micro-optimizing instructions.
- Split cold metadata from hot arrays.
- Consider prefetch only after layout is sane — prefetch hides latency, not bandwidth limits.

## Evidence

Hardware counters (LLC misses, bandwidth) or allocator profiles.

## Accept when

Access pattern aligns with measured miss profile or change is rejected with workload proof that memory is not the limiter.
