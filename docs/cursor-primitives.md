# Cursor primitives

Brief reference for how this hub uses Cursor’s building blocks.

## Rules (`.cursor/rules/*.mdc`)

- **What:** Persistent instructions the model can see. Stored as Markdown with YAML frontmatter.
- **When:** Either **always** (`alwaysApply: true`) or when **specific files** are in context (`globs: ["**/*.rs"]`).
- **Use:** Standards, “how we work” (e.g. design log, senior teacher), language-specific guidelines. Keep each rule focused and short; long procedures belong in commands.

## Commands (`.cursor/commands/*.md`)

- **What:** Slash-triggered workflows (e.g. `/rust-design-review__wf-1-design-review`, `/rust-review__standalone-pr-review`, `/documentation__standalone-architecture-doc`). Stored as Markdown.
- **When:** User types `/` and picks a command; the command content is used as instructions for that turn.
- **Use:** Multi-step workflows (design review, implement from log, add tests, bugfix, refactor-safe, PR review, documentation). Make the steps explicit and, where relevant, require verification (e.g. run cargo test, run the design-log validator).

## Agents (`.cursor/agents/*.md`)

- **What:** Specialized agent personas. Each file describes behavior and scope for an agent.
- **When:** User or flow runs a command that embodies that agent (e.g. design critic, implementer, reviewer).
- **Use:** Focused roles (design critic, implementer, reviewer, test author, documentation) so the right checklist and tone apply when you run the matching command.

## Hooks

Cursor may support hooks (e.g. pre/post save, pre-commit). This hub does not define hooks yet; packs are limited to rules, commands, and agents.

## Summary

- **Rules** = always-on or file-scoped guardrails.
- **Commands** = on-demand workflows triggered by `/`.
- **Agents** = specialized assistants invoked by name or flow.
