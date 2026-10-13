# System orchestration kit design decision

Date: 2026-10-12
Baseline: d6f034fa50669886d25293ad4df21aa2a1da1d69
Authorization: user requested implementation of the discussed construction-kit approach in cursor-hub and an independent Cursor review prompt.

## Decision

Add an opt-in design/review pack plus a narrow offline reference supervisor. Keep operational contracts, policy decisions, model proposals, receipts and verification separate. Reuse recursive skill installation and extend the CLI with isolated orchestration commands. Retain current doctrine/fault-first/default-bundle behavior.

## Alternatives and consequences

A prompt-only pack cannot demonstrate lifecycle/recovery enforcement. A live autonomous runtime would introduce provider, credentials, sandboxing and deployment responsibilities not yet validated. A generic workflow language would overgeneralize before a pilot. The chosen implementation supports offline contract work and synthetic examples without external effects. Its JSON schemas are generated from one executable definition rather than independently maintained copies.

## Scope and verification boundaries

The SQLite journal stores committed simulation prefixes, not real action execution. Replay uses recorded events; no new model call occurs. Actor identities, usage and evidence are assertions supplied by fixtures. The test suite exercises the supervisor and installer, not live agent security or model accuracy. README, catalog and skill references must describe this limit explicitly.

See docs/system-orchestration.md for commands, tests, ownership and live-activation gaps. This standalone hub design note is not a workflow completion stamp and does not modify any target project's numbered logs.
