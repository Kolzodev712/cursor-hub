# Doctrine source audit (authoring artifact)

**Not installed** into target projects. Records the 2026-10-05 epistemic hardening pass.

**Corpus status:** **PARTIALLY SOURCE-AUDITED** — structural registry and major corrections applied; vendor manual revisions and project-specific protocols remain maintainer-verified over time.

**Knowledge layout (2026-10-05):** Flat `reference/` removed. Content lives under `decision/` (problem routing), optional `techniques/` (mechanisms), `platforms/` (conditional). See [engineering-doctrine.md](engineering-doctrine.md).

## Summary

| Metric | Count |
|--------|------:|
| Reference files rewritten | 11 |
| Registry entries (SOURCES.md) | 20 |
| Claims removed as authoritative | 8+ (see below) |
| Claims reclassified HEURISTIC/POLICY | 15+ |
| UNRESOLVED left in runtime | 0 (portable SIMD stability pinned to “check toolchain”) |

## Claim audit table (high-signal)

| File | Claim (prior) | Class (now) | Source | Verdict | Action |
|------|---------------|-------------|--------|---------|--------|
| atomics.md | Weakest order; SeqCst smell | HEURISTIC/POLICY | RUST-NOMICON-ATOMICS | REWORD | Prefer SeqCst when unsure; weaken only with proof |
| simd.md | Aligned+contiguous prerequisite | — | LLVM-VECTORIZERS | REMOVE | Not universal |
| simd.md | Auto-vec with -O3/LTO | IMPLEMENTATION | LLVM-VECTORIZERS, RUST-CARGO-PROFILES | REWORD | Vectorizers default; LTO separate |
| cpu-caches.md | Line size typically 64 B | — | — | REMOVE | Project/workload facts |
| data-layout.md | SoA/AoS rules | HEURISTIC | INTEL-OPT-MANUAL (scoped) | RECLASSIFY | Evaluate + measure |
| algorithm-selection.md | Perfect hashing/interning default path | HEURISTIC | — | REWORD | Specialized only |
| allocation.md | Remove allocs before allocator swap | HEURISTIC | — | RECLASSIFY | Profile-first |
| concurrency.md | Bounded queues always | HEURISTIC/POLICY | — | RECLASSIFY | Runtime-specific |
| networking.md | Length-prefixed frames | — | — | REMOVE | Protocol-spec first |
| networking.md | Batch when syscall dominates | HEURISTIC | — | RECLASSIFY | Measure + latency check |
| benchmarking.md | Same hardware as production | POLICY | — | REWORD | Environment appropriate to claim |
| memory-locality.md | Sequential before uops | HEURISTIC | vendor scoped | RECLASSIFY | Measure |

## Most important corrections

### SIMD

- **Before:** Alignment/contiguity and `-O3`/LTO framed as gates.
- **After:** LLVM vectorizers on by default with **cost model**; alignment not universal prerequisite; decision path ends in **target-hardware** benchmark.

### Atomics

- **Before:** “Weakest order” / SeqCst as smell.
- **After:** Matches Nomicon — **SeqCst when unsure**; weakening requires synchronization argument; benchmarks ≠ correctness proof.

### Cache-line assumptions

- **Before:** Generic 64 B line.
- **After:** Cache-line size/topology in **project workload**; padding only with observation (e.g. perf c2c) and remeasure.

### Rust data layout

- **Before:** Implicit declaration order / SoA faster.
- **After:** `repr(Rust)` field order not guaranteed (RUST-REF-TYPE-LAYOUT); `Vec` contiguous (SPEC); SoA/AoS **EMPIRICAL**.

### Algorithm choice

- **Before:** HashMap after ruling out perfect hashing.
- **After:** Complexity from std docs; constant-factor wins require measurement; interning/perfect hashing niche.

### Benchmark interpretation

- **Before:** Implied production machine required.
- **After:** Tiered benchmarks; perf counters → **hypothesis**, not fix proof.

## Validation added

- `tools/validate_doctrine_sources.py` — structure only (no network).

## Maintainer workflow

1. Edit reference + SOURCES.md together.
2. Run `python3 tools/validate_doctrine_sources.py`.
3. Update `Verified:` dates when re-checking URLs/scopes.
