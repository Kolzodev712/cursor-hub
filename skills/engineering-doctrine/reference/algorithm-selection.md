# Algorithm and collection selection

## Epistemic status

Verified: 2026-10-05  
Scope: Rust std collections + generic complexity reasoning.  
Claim classes: SPEC, IMPLEMENTATION, EMPIRICAL, HEURISTIC

## Trigger

Choosing map vs vector vs tree; hash vs sort; batching; hot lookup/insert path.

## Established facts

**[SPEC / IMPLEMENTATION]** `HashMap` documents expected average O(1) lookup/insert at algorithmic level; `BTreeMap` documents O(log n) lookup/insert; module docs summarize collection costs. Sources: RUST-STD-HASHMAP, RUST-STD-BTREEMAP, RUST-STD-COLLECTIONS.

**[SPEC]** `Vec` supports O(1) indexed access when indices are valid. Source: RUST-STD-VEC.

**[EMPIRICAL]** Asymptotic class **does not** prove faster for your N, key type, hash cost, or memory footprint — constants and locality dominate at moderate N.

## Decision questions

- N, growth, **dense vs sparse** key domain?
- Point lookup vs range/ordering requirements?
- Read/write/delete mix; latency vs throughput priority?
- Is the path **actually hot** (profile)?

## Engineering guidance

**[HEURISTIC]** **Dense, small, bounded integer domain:** evaluate direct indexing (`Vec`, bitset) vs hash — compare memory and branch behavior, then benchmark.

**[HEURISTIC]** **Sparse/opaque keys:** `HashMap` is a default **candidate**, not a mandate; consider `BTreeMap` when ordering/range queries are required.

**[HEURISTIC]** Interning / perfect hashing are **specialized** tools — consider only when domain constraints are documented and simpler structures fail measurement.

**[HEURISTIC]** Batch updates when bursts amortize structure maintenance.

## Evidence required

**[EMPIRICAL]** Representative size distribution from `workload.md`; A/B on target hardware; correctness tests.

## Accept / reject

**Accept** when choice matches workload facts **and** measurement (or documented non-hot path).

**Reject** “HashMap is O(1) so always use HashMap” or “Vec is contiguous so always faster.”

## Sources

- RUST-STD-COLLECTIONS
- RUST-STD-VEC
- RUST-STD-HASHMAP
- RUST-STD-BTREEMAP
