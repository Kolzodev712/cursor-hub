# Engineering Doctrine Sources

Authoritative registry for **generic** engineering-doctrine claims. Target-project facts live in `.cursor/doctrine/`. Claim classes: **SPEC**, **IMPLEMENTATION**, **EMPIRICAL**, **HEURISTIC**, **POLICY**.

**Verified date** on each entry is when a maintainer last confirmed the URL and scope against the claim set in this repo (not live CI).

---

## RUST-REF-MEMORY-MODEL

Authority: Tier A (partial — model explicitly incomplete)  
Publisher: Rust Project  
Document: The Rust Reference — Introduction (memory model)  
Scope: Rust’s documented memory-model status; not a complete formal spec  
Status: Current stable docs  
Verified: 2026-10-05  
URL: https://doc.rust-lang.org/reference/introduction.html  

Supports:

- Rust inherits C++20 atomics/memory-order concepts in practice (see also Nomicon)
- Overall memory model remains subject to change; do not claim stronger formal guarantees than the Reference documents

Does not establish:

- A complete happens-before proof procedure for arbitrary code
- That any particular `Ordering` choice is optimal for performance

---

## RUST-REF-TYPE-LAYOUT

Authority: Tier A  
Publisher: Rust Project  
Document: The Rust Reference — Type layout  
Scope: `repr`, alignment, field layout guarantees  
Verified: 2026-10-05  
URL: https://doc.rust-lang.org/reference/type-layout.html  

Supports:

- Default `repr(Rust)` does **not** guarantee source declaration order of fields in memory
- `repr(C)`, `repr(align)`, `repr(packed)` semantics as documented
- Size/align rules for arrays, slices, pointers as documented

Does not establish:

- That any particular struct layout is optimal for cache performance (EMPIRICAL)

---

## RUST-REF-TARGET-FEATURE

Authority: Tier A  
Publisher: Rust Project  
Document: The Rust Reference — Conditional compilation / `target_feature`  
Scope: `#[target_feature]`, `cfg(target_feature = "...")`  
Verified: 2026-10-05  
URL: https://doc.rust-lang.org/reference/attributes/codegen.html#the-target_feature-attribute  

Supports:

- Rules for marking functions with target features; safety obligations for callers

Does not establish:

- That a loop will vectorize or that intrinsics are faster on your hardware

---

## RUST-STD-ATOMICS

Authority: Tier A  
Publisher: Rust Project  
Document: `std::sync::atomic` — `Ordering` and atomic operations  
Scope: Rust std atomic API and documented ordering names  
Verified: 2026-10-05  
URL: https://doc.rust-lang.org/std/sync/atomic/enum.Ordering.html  

Supports:

- Definitions of `Relaxed`, `Acquire`, `Release`, `AcqRel`, `SeqCst` as API contracts
- Which operations accept which orderings

Does not establish:

- Weakest correct ordering for your algorithm (correctness reasoning required)
- Performance ranking of orderings on your CPU (EMPIRICAL)

---

## RUST-NOMICON-ATOMICS

Authority: Tier B (explanatory; defers to spec/std for normative detail)  
Publisher: Rust Project  
Document: The Rustonomicon — Atomics  
Scope: Intuition for compiler/hardware reordering; ordering choice guidance  
Verified: 2026-10-05  
URL: https://doc.rust-lang.org/nomicon/atomics.html  

Supports:

- SeqCst is simpler to reason about; **if not confident about other orders, SeqCst is the right default** (Nomicon)
- Weaker orderings may be cheaper on weakly ordered hardware; correctness must be argued
- Data races require synchronization via atomics (not data races alone)

Does not establish:

- That Relaxed is always safe when “only a counter”
- Formal verification of lock-free algorithms

---

## RUST-STD-VEC

Authority: Tier A  
Publisher: Rust Project  
Document: `std::vec::Vec`  
Scope: Contiguous buffer semantics for `Vec<T>`  
Verified: 2026-10-05  
URL: https://doc.rust-lang.org/std/vec/struct.Vec.html  

Supports:

- `Vec` stores elements in a contiguous buffer (as documented)
- Capacity/length/growth behavior at API level

