# SIMD and auto-vectorization

## Epistemic status

Verified: 2026-10-05  
Scope: Rust + LLVM backend (compiler version dependent).  
Claim classes: IMPLEMENTATION, EMPIRICAL, HEURISTIC, POLICY

## Trigger

Hot numeric or data-parallel loop; manual intrinsics; `#[target_feature]`; question “should we SIMD this?”

## Established facts

**[IMPLEMENTATION: LLVM]** LLVM provides **Loop** and **SLP** vectorizers; both are **enabled by default**. Vectorization uses **profitability/cost** analysis — many loops are skipped (control flow, types, calls, pointer uncertainty). Source: LLVM-VECTORIZERS.

**[IMPLEMENTATION: LLVM]** Vectorization is **not** strictly limited to “aligned + contiguous” loops; gather/scatter and mixed types may vectorize when profitable — or may not. Source: LLVM-VECTORIZERS.

**[IMPLEMENTATION: Rust/Cargo]** Optimization level (`opt-level`) and **LTO** are profile settings in Cargo; LTO is **not** the same switch as “enable vectorization.” Source: RUST-CARGO-PROFILES, LLVM-VECTORIZERS.

**[SPEC]** Platform intrinsics live under `std::arch` and are target-specific; `#[target_feature]` has documented safety rules. Source: RUST-STD-ARCH, RUST-REF-TARGET-FEATURE.

**[IMPLEMENTATION]** Portable SIMD (`std::simd` / `core::simd`) status depends on Rust release — treat as **unstable/experimental** unless your pinned toolchain docs mark it stable. Check current docs before recommending.

## Decision path

1. **[EMPIRICAL]** Is the path **hot** on representative hardware/workload (profile/trace)?
2. **[EMPIRICAL]** What limits the path (CPU compute, memory bandwidth, branches, calls)?
3. **[HEURISTIC]** Is there **independent work per lane** (data parallelism)?
4. **[IMPLEMENTATION]** Can LLVM already vectorize it? (optimization remarks / asm inspection — version-specific.)
5. **[HEURISTIC]** Do aliasing, control flow, or ABI calls block vectorization?
6. **[HEURISTIC]** Are explicit intrinsics/`target_feature` justified only after scalar + auto-vec baseline and **CPU feature deployment** story?
7. **[EMPIRICAL]** Benchmark scalar vs candidate on **representative target hardware** with documented flags/profile.

## Engineering guidance

**[HEURISTIC]** Fix correctness and aliasing before intrinsics; keep scalar fallback tested.

**[HEURISTIC]** Runtime feature detection + dispatch when minimum CPU features vary (see project `workload.md`).

**[POLICY]** Do not rewrite loops with AVX2/NEON because “SIMD is faster” without steps 1–7.

## Evidence required

**[EMPIRICAL]** Vectorization reports or asm diff; benchmark with `black_box` where microbench DCE is a risk (RUST-STD-HINT-BLACK-BOX).

## Accept / reject

**Accept** measured win on deployment-class hardware **or** documented rejection with auto-vec analysis.

**Reject** alignment/contiguity checklists as proof of vectorization or speedup.

## Sources

- LLVM-VECTORIZERS
- RUST-STD-ARCH
- RUST-REF-TARGET-FEATURE
- RUST-CARGO-PROFILES
- RUST-RUSTC-CODEGEN
- RUST-STD-HINT-BLACK-BOX
