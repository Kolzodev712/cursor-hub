# Networking and serialization

## Epistemic status

Verified: 2026-10-05  
Scope: Protocol-first; no universal framing/compression rules.  
Claim classes: SPEC, HEURISTIC, EMPIRICAL, POLICY

## Trigger

Wire format, parse/encode on hot path, batching, copies, compression.

## Established facts

**[SPEC]** Internet and application protocols define framing, parsing, and semantics in their **RFCs or vendor specs** — use the canonical spec for **your** protocol (HTTP, WebSocket, gRPC, FIX, custom binary, etc.).

**[SPEC / IMPLEMENTATION]** Rust `std::net` documents blocking TCP/UDP APIs; async stacks (e.g. Tokio) document their I/O model separately.

## Decision questions

- What does the **protocol spec** require for framing and parsing?
- Where do **copies** happen (socket buffer → parse → domain object)?
- Message size distribution and rate (from `workload.md`)?
- Dominant cost: syscall count, bandwidth, parse CPU, compression CPU?
- Does batching violate **latency** invariants?

## Engineering guidance

**[HEURISTIC]** For **untrusted** input, use bounded parsing and limit allocation — security/correctness (POLICY), not one framing style for all protocols.

**[HEURISTIC]** Batching/coalescing when **measurement** shows syscall/setup overhead dominates **and** latency budget allows.

**[HEURISTIC]** “Zero-copy” depends on API ownership/lifetime — prove with profiling, not slogan.

**[HEURISTIC]** Compression when CPU cost < bandwidth/latency savings — **EMPIRICAL** per payload.

## Evidence required

**[EMPIRICAL]** End-to-end or component benchmark with realistic messages; fuzz/property tests for parsers.

## Accept / reject

**Accept** when design conforms to protocol spec and measurements support bottleneck story.

**Reject** “always length-prefixed frames” for protocols that define otherwise.

## Sources

- RUST-STD-VEC
