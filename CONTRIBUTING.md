# Contributing to cursor-hub

Thanks for considering contributing. This document explains how to propose changes and keep the hub consistent.

## Development setup

1. Clone the repo (or your fork).
2. From the repo root, run validation:
   ```bash
   python tools/validate_packs.py
   ```
   Fix any errors before opening a PR.

## What we check

- **Pack structure:** Every pack under `packs/cursor/` has a `pack.yml`. Non–`_shared` packs have `.cursor/rules/`, `.cursor/commands/`, and optionally `.cursor/agents/`.
- **Rules:** `.mdc` files have valid YAML frontmatter with at least a `description` field.
- **Commands:** Command files are named `{pack-name}__{command-name}.md` (e.g. `rust-design-review__wf-1-design-review.md`) so that installing multiple packs does not produce name collisions. Validator enforces this.
- **Pack version:** `pack.yml` may include a `version` (e.g. `0.2.0`). The installer prints installed pack versions when present.

## Pull requests

1. Branch from `main` (or the current default branch).
2. Run `python tools/validate_packs.py` and fix any failures.
3. Keep changes focused: one logical change per PR (e.g. one new rule, or one pack update).
4. Update [CHANGELOG.md](CHANGELOG.md) under `[Unreleased]` for user-visible changes.
5. Open a PR; we’ll run CI (validation) and review.

## Adding a new pack

1. Create `packs/cursor/<pack-name>/` with:
   - `pack.yml` (required; include `name`, `description`, and optionally `version`).
   - `.cursor/rules/` (at least one `.mdc` with frontmatter).
   - `.cursor/commands/` — each file must be named `<pack-name>__<command>.md`.
   - `.cursor/agents/` (optional) — `.md` files only.
2. Run `python tools/validate_packs.py` and fix any errors.
3. Document the pack in [CATALOG.md](CATALOG.md) and add it to the installer’s `ALL_RUST_PACKS` in `tools/install.py` if it should be part of the “all” set.

## Adding a new command

- Add a file `.cursor/commands/{pack-name}__{command-name}.md` in the pack.
- The filename (without `.md`) is the slash command users will see (e.g. `/design-log__create`).
- Keep the content focused on one workflow; include verification steps where the command changes code.
- Update CATALOG.md and any relevant docs (e.g. [docs/using-packs.md](docs/using-packs.md)).

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
