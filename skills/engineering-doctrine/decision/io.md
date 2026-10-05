# Decision domain — I/O and serialization

## Epistemic status

Verified: 2026-10-05 · Scope: wire/parse path · Classes: SPEC, HEURISTIC, EMPIRICAL, POLICY

## Questions before any technique

- What does the **protocol spec** require (RFC/vendor — project-owned reference)?
- Dominant cost: syscalls, bandwidth, parse CPU, copies, compression CPU?
- Message sizes/rates (project workload)?
- Untrusted input — bounded parsing and allocation limits?

## Possible next investigations

- Measure copy points and parse cost separately.
- Batching/coalescing only if measurement shows setup overhead **and** latency budget allows.
- “Zero-copy” claims → prove with profiling + API ownership model.

## Knowledge gap

Project-specific protocol (FIX, exchange binary, etc.) → **project doctrine** or **EXTERNAL_RESEARCH** to canonical spec — not generic doctrine.

## Evidence

**[EMPIRICAL]** Realistic load + parser tests/fuzz where untrusted.

## Sources

- RUST-STD-VEC
