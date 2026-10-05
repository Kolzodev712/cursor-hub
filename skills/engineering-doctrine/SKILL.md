---
name: engineering-doctrine
description: >-
  Decision router for systems engineering — algorithms, memory, concurrency, SIMD,
  I/O, benchmarking, and evidence. Use when choosing representations, optimizing hot
  paths, designing concurrency, or claiming performance. Load only the reference
  files relevant to the current decision.
---

# Engineering doctrine (decision router)

## When to use

- Choosing **data structures / algorithms** for a hot or allocation-sensitive path.
- **Memory layout**, cache behavior, or **allocation** strategy changes.
- **Concurrency**, atomics, or cross-thread sharing.
- **SIMD** or vectorization candidates.
- **Networking / serialization** on critical paths.
- Any **performance or scalability claim** — pair with evidence requirements.

## Decision hierarchy (reminder)

Project `.cursor/doctrine/` objectives → invariants → architecture → workload **override** generic doctrine.

## Router — pick **one or two** references, read them, apply to the decision

| Trigger | Read |
|---------|------|
| Choosing map vs array vs tree; hash vs sort; batching | [reference/algorithm-selection.md](reference/algorithm-selection.md) |
| Struct layout, SoA vs AoS, indirection, padding | [reference/data-layout.md](reference/data-layout.md) |
| Sequential access, prefetch, working set size | [reference/memory-locality.md](reference/memory-locality.md) |
| L1/L2 misses, false sharing, line size awareness | [reference/cpu-caches.md](reference/cpu-caches.md) |
| Heap churn, pools, stack buffers, amortization | [reference/allocation.md](reference/allocation.md) |
| Threads, locks, channels, lock-free, ordering | [reference/concurrency.md](reference/concurrency.md) |
| Atomic RMW, memory order, fences | [reference/atomics.md](reference/atomics.md) |
| Auto-vectorization vs intrinsics, portability | [reference/simd.md](reference/simd.md) |
| Framing, copies, parsing on wire/disk | [reference/networking-serialization.md](reference/networking-serialization.md) |
| Microbench, regression, profiling discipline | [reference/benchmarking.md](reference/benchmarking.md) |
| What proof is required before merging | [reference/evidence-requirements.md](reference/evidence-requirements.md) |

Do **not** load all references for every task. Stop after the decision is justified or blocked on missing workload facts — then read project `workload.md` or ask.

## Output shape for engineering decisions

State: **trigger → questions answered → options → chosen approach → exceptions → verification plan → accept/reject criteria**.
