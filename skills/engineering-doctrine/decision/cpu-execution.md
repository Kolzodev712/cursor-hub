# Decision domain — CPU execution and vectorization

## Epistemic status

Verified: 2026-10-05 · Scope: compute vs other limiters; when SIMD/codegen matters · Classes: HEURISTIC, EMPIRICAL, IMPLEMENTATION, POLICY

## Questions before any technique

- Is the path **hot** and **compute-bound** (profile — not guess)?
- What limits it: ALU, branches, memory bandwidth, calls, sync?
- Is there **independent work per lane** (data parallelism)?
- What does **current generated code** do (asm, LLVM remarks — toolchain-specific)?
- What **CPU features** does deployment guarantee (project `workload.md`)?

## Codegen chain (recognition, not encyclopedia)

```text
source → rustc → LLVM → machine code → CPU
```

Inlining, monomorphization, bounds checks, vectorization, and LTO are **separate** levers (Cargo profiles vs LLVM passes). Do not treat “enable LTO” as a substitute for identifying the limiter.

**Future candidate domain (not in corpus):** dedicated `compiler-codegen` if recurring routing failures appear in real projects.

## Possible next investigations

- Compute-bound + data parallelism → load **techniques/simd.md** only after above questions answered.
- Branch/call bound → algorithm/structure before SIMD.
- Memory bound → **memory** / **data-layout** domains first.

## Knowledge gap examples

**[POLICY]** AVX2 on Zen 4, Tokio wake semantics, PGO on your CI profile → declare **KNOWLEDGE GAP**, consult authoritative source, scope IMPLEMENTATION — do not invent.

## Evidence

**[EMPIRICAL]** Scalar baseline + candidate on representative target hardware; compiler diagnostics documented.

## Sources

- LLVM-VECTORIZERS
- RUST-CARGO-PROFILES
- RUST-RUSTC-CODEGEN
