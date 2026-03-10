# Workflow doc (standalone)

Produce a **general-level workflow document**: how work gets done in the project — main phases, roles, tooling, and conventions. Use for onboarding, process docs, or team alignment.

## Steps

1. **Scope:** Confirm what to document (e.g. "how we build features", "release process", "how we use this repo's workflows"). If unclear, ask.
2. **Gather:** Review repo docs, `.cursor/` (commands, design-log, tools), and any existing workflow or contributing docs. Infer from pack commands and design-log methodology if present.
3. **Produce the doc:** Write a concise workflow document with:
   - **Purpose** — One line: what workflow this describes.
   - **Overview** — When this workflow applies and who does what (roles or "the developer").
   - **Phases** — Main steps (e.g. design → implement → test; or triage → fix → verify). Brief description of each.
   - **Tooling** — Commands, scripts, or tools used (e.g. slash commands, `cargo`, scripts in `.cursor/tools/`).
   - **Conventions** — Branching, design logs, review expectations, or other norms.
   - **Where to go deeper** — Point to specific workflow docs or commands for step-by-step detail.
4. **Output:** Present the doc in the response. If the user wants it saved, create or overwrite a file (e.g. `docs/workflow.md` or a path they specify). Otherwise leave it in chat.

Keep it general: high-level flow, not every sub-step. For one workflow in full detail use `/documentation__standalone-specific-workflow-doc`.
