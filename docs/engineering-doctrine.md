# Ambient engineering doctrine

cursor-hub separates **policy**, **knowledge**, **project truth**, and **enforcement** so engineering discipline does not depend on remembering slash commands.

## Mental model

| Layer | Location | Role |
|-------|----------|------|
| **Rules** | `.cursor/rules/` | Short ambient policy (classify, consult doctrine, evidence bar) |
| **Skills** | `.cursor/skills/` | Deep reusable doctrine; loaded progressively via the skill router |
| **Project doctrine** | `.cursor/doctrine/` | Objectives, invariants, architecture, workload, findings, component map |
| **Hooks** | `.cursor/hooks/` + `hooks.json` | Mechanical gates at meaningful boundaries (first write to classified paths) |
| **Commands** | `.cursor/commands/` | Optional explicit workflows (design review, gates, bugfix) |

Normal prompts should inherit policy from rules; the agent loads skills and project doctrine as needed. Commands remain for deliberate audits and structured workflows.

## Epistemic model (doctrine content)

Generic skill text is classified so agents do not confuse mechanisms with benchmarks:

| Class | Role |
|-------|------|
| **SPEC** | Spec/API guarantees (Rust Reference, std docs, RFCs) |
| **IMPLEMENTATION** | Scoped to a compiler version, std build, CPU family, or tool |
| **EMPIRICAL** | Application performance — requires project measurement |
| **HEURISTIC** | What to investigate; not universal truth |
| **POLICY** | cursor-hub / project behavior (evidence before “faster”) |

**Sources** ([skills/engineering-doctrine/SOURCES.md](../skills/engineering-doctrine/SOURCES.md)) establish mechanisms and scope limits (“does not establish”). **Project doctrine** holds objectives, invariants, and machine facts. **Policy** holds evidence thresholds. Maintainers audit changes in [doctrine-source-audit.md](doctrine-source-audit.md); run `python3 tools/validate_doctrine_sources.py` in CI.

Runtime agents should rely on **verified local doctrine + project facts + measurement**, not ad-hoc web search, unless updating doctrine or covering a gap marked UNRESOLVED.

## Install

```bash
cursor-hub install engineering-doctrine /path/to/project
```

Optional: add to an existing language install — doctrine is **not** part of `--lang rust all` unless you install it explicitly.

The installer:

- Merges the **engineering-doctrine** rule and hook scripts
- **Merges** `hooks.json` (dedupes hub entries; preserves user hooks)
- Installs the **engineering-doctrine** skill under `.cursor/skills/`
- **Bootstraps** missing files under `.cursor/doctrine/` only (never overwrites project content, including with `--overwrite`)

Pack-declared **skill dependencies** (e.g. `rust-implementation` → `rust-best-practices`) are copied recursively when those packs are installed.

## Component classification

Edit `.cursor/doctrine/components.json`:

```json
{
  "components": [
    {
      "id": "matching-engine",
      "patterns": ["crates/matcher/**"],
      "required_project_files": [
        ".cursor/doctrine/objectives.md",
        ".cursor/doctrine/invariants.md",
        ".cursor/doctrine/workload.md"
      ],
      "required_doctrine_refs": [
        ".cursor/skills/engineering-doctrine/reference/algorithm-selection.md"
      ]
    }
  ]
}
```

Empty `components` disables write gates (policy rules still apply).

## Hooks — what they guarantee

When Cursor runs project hooks:

- **postToolUse (Read):** After a successful Read, records a **SHA-256 fingerprint** of each path under `.cursor/doctrine/` or `.cursor/skills/` for the session.
- **preToolUse (Write family):** Denies writes to classified paths until required files were read **at their current fingerprint** in that session.

**Invalid `components.json`:** If the file **exists** but cannot be parsed or validated, **all substantive file writes** are denied until it is fixed. An empty valid `components: []` disables classification gates (policy rules still apply).

**Session keys:** Prefer Cursor `conversation_id` when present. Otherwise hooks use a **process+workspace ephemeral key** (`ephemeral:pid-…:root-…`) — not a global shared bucket. Reads recorded under one conversation id do not satisfy another.

**Limitations (document honestly):**

- **Engineering-process enforcement, not a security boundary.** Hook coverage is limited to supported Cursor file-write tools. Shell redirects, MCP writes, and other paths bypass the gate until Cursor exposes reliable hooks for them.
- Read tracking means **the agent received the current bytes**, not that it understood them — the ambient rule still requires using doctrine in reasoning.
- **Ephemeral session (residual):** Keys are `ephemeral:pid-<pid>:root-<hash>`. This removes the old global `default` bucket but **does not** isolate two chats in the **same Cursor process and workspace** when **both** lack `conversation_id` — they can share read state. For the real-repo experiment, confirm whether Cursor normally sends `conversation_id` in hook payloads; if yes, this edge case is rare. See [experiment-engineering-doctrine.md](experiment-engineering-doctrine.md).
- Hooks do not auto-invoke skills; the ambient rule asks the model to load the skill when relevant.

## Real-repo experiment

Before adding harness features, run the **one-component** A/B procedure and scorecard in [experiment-engineering-doctrine.md](experiment-engineering-doctrine.md). Success means better engineering judgment in ordinary chat, not only a denied first write.

## Ownership

| Artifact | Ownership |
|----------|-----------|
| Hub rules/commands/agents | Hub-managed; `--overwrite` refreshes on collision |
| Hub hook scripts | Hub-managed; refreshed on doctrine install |
| `hooks.json` | **Merged** — user entries kept; hub entries deduped by command+matcher |
| `.cursor/doctrine/*` (after bootstrap) | **Project-managed** — never overwritten by install |
| `.cursor/skills/*` | Hub files added/updated with `--overwrite`; existing files skipped otherwise |
| Design logs `NNN-*.md` | **Project-managed** (unchanged) |
