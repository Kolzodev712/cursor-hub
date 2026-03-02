# Cursor primitives

Brief reference for how this hub uses Cursor’s building blocks.

## Rules (`.cursor/rules/*.mdc`)

- **What:** Persistent instructions the model can see. Stored as Markdown with YAML frontmatter.
- **When:** Either **always** (`alwaysApply: true`) or when **specific files** are in context (`globs: ["**/*.rs"]`).
- **Use:** Standards, “how we work” (e.g. design log, senior teacher), language-specific guidelines. Keep each rule focused and short; long procedures belong in commands.

## Commands (`.cursor/commands/*.md`)

- **What:** Slash-triggered workflows (e.g. `/design-review`, `/pr-review`). Stored as Markdown.
- **When:** User types `/` and picks a command; the command content is used as instructions for that turn.
- **Use:** Multi-step workflows (review, create ADR, TDR, refactor-safe). Make the steps explicit and, where relevant, require verification (e.g. “run cargo test”).

## Subagents (`.cursor/agents/*.md`)

- **What:** Specialized agent personas. Each file describes behavior and scope for a subagent.
- **When:** User or flow delegates to a subagent (e.g. “use the design critic”).
- **Use:** Focused roles (design critic, implementer, reviewer, test author) so the main agent can hand off to a consistent personality and checklist.

## Hooks

Cursor may support hooks (e.g. pre/post save, pre-commit). This hub does not define hooks yet; packs are limited to rules, commands, and agents.

## Summary

- **Rules** = always-on or file-scoped guardrails.
- **Commands** = on-demand workflows triggered by `/`.
- **Agents** = specialized assistants invoked by name or flow.
