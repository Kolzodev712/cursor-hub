# CPU caches and coherence

## Epistemic status

Verified: 2026-10-05  
Scope: Generic mechanisms; **machine-specific numbers come from project doctrine**.  
Claim classes: IMPLEMENTATION, EMPIRICAL, HEURISTIC, POLICY

## Trigger

Multithreaded scaling stalls; suspected false sharing; counter/array contention across cores.

## Established facts

**[IMPLEMENTATION]** Multicore CPUs cache data in hierarchies; writes to the same cache line from different cores can cause **coherence traffic** (often called false sharing when independent variables share a line). Sources: INTEL-OPT-MANUAL, AMD-ZEN4-OPT (when target is known), LINUX-FALSE-SHARING.

**[IMPLEMENTATION]** Linux `perf` and related tools (including **c2c** where available) can help **observe** line contention — observation is not causality. Source: LINUX-PERF.

**[POLICY / project fact]** **Cache-line size is not universal doctrine.** Record line size, topology, and NUMA in `.cursor/doctrine/workload.md` for the **verified deployment** architecture. Do not assume 64 B globally.

## Decision questions

- What is the **verified** machine (CPU family, cores, NUMA)?
- Which **mutable** fields are updated by different threads?
- Is contention **measured** (c2c, scaling curve, hardware counters)?
- Would padding/separation increase memory footprint or complicate layout (EMPIRICAL trade-off)?

## Engineering guidance

**[HEURISTIC]** Separate hot per-thread counters; avoid sharing a cache line for independent hot writes — **after** confirming contention.

**[HEURISTIC]** Immutable snapshots or read-mostly paths when write rate is low (workload-dependent).

**[EMPIRICAL]** Padding/alignment mitigations require before/after measurement — padding can hurt density and bandwidth.

## Evidence required

**[EMPIRICAL]** `perf c2c` or equivalent + scaling benchmark; tie intervention to observed contention.

## Accept / reject

**Accept** when mitigation addresses **measured** sharing/contention on target topology.

**Reject** “pad every atomic to 64 bytes” without architecture facts and observation.

## Architecture-specific

Load INTEL-OPT-MANUAL or AMD-ZEN4-OPT **only when** project doctrine names that deployment CPU.

## Sources

- INTEL-OPT-MANUAL
- AMD-ZEN4-OPT
- AMD64-ARCH-MANUAL
- LINUX-FALSE-SHARING
- LINUX-PERF
