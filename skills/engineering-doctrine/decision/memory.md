# Decision domain — memory locality and cache coherence

## Epistemic status

Verified: 2026-10-05 · Scope: access patterns + multicore sharing · Classes: IMPLEMENTATION, EMPIRICAL, HEURISTIC, POLICY

## Questions before any technique

- Access pattern: sequential, strided, random, pointer-chasing?
- Working set vs cache hierarchy (**from project machine facts**, not assumed line sizes)?
- Multicore: independent hot writes to nearby fields/ counters?
- Memory-bound vs compute-bound (counters + profile)?

## Established facts

**[IMPLEMENTATION]** Caches and coherence exist; false sharing is a **measurable** coherence-line phenomenon on Linux (tools such as perf family). Sources: LINUX-FALSE-SHARING, LINUX-PERF, vendor manuals when CPU scoped in project.

**[POLICY]** **Cache-line size is not universal doctrine** — record in `.cursor/doctrine/workload.md` for verified deployment targets.

## Possible next investigations

- Memory-bound sequential work → improve predictability / working set before instruction tweaks (**data-layout**).
- Scaling fails across cores → measure **false sharing**; separation/padding only if observed (EMPIRICAL trade-off).
- Prefetch / huge pages / NUMA → **technique** candidates **after** gap analysis and authoritative research — not default menu.

## Evidence

**[POLICY]** observation (misses, c2c) → hypothesis → intervention → remeasure.

## Sources

- LINUX-PERF
- LINUX-FALSE-SHARING
- INTEL-OPT-MANUAL
- AMD-ZEN4-OPT
