---
name: engineering-doctrine
description: >-
  Layered engineering doctrine: decision domains, optional techniques/platforms,
  project facts, evidence. Routes minimal verified context; escalates knowledge gaps.
  Use for representation, hot paths, concurrency, performance claims — not trivial edits.
---

# Engineering doctrine — router

## Corpus is intentionally incomplete

Local doctrine provides **verified decision frameworks**, not exhaustive engineering knowledge. Missing technique/platform files → **research or measure**, not model-memory authority. See [decision/evidence.md](decision/evidence.md).

## Layer model

```text
Core policy (ambient rule + this router)
  → decision/     (what kind of problem?)
  → techniques/   (optional mechanisms — load only if candidate)
  → platforms/    (conditional — project toolchain/CPU)
  → .cursor/doctrine/  (project facts)
  → measurement
```

Provenance: [SOURCES.md](SOURCES.md) (maintainers; do not load entire file for every task).

## Routing procedure

1. **DOMAIN_IDENTIFIED** — pick **one** primary decision file (at most **two** if tightly coupled, e.g. algorithm-selection + data-layout).
2. **PROJECT_FACTS_MISSING** — read `.cursor/doctrine/` objectives/invariants/workload as needed; stop if blocked.
3. **LOCAL_KNOWLEDGE_SUFFICIENT** — answer with decision questions + established SPEC/IMPLEMENTATION facts only.
4. **TECHNIQUE_INVESTIGATION_REQUIRED** — load **one** `techniques/*.md` named by decision “Possible next investigations”.
5. **PLATFORM_KNOWLEDGE_REQUIRED** — consult SOURCES + authoritative docs; scope IMPLEMENTATION to project CPU/toolchain.
6. **EXTERNAL_RESEARCH_REQUIRED** — declare **KNOWLEDGE GAP** (missing fact, why it matters, authority to consult); no fabrication.
7. **MEASUREMENT_REQUIRED** — EMPIRICAL claims need benchmark/profile tier from decision/benchmarking.md.
8. **DECISION_READY** — options, policy checks, verification plan, accept/reject.

**Context rule:** never load `techniques/` or `platforms/` catalogs up front.

## Knowledge boundary (policy)

If verified local doctrine does not cover a required fact, **do not** state it as established. Form hypotheses, research authoritative sources (see SOURCES tiers), classify scope, or mark the decision **blocked/conditional**.

## Decision domain index

| If the decision is about… | Load |
|---------------------------|------|
| Map/vec/tree, hash vs sort | [decision/algorithm-selection.md](decision/algorithm-selection.md) |
| Struct layout, repr, SoA/AoS question | [decision/data-layout.md](decision/data-layout.md) |
| Bandwidth, working set, false sharing | [decision/memory.md](decision/memory.md) |
| Heap churn, pools, allocator | [decision/allocation.md](decision/allocation.md) |
| Threads, queues, tasks | [decision/concurrency.md](decision/concurrency.md) |
| Memory orders, atomics | [decision/atomics.md](decision/atomics.md) |
| Compute-bound, vectorization, codegen | [decision/cpu-execution.md](decision/cpu-execution.md) |
| Wire format, parse, I/O path | [decision/io.md](decision/io.md) |
| Benchmarks, profiles | [decision/benchmarking.md](decision/benchmarking.md) |
| Claims, evidence, gaps | [decision/evidence.md](decision/evidence.md) |

## Technique index (load only when routed)

| Technique file | After domain |
|----------------|--------------|
| [techniques/simd.md](techniques/simd.md) | cpu-execution |

See [techniques/README.md](techniques/README.md).

## Future candidate domains (not in corpus)

- `compiler-codegen` (if codegen routing fails repeatedly)
- `latency-throughput` / scheduling-backpressure (if concurrency+benchmarking insufficient in trading-system experiment)

## Output shape

Trigger → routing state → decision questions → (optional technique/platform) → evidence plan → accept/reject.
