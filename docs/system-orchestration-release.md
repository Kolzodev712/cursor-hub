# System orchestration release notes

Hub package: 0.7.0. Opt-in pack: system-orchestration 0.1.0.

Adds design/review commands, source-scoped references, project charter/adapter scaffolds, closed contract exports, validation, a deterministic offline supervisor, and optional local transactional checkpoint/replay. Two examples are synthetic and invoke no external systems. No live runtime is activated or included in default language bundles.

The single-argument installer now recognizes optional packs through manifest discovery, including fault-first. Existing language shortcuts and target interpretation remain compatible. No doctrine, fault-first, hooks, setup schemas or project-owned operating files are changed.

The initial candidate (81fe1e0f38c11f8d4e3f4bd0d87c4ea4389debcb) passed GitHub Actions run 38274676146 on Python 3.10, 3.11 and 3.12, including pack validation, doctrine source structure and 139 tests. Subsequent documentation/isolation-check changes require their own CI result; this is not a claim about an untested later commit.

Known scope limits: actor identities, model usage and evidence are fixture assertions; no authenticated approval or real artifact verification exists. The journal is local operator-owned storage, not a security boundary or distributed scheduler. An interrupted first creation can leave a file that must be inspected explicitly. No automatic repair/migration is performed. Existing unrelated ResourceWarning messages in doctrine tests and legacy GitHub Action runtime deprecation warnings are outside this feature's change scope.

See [system-orchestration.md](system-orchestration.md) for usage and the separate live-adapter activation requirements.