Does not establish:

- `Vec` is faster than `HashMap` for your workload (EMPIRICAL)

---

## RUST-STD-COLLECTIONS

Authority: Tier A  
Publisher: Rust Project  
Document: `std::collections` — module documentation  
Scope: Collection trait costs overview  
Verified: 2026-10-05  
URL: https://doc.rust-lang.org/std/collections/index.html  

Supports:

- Documented high-level complexity characteristics of std collections module

Does not establish:

- Constant-factor dominance on real hardware for your N and key type

---

## RUST-STD-HASHMAP

Authority: Tier A / IMPLEMENTATION  
Publisher: Rust Project  
Document: `std::collections::HashMap`  
Scope: Current std `HashMap` API and **documented implementation notes** (may change)  
Verified: 2026-10-05  
URL: https://doc.rust-lang.org/std/collections/struct.HashMap.html  

Supports:

- API semantics (insert, lookup, hasher requirements)
- Current implementation strategy described in std docs (treat as IMPLEMENTATION, not eternal guarantee)

Does not establish:

- HashMap beats Vec/BTreeMap for small N or sparse keys (EMPIRICAL)

---

## RUST-STD-BTREEMAP

Authority: Tier A  
Publisher: Rust Project  
Document: `std::collections::BTreeMap`  
Scope: Ordered map API and documented complexity  
Verified: 2026-10-05  
URL: https://doc.rust-lang.org/std/collections/struct.BTreeMap.html  

Supports:

- Logarithmic lookup/insert in size as documented
- Iteration in key order

Does not establish:

- BTreeMap vs HashMap winner for your access pattern (EMPIRICAL)

---

## RUST-STD-ARCH

Authority: Tier A  
Publisher: Rust Project  
Document: `std::arch`  
Scope: Platform intrinsics modules  
Verified: 2026-10-05  
URL: https://doc.rust-lang.org/std/arch/index.html  

Supports:

- Intrinsics are platform-specific and unsafe at call sites where documented

Does not establish:

- Portable SIMD replacement; auto-vectorization behavior

---

## RUST-STD-HINT-BLACK-BOX

Authority: Tier A  
Publisher: Rust Project  
Document: `std::hint::black_box`  
Scope: Preventing certain optimizations in benchmarks  
Verified: 2026-10-05  
URL: https://doc.rust-lang.org/std/hint/fn.black_box.html  

Supports:

- Using `black_box` to inhibit compile-time elimination in microbenchmarks

Does not establish:

- That a microbenchmark models production

---

## RUST-CARGO-PROFILES

Authority: Tier A  
Publisher: Rust Project  
Document: The Cargo Book — Profiles  
Scope: `opt-level`, LTO settings, debug info  
Verified: 2026-10-05  
URL: https://doc.rust-lang.org/cargo/reference/profiles.html  

Supports:

- Optimization level and LTO are **separate** profile controls
- Release vs dev defaults

Does not establish:

- That `-O3` or LTO is required for LLVM loop vectorization (vectorizers are enabled by default in LLVM; see LLVM-VECTORIZERS)

---

## RUST-RUSTC-CODEGEN

Authority: Tier B  
Publisher: Rust Project  
Document: rustc — Codegen options  
Scope: `-C target-feature`, `-C opt-level`, etc.  
Verified: 2026-10-05  
URL: https://doc.rust-lang.org/rustc/codegen-options/index.html  

Supports:

- How to pass target features and optimization flags to LLVM backend

Does not establish:

- Exact vectorization outcome for a given crate

---

## LLVM-VECTORIZERS

Authority: Tier B  
Publisher: LLVM Project  
Document: Auto-Vectorization in LLVM  
Scope: Loop and SLP vectorizers, cost model, diagnostics  
Verified: 2026-10-05  
URL: https://llvm.org/docs/Vectorizers.html  

Supports:

- Loop and SLP vectorizers exist and are **enabled by default**
- Vectorization uses profitability/cost analysis; many loops fail to vectorize (control flow, types, calls)
- Gather/scatter and mixed patterns may vectorize but cost model may reject
- Vectorization diagnostics flags (`-Rpass=loop-vectorize`, etc.)

