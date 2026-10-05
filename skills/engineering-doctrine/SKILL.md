---
name: engineering-doctrine
description: >-
  Source-backed decision router for systems engineering — algorithms, memory, concurrency,
  SIMD, I/O, benchmarking, evidence. Use when choosing representations, optimizing hot
  paths, designing concurrency, or claiming performance. Load only references relevant
  to the decision; see SOURCES.md for provenance.
---

# Engineering doctrine (decision router)

## Epistemic model (read once)

| Class | Meaning |
|-------|---------|
| **SPEC** | Language/ISA/protocol spec guarantee |
| **IMPLEMENTATION** | Compiler, std version, CPU family, tool behavior (scoped) |
| **EMPIRICAL** | True only with project measurement |
| **HEURISTIC** | Investigation guide, not a law |
| **POLICY** | cursor-hub / project agent behavior |

Provenance registry: [SOURCES.md](SOURCES.md) (maintainer-facing, not loaded for every task). Performance claims require project evidence ([reference/evidence-requirements.md](reference/evidence-requirements.md)).

**Do not** web-search during normal tasks unless updating doctrine or targeting uncovered hardware/libs.

## When to use

- Representation or **algorithm** choice on a hot or correctness-critical path
- **Layout**, **cache/coherence**, **allocation** changes
- **Concurrency** / **atomics** design
- **SIMD** or vectorization
- **Wire/parse** path changes
- Any **performance claim** → pair with evidence requirements

**Do not use** for trivial renames/comments with no semantic or performance impact.

## Decision hierarchy

Project `.cursor/doctrine/` objectives → invariants → architecture → workload **override** generic doctrine.

## Router — load **one or two** references by decision type

| Decision type | Read |
|---------------|------|
| Map vs vec vs tree; hash vs sort; batching | [algorithm-selection.md](reference/algorithm-selection.md) |
| Struct layout, repr, SoA/AoS (no perf claim yet) | [data-layout.md](reference/data-layout.md) |
| Access pattern / bandwidth / working set | [memory-locality.md](reference/memory-locality.md) |
| False sharing, coherence, scaling across cores | [cpu-caches.md](reference/cpu-caches.md) |
| Heap churn, pools, allocator swap | [allocation.md](reference/allocation.md) |
| Threads, queues, runtime choice | [concurrency.md](reference/concurrency.md) |
| Memory orders, atomics, lock-free | [atomics.md](reference/atomics.md) |
| Auto-vec vs intrinsics vs target features | [simd.md](reference/simd.md) |
| Protocol framing, copies, batching | [networking-serialization.md](reference/networking-serialization.md) |
| Benchmark design / interpreting perf | [benchmarking.md](reference/benchmarking.md) |
| Required proof before claiming “faster” | [evidence-requirements.md](reference/evidence-requirements.md) |

Combine at most **two** references (e.g. algorithm-selection + data-layout for representation change). Stop when blocked on missing **workload.md** facts.

## Output shape

**Trigger → questions → established facts (with class) → options → policy checks → verification plan → accept/reject.**
