# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

(No changes yet.)

---

## [0.2.0] - 2025-03-10

### Added

- **design-log pack** — Dedicated pack for design log creation and step recording. Workflow commands (design review, implement, add tests, bugfix steps) now create or append the design log automatically at the end of each run; no separate "create design log" step. Commands: `design-log__create`, `design-log__record-step`. Rule: `design-log-record.mdc` (reference only).
- **rust-bugfix pack** — Separate pack for bugfix: standalone command `standalone-fix-small-bug` and 3-step workflow (wf-1-investigation → wf-2-proposed-solution → wf-3-resolution), each with design log recording. Not connected to the main design/implement/test flow.
- **Workflow design-log validator** — `tools/validate_workflow_design_log.py --step <step>` verifies that the expected section is present in the design log after a workflow command. Workflow commands include a "Verify" step that runs the validator; standalone commands do not. Steps: design-review, implement, add-tests, investigation, proposed-solution, resolution.
- **documentation pack** — Standalone commands only: `standalone-architecture-doc`, `standalone-feature-doc`, `standalone-workflow-doc`, `standalone-specific-workflow-doc`, `standalone-bug-summary` for generating architecture, feature, workflow, and bug-summary docs.
- **Design review: check existing logs** — New step 1 in wf-1-design-review: check `.cursor/design-log/` for related or overlapping logs and reference/extend them when relevant.
- **Optional cargo audit / cargo check** — Implement (wf-1-implement-module) and bugfix resolution (wf-3-resolution) verification steps now mention optional `cargo audit` and `cargo check --all-targets --all-features` if the project uses them.

### Changed

- **Pack-local workflow numbering** — Workflow step numbers are per pack only (no cross-pack "Step 1, 3, 4"). rust-design-review has wf-1-design-review; rust-implementation has wf-1-implement-module; rust-testing has wf-1-add-tests-only. You can run design, implement, or add tests in any order or on their own.
- **Design log creation** — Removed manual "Step 2: create design log" from the main flow. Recording is mandatory at the end of each workflow command (design discussion, Implementation Results, Test session, or bugfix Investigation/Proposed solution/Resolution).
- **design-log-record.mdc** — Clarified as reference-only (not auto-applied); workflow commands inline the recording and verification steps.
- **Bugfix** — Moved from rust-testing (wf-4-bugfix-tdr) into the new rust-bugfix pack (standalone + 3-step workflow). rust-testing now has only wf-1-add-tests-only.
- **CATALOG, README, docs/using-packs, examples/feature-workflow** — Updated for design-log pack, rust-bugfix pack, pack-local numbering, validator, and documentation pack.

### Removed

- **rust-design-review__wf-2-design-log-create** — Replaced by design-log pack's `design-log__create` and automatic recording in workflow commands.
- **rust-testing__wf-4-bugfix-tdr** — Replaced by rust-bugfix pack (standalone-fix-small-bug and wf-1/wf-2/wf-3 workflow).

---

## [0.1.1] - 2025-03-02

### Added

- **CONTRIBUTING.md** — How to contribute, run validation, add packs/commands, and open PRs.
- **CI** — GitHub Actions workflow runs `python tools/validate_packs.py` on push/PR to `main`.
- **Install tools** — Installer copies scripts into the target project under `.cursor/tools/` so `new_design_log.py` can be run from the project root.
- **Installer prints pack versions** — When `pack.yml` includes `version`, the installer reports installed pack versions (e.g. `_shared=0.1.0 rust-design-review=0.1.0`).
- **Command naming convention** — Commands must be named `{pack-name}__{command-name}.md`; validator enforces this to avoid cross-pack collisions. Command names are explicit about intent (e.g. `/rust-design-review__wf-1-design-review`, `/rust-review__standalone-pr-review`, `/rust-design-review__gate-design`).
- **Cross-platform install docs** — README uses cursor-hub naming, Unix/macOS examples first, then Windows (PowerShell) examples; tools are installed into `.cursor/tools/`.

### Changed

- **Repo naming** — README and tooling refer to "cursor-hub" (replacing "AI_Rules_Kolzo") for consistency.
- **docs/pack-versioning.md** — Documents command naming convention, installer version output, and CI.
- **docs/authoring-guidelines.md** — Commands must use `pack-name__command-name` convention.
- **CATALOG.md, examples/feature-workflow.md, docs/using-packs.md, docs/cursor-primitives.md** — Command references updated to match the explicit workflow/standalone naming scheme.
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

[Unreleased]: https://github.com/your-org/cursor-hub/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/your-org/cursor-hub/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/your-org/cursor-hub/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/your-org/cursor-hub/releases/tag/v0.1.0