Does not establish:

- That **your** Rust/LLVM build vectorizes a specific loop
- That vectorized code is faster on deployment hardware (EMPIRICAL)
- Alignment/contiguity as strict prerequisites for all vectorization

---

## INTEL-OPT-MANUAL

Authority: Tier B  
Publisher: Intel  
Document: Intel® 64 and IA-32 Architectures Optimization Reference Manual  
Scope: x86/x86-64 microarchitectural optimization guidance (version-specific)  
Status: Vendor manual — verify revision for your CPU  
Verified: 2026-10-05  
URL: https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html  

Supports:

- Mechanisms: caches, prefetch, alignment considerations on Intel cores (scoped to Intel uarch)

Does not establish:

- Same behavior on AMD ARM, or all x86 CPUs
- Application speedups without measurement

---

## AMD-ZEN4-OPT

Authority: Tier B  
Publisher: AMD  
Document: Software Optimization Guide for AMD Zen 4 (publication 57647)  
Scope: Zen 4–specific tuning (verify document revision)  
Verified: 2026-10-05  
URL: https://www.amd.com/en/search/documentation-hub.html  

Supports:

- Zen-family-specific guidance when Zen 4 is the **verified** deployment target

Does not establish:

- Generic cache-line size for all architectures
- Claims for non-Zen hardware

---

## AMD64-ARCH-MANUAL

Authority: Tier A (ISA)  
Publisher: AMD  
Document: AMD64 Architecture Programmer’s Manual  
Scope: ISA-level semantics for AMD64  
Verified: 2026-10-05  
URL: https://www.amd.com/en/search/documentation-hub.html  

Supports:

- ISA semantics where relevant to atomics/memory fences at hardware level (with Rust abstract machine on top)

Does not establish:

- Rust `Ordering` mapping without Rust std/Nomicon

---

## LINUX-FALSE-SHARING

Authority: Tier B  
Publisher: Linux kernel documentation  
Document: Kernel docs — performance / cache effects (false sharing discussions in perf tooling context)  
Scope: Linux tooling and kernel guidance on sharing cache lines  
Verified: 2026-10-05  
URL: https://docs.kernel.org/admin-guide/mm/index.html  

Supports:

- False sharing as a measurable coherence/cache-line phenomenon on Linux systems
- Investigation often uses perf-family tools (see LINUX-PERF)

Does not establish:

- Universal 64-byte line size on all hardware
- That padding fixes your bottleneck (EMPIRICAL)

---

## LINUX-PERF

Authority: Tier B  
Publisher: Linux  
Document: `perf` tool documentation (including c2c where available)  
Scope: Profiling and cache-coherence analysis on Linux  
Verified: 2026-10-05  
URL: https://www.kernel.org/doc/html/latest/admin-guide/perf/index.html  

Supports:

- perf can sample events and support cache-related analysis workflows
- `perf c2c` (when built/supported) helps locate false sharing

Does not establish:

- Causal proof that a code change fixes the limiter (observation → hypothesis → experiment)

---

## MARA-BOS-ATOMICS

Authority: Tier D (expert secondary; defers to Rust std/Reference)  
Publisher: Mara Bos  
Document: Rust Atomics and Locks  
Scope: Explanatory text for Rust atomics and common patterns  
Verified: 2026-10-05  
URL: https://marabos.nl/atomics/  

Supports:

- Pedagogy for memory orders, mutexes, and lock-free patterns

Does not establish:

- Normative semantics beyond Rust documentation
- Weakest ordering prescriptions without correctness proof

---

## POLICY-CURSOR-HUB-EVIDENCE

Authority: Tier — **POLICY** (cursor-hub)  
Publisher: cursor-hub  
Document: `reference/evidence-requirements.md`  
Scope: Agent behavior for performance claims in projects using this hub  
Verified: 2026-10-05  
URL: (in-repo) `skills/engineering-doctrine/reference/evidence-requirements.md`  

Supports:

- Require measurement before claiming improvement
- Project doctrine overrides generic optimization preferences

Does not establish:

- External technical truth about CPUs or compilers
