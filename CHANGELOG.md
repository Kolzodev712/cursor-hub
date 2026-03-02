# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial public release of the Cursor AI hub (modular rules, commands, and agents).
- **Packs** (under `packs/cursor/`):
  - **_shared** — Design-log methodology, when-to-log guidance; always installed with any other pack.
  - **rust-design-review** — Question-first design, design review bar, ADR creation, decision summaries.
  - **rust-implementation** — Small diffs, verification loop (fmt/clippy/test), anti-footguns.
  - **rust-testing** — TDR, add-tests-only, deterministic tests, fixtures.
  - **rust-review** — PR review checklist, risky-changes scan (unsafe, unwrap, new deps, API breaks).
- **Tools** (under `tools/`):
  - `install.py` — Install one or more packs into a target project (merge into `.cursor/`).
  - `validate_packs.py` — Validate pack layout, frontmatter, and command uniqueness.
  - `new_design_log.py` — Create design-log files with deterministic numbering.
  - `export_design_logs_mongo.py` — Stub for exporting design-log metadata (e.g. to MongoDB).
- **Documentation**: CATALOG.md, using-packs, cursor-primitives, authoring-guidelines, pack-versioning, feature-workflow example.

---

## [0.1.0] - 2025-03-02

### Added

- First versioned release; contents as described under [Unreleased] above.

[Unreleased]: https://github.com/your-org/cursor-hub/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/your-org/cursor-hub/releases/tag/v0.1.0
