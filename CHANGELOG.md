# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **CONTRIBUTING.md** — How to contribute, run validation, add packs/commands, and open PRs.
- **CI** — GitHub Actions workflow runs `python tools/validate_packs.py` on push/PR to `main`.
- **Install `--with-tools`** — Option to copy `tools/` into the target project so `new_design_log.py` can be run from the project root.
- **Installer prints pack versions** — When `pack.yml` includes `version`, the installer reports installed pack versions (e.g. `_shared=0.1.0 rust-design-review=0.1.0`).
- **Command naming convention** — Commands must be named `{pack-name}__{command-name}.md`; validator enforces this to avoid cross-pack collisions. All existing commands renamed (e.g. `/design-review` → `/rust-design-review__design-review`).
- **Cross-platform install docs** — README uses cursor-hub naming, Unix/macOS examples first, then Windows (PowerShell) examples; submodule + `--with-tools` workflow documented.

### Changed

- **Repo naming** — README and tooling refer to "cursor-hub" (replacing "AI_Rules_Kolzo") for consistency.
- **docs/pack-versioning.md** — Documents command naming convention, installer version output, and CI.
- **docs/authoring-guidelines.md** — Commands must use `pack-name__command-name` convention.
- **CATALOG.md, examples/feature-workflow.md, docs/using-packs.md, docs/cursor-primitives.md** — All command references updated to namespaced form (e.g. `/rust-design-review__adr-new`).
- **design-log.mdc, rust-implementer.md, reviewer.md** — Internal command references updated to namespaced commands.

### Fixed

- Installer error message when target is inside hub is now cross-platform (no Windows-specific path hint).

---

## [0.1.0] - 2025-03-02

### Added

- Initial public release of the Cursor AI hub (modular rules, commands, and agents).
- **Packs** (under `packs/cursor/`): _shared, rust-design-review, rust-implementation, rust-testing, rust-review.
- **Tools**: install.py, validate_packs.py, new_design_log.py, export_design_logs_mongo.py (stub).
- **Documentation**: CATALOG.md, using-packs, cursor-primitives, authoring-guidelines, pack-versioning, feature-workflow example.
- LICENSE (MIT), CHANGELOG.md.

[Unreleased]: https://github.com/your-org/cursor-hub/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/your-org/cursor-hub/releases/tag/v0.1.0
