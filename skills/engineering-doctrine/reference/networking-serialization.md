# Networking and serialization

## Trigger

Wire format or parse/encode on request path or bulk ingest.

## Questions

- Copies per message? Zero-copy possible with framing?
- Schema evolution requirements?
- Compression worth CPU at this bandwidth/latency?

## Reasoning

- Measure bytes on wire and parse CPU separately.
- Prefer length-prefixed frames and bounded parsers for untrusted input.
- Batch small messages when syscall overhead dominates.

## Evidence

Load test with realistic message sizes; fuzz or property tests for parsers.

## Accept when

End-to-end latency/throughput meets objective or bottleneck identified elsewhere.
