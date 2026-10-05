# Memory locality

## Epistemic status

Verified: 2026-10-05  
Scope: Access-pattern reasoning; not a substitute for profiling.  
Claim classes: IMPLEMENTATION, EMPIRICAL, HEURISTIC

## Trigger

Profile/memory counters suggest bandwidth or cache misses; strided/random access in hot path.

## Established facts

**[IMPLEMENTATION]** CPU memory hierarchies reward predictable access; sequential scans often hit cache lines efficiently — **until** working set exceeds cache capacity (hardware-specific). Sources: INTEL-OPT-MANUAL, AMD-ZEN4-OPT (scoped).

**[IMPLEMENTATION]** Prefetch instructions/hardware prefetchers may hide latency but **do not remove bandwidth limits**. Sources: vendor optimization manuals (scoped).

## Decision questions

- Access pattern: sequential, strided, random, pointer-chasing?
- Working set size vs last-level cache (from **project** machine facts)?
- Allocator-induced scatter (see allocation.md)?

## Engineering guidance

**[HEURISTIC]** When memory-bound, improve access predictability and working-set size before instruction-level tweaks — **verify** with counters.

**[HEURISTIC]** Split cold metadata from hot arrays when profile shows mixed access.

**[HEURISTIC]** Prefetch only after layout/access pattern is understood; measure on target.

## Evidence required

**[EMPIRICAL]** LLC miss rate, bandwidth counters, or allocator profiles — then intervention + remeasure.

## Observation → intervention

**[POLICY]** A miss counter or flamegraph hotspot **hypothesizes** a limiter; it does not prove a specific representation change will help until A/B measured.

## Accept / reject

**Accept** when access-pattern story matches **measurement** or change is rejected with evidence memory is not the limiter.

## Sources

- INTEL-OPT-MANUAL
- AMD-ZEN4-OPT
- LINUX-PERF
