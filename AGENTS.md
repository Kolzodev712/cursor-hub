# AGENTS.md — AI contract for cursor-hub

This file is the single contract for contributors and agents working on the **cursor-hub repository itself** (adding packs, rules, commands, or changing hub docs/tooling).

## Purpose of the hub

- **Languages:** `tools/install.py` defines language profiles for `--lang` (e.g. rust
  installs design-log, documentation, security, and all Rust packs under
  `packs/cursor/rust/`). Other languages currently install shared packs plus their
  placeholder pack.

- **Languages:** Language profiles live under `packs/cursor/languages/<lang>/manifest.yml` and list which packs to install for that language. Rust-specific packs live under `packs/cursor/rust/` (design-review, implementation, testing, bugfix, review). Other languages (python, js-ts, terraform) have placeholder packs today.


- **Design-log and workflow are non-negotiable.** The hub ships a design-log methodology (logs in `.cursor/design-log/`, creation via `new_design_log.py`), workflow commands (design review → implement → test, plus bugfix flow), and standalone commands. Packs live under `packs/cursor/`; each has `pack.yml` and optionally `.cursor/rules/`, `.cursor/commands/`, `.cursor/agents/`.
- **Where things live:** Rules in `.cursor/rules/*.mdc`, commands in `.cursor/commands/*.md`, agents in `.cursor/agents/*.md`. Command filenames use `{pack-name}__{command-name}.md`. The installer copies into a target project’s `.cursor/`; see [CATALOG.md](CATALOG.md) and [README.md](README.md).

## When adding or changing hub content

- **Follow [docs/authoring-guidelines.md](docs/authoring-guidelines.md):** one concern per rule, command naming `pack-name__task`, verification steps where commands change code, frontmatter for rules.
- **Present drafts for approval:** For generated or new artifacts (new rules, new commands, new design-log sections beyond the template), **present the full draft to the user and wait for explicit approval before writing files.** This applies when you are creating or editing hub content (e.g. a new pack, a new rule, or a new command). See the **present-before-writing** rule in `_shared`; workflow and design-log methodology reference it where relevant.

## Validation

- After adding or changing packs or rules, run `python tools/validate_packs.py` and update [CATALOG.md](CATALOG.md) and [README.md](README.md) as needed.
