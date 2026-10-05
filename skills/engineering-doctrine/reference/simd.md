# SIMD

## Trigger

Numeric hot loop with independent lanes and stable types.

## Questions

- Is data aligned and contiguous?
- Is portability required across CPU features?
- Does compiler auto-vectorize with `-O3`/LTO already?

## Reasoning

- Fix layout and aliasing before intrinsics.
- Use runtime dispatch when baseline CPU feature set is mixed.
- Scalar fallback must remain correct and tested.

## Evidence

Assembly or vectorization report; correctness tests on non-SIMD path.

## Accept when

Speedup measured on target hardware or SIMD rejected with auto-vec evidence.
