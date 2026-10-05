# Technique — SIMD and vectorization

## Parent decision domain

cpu-execution

## Epistemic status

Verified: 2026-10-05 · Scope: mechanism options after cpu-execution routing · Classes: IMPLEMENTATION, HEURISTIC, EMPIRICAL, POLICY

Load this file **only when** decision/cpu-execution.md establishes a hot, compute-relevant path with plausible data parallelism.

## Mechanisms (not recommendations)

**[IMPLEMENTATION: LLVM]** Loop and SLP vectorizers enabled by default; profitability/cost model; diagnostics available. Source: LLVM-VECTORIZERS.

**[IMPLEMENTATION: Rust]** `std::arch` intrinsics; `#[target_feature]` rules. Sources: RUST-STD-ARCH, RUST-REF-TARGET-FEATURE.

**[IMPLEMENTATION]** `opt-level` vs **LTO** are separate Cargo profile controls. Sources: RUST-CARGO-PROFILES, RUST-RUSTC-CODEGEN.

**[HEURISTIC]** Typical sequence: inspect auto-vectorization → scalar baseline benchmark → explicit intrinsics/dispatch if justified → fallback path tested.

**[EMPIRICAL]** “Manual SIMD wins” is never generic doctrine.

## Platform scope

CPU feature sets (AVX2, NEON, etc.) belong in **project workload** + vendor manuals — not loaded unless deployment target known.

## Evidence

Vectorization reports/asm; `black_box` in microbenches when needed (RUST-STD-HINT-BLACK-BOX).

## Sources

- LLVM-VECTORIZERS
- RUST-STD-ARCH
- RUST-REF-TARGET-FEATURE
- RUST-CARGO-PROFILES
- RUST-RUSTC-CODEGEN
- RUST-STD-HINT-BLACK-BOX
