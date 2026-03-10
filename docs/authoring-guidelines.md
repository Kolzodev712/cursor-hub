# Authoring guidelines

How to keep packs “just right”: clear purpose, no bloat, commands that force verification.

## Sizing rules

- **One concern per rule.** If a rule file grows beyond a single theme (e.g. “design review bar” or “Rust error handling”), split it.
- **Keep alwaysApply rules short.** If it’s always-on, every conversation pays the token cost. Put long procedures in commands.
- **Commands: one workflow per file.** The command filename must be `{pack-name}__{task}.md` (e.g. `rust-design-review__wf-1-design-review.md` → `/rust-design-review__wf-1-design-review`). This avoids collisions when installing multiple packs.
- **Agents: one role per file.** Describe behavior and scope; avoid duplicating long rule text.

## Avoid alwaysApply bloat

- Reserve `alwaysApply: true` for a small set of global constraints (e.g. design-log methodology, senior-teacher first response). Prefer `alwaysApply: false` and `globs` for everything else so rules apply only when relevant files are open.
- If a rule is only needed for a specific command, consider inlining the instructions in the command instead of a separate always-on rule.

## Commands that force verification

Commands that change code should end with an explicit verification step so the model doesn’t skip it:

- **Rust:** “Run `cargo fmt --all -- --check` (then `cargo fmt --all` if needed), `cargo clippy --fix --allow-dirty --all-targets --all-features -- -D warnings`, and `cargo test --all-features`. Optionally `cargo audit` and `cargo check --all-targets --all-features`. If the project has a justfile, `just quick` or `just fmt` / `just clippy-fix` / `just test` can be used as equivalents. Fix any failures before considering the task done.”
- **Design/ADR:** “Create the log with `python .cursor/tools/new_design_log.py --slug <name>`; do not guess the next NNN.”
- **Refactor:** “Run tests after each step; do not proceed to the next step until tests pass.”

State the exact commands and the success criterion (e.g. “all tests pass”, “script prints the new file path”).

## Naming

- **Rules:** `kebab-case.mdc`, descriptive (e.g. `rust-anti-footguns.mdc`, `design-log.mdc`).
- **Commands:** `{pack-name}__{kebab-case}.md`; the stem is the slash command (e.g. `rust-design-review__wf-1-design-review.md` → `/rust-design-review__wf-1-design-review`). See [pack-versioning](pack-versioning.md) for the naming convention.
- **Agents:** `kebab-case.md` (e.g. `design-critic.md`, `rust-implementer.md`).

## Frontmatter (rules)

Every `.mdc` rule must have a YAML frontmatter block with at least:

```yaml
---
description: "Short description for the rule picker"
alwaysApply: true   # or false
globs:             # only if file-scoped
  - "**/*.rs"
---
```

Keep the description to one line so the rule picker stays readable.
