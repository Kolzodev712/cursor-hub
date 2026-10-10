# Fault-first analysis pack

**Status:** opt-in pack (v0.1.0); read-only by default; not part of `--lang` bundles and installs no hooks.

## Installation

From a cursor-hub checkout containing this pack:

```bash
cursor-hub install fault-first /path/to/disposable-project
```

The existing installer discovers `packs/cursor/fault-first/pack.yml` and recursively installs `skills/fault-first/`. This pack does **not** change ambient rules, hooks, project doctrine, or the existing `--lang rust` bundle. Installation is opt-in. In Cursor invoke `/fault-first__analyze` with a named scope and desired failure outcome. The command delegates to the skill and optional analyst role. No autonomous edits, test generation, or fault injection are authorized.

## Relationship to engineering-doctrine

The fault-first workflow consumes project objectives, invariants, architecture and workload *if present*. It is compatible with the layered engineering-doctrine skill but does not require it or override its setup gate. Fault-first asks **how guarantees might fail**; doctrine asks **how to choose an engineering approach**. Findings are proposed, not automatically promoted to `.cursor/doctrine/` or design logs.

## Usage

- Before implementation: `/fault-first__analyze Evaluate the proposed TCP frame decoder design; focus on incomplete frames, resource bounds, and state transitions. Do not write code.`
- Existing code: `/fault-first__analyze Inspect the framing boundary in src/protocol/tcp_framing.rs; distinguish demonstrated violations from hypotheses.`
- Named outcome: `/fault-first__analyze Starting from "a frame consumes bytes from the next frame", derive credible causes and tests.`

For the first pilot use a **disposable ll-cache clone** and only one component. Preserve user-led design and no-code workflow. The analysis is read-only, even if the repository contains existing implementation commands that normally write design logs. No production trading or exchange activity.

## Evaluation protocol

Run only after **Phase 1** on a disposable pilot repo (ordinary development works with doctrine installed). Compare (A) normal scoped design review and (B) fault-first on the same requirements, code snapshot, and model/settings. Have a human evaluate: useful missing guarantees identified; confirmed claims backed by evidence; hypothesis/spec-gap precision; actionable falsification tests; unnecessary speculative findings; tokens/time and human review burden. Do not reward number of failure modes. Record whether a suggestion was already covered by tests or existing invariants. Repeat tasks before claiming improvement.

**Acceptance bar:** the workflow identifies at least one material new risk or produces a well-supported no-new-risk assessment without fabricating defects, respects read-only/user-owned work, and stays within bounded scope. A single successful pilot is not proof of broad benefit.

## Known limitations

This is an instruction-driven investigation, not an executable model checker or fault injector. It does not enforce test execution, correctness proofs, or completion gates. No new hook is installed. Claims of confirmed defects still require human verification of cited evidence. The standard-method references are methodological background, not certification.
