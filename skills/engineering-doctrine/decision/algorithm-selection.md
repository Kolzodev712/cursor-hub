# Decision domain — algorithm and collection choice

## Epistemic status

Verified: 2026-10-05 · Scope: representation / asymptotic choice · Classes: SPEC, EMPIRICAL, HEURISTIC, POLICY

## Questions before any technique

- What **operation** dominates (lookup, insert, scan, range, join)?
- What is **N**, growth, and key domain (**dense vs sparse**, bounded vs unbounded)?
- Read/write/delete mix; ordering or range queries required?
- Latency vs throughput objective (project doctrine)?
- Is this path **hot** (profile/trace)?

## Established facts (mechanisms only)

**[SPEC/IMPLEMENTATION]** Std collection **API complexity** is documented (`HashMap`, `BTreeMap`, `Vec`) — not constant-factor winners at your N. Sources: RUST-STD-HASHMAP, RUST-STD-BTREEMAP, RUST-STD-VEC, RUST-STD-COLLECTIONS.

## Possible next investigations

- Dense bounded integer keys → evaluate **direct indexing** / contiguous storage (then **data-layout** + measure).
- Need ordering/range → **BTreeMap** or sorted contiguous structure (measure).
- Opaque/sparse keys → **hash map** as a **candidate** (measure hash + locality costs).
- Specialized structures (interning, perfect hashing) → only if domain constraints documented **and** simpler options fail measurement.

## Evidence

**[POLICY]** No “O(1) therefore faster” claims; require representative benchmark + correctness tests.

## Sources

- RUST-STD-COLLECTIONS
- RUST-STD-VEC
- RUST-STD-HASHMAP
- RUST-STD-BTREEMAP
