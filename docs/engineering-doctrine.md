# Ambient engineering doctrine

cursor-hub separates **policy**, **knowledge**, **project truth**, and **enforcement** so engineering discipline does not depend on remembering slash commands.

## Mental model

| Layer | Location | Role |
|-------|----------|------|
| **Rules** | `.cursor/rules/` | Short ambient policy (classify, consult doctrine, evidence bar) |
| **Skills** | `.cursor/skills/engineering-doctrine/` | Layered knowledge: **decision** → optional **techniques** / **platforms** (see below) |
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

## Knowledge architecture (inside the skill)

The corpus is **not an encyclopedia** of algorithms, CPU tricks, or frameworks.

```text
Core policy (ambient rule + SKILL.md router)
        ↓
decision/          — problem recognition & questions (default load)
        ↓
techniques/        — optional mechanisms (only when routed)
        ↓
platforms/         — conditional compiler/CPU/OS/library facts
        ↓
.cursor/doctrine/  — project objectives, workload, machine facts
        ↓
measurement / evidence
```

**Incompleteness is intentional.** Missing technique/platform files → declare **KNOWLEDGE GAP**, research authoritative sources (SOURCES.md tiers), or measure — do not guess from model memory.

**Promotion:** Project research does not auto-enter cursor-hub. Promote only reusable, source-audited knowledge ([AGENTS.md](../AGENTS.md)).

**Research escalation:** When local verified knowledge is insufficient, state what fact is missing, why it matters, and which authority to consult; mark decisions blocked/conditional if research unavailable.

**Future candidate decision domains** (not implemented until experiment proves need): `compiler-codegen`, `latency-throughput` / scheduling-backpressure.

## Install

```bash
cursor-hub install engineering-doctrine /path/to/project
```

Optional: add to an existing language install — doctrine is **not** part of `--lang rust all` unless you install it explicitly.

The installer:

- Merges the **engineering-doctrine** rule and hook scripts
- **Merges** `hooks.json` (refreshes **hub-owned** entries by script name; preserves unrelated user hooks; **fails** if existing `hooks.json` is invalid JSON)
- Installs the **engineering-doctrine** skill under `.cursor/skills/`
- **Bootstraps** missing files under `.cursor/doctrine/` only (never overwrites project content, including with `--overwrite`)
- On an **interactive** terminal, runs **guided repository setup** when project doctrine is not yet valid (resume anytime with `cursor-hub doctrine setup .`)

Non-interactive install (CI, pipes) **fails** if setup is still required — no guessed defaults. Use `cursor-hub doctrine status .` and `cursor-hub doctrine validate .` to inspect setup.

```bash
cursor-hub doctrine setup .              # run or resume wizard
cursor-hub doctrine setup --review .     # section-by-section review
cursor-hub doctrine setup --review-unknowns .
cursor-hub doctrine status .
cursor-hub doctrine validate .
```

Project-owned **setup lifecycle** lives in `.cursor/doctrine/setup.json` (schema version, section progress, status). Engineering facts stay in `objectives.md`, `invariants.md`, `workload.md`, `architecture.md`, and `components.json`.

Pack-declared **skill dependencies** (e.g. `rust-implementation` → `rust-best-practices`) are copied recursively when those packs are installed.

## Component classification

The setup wizard generates `.cursor/doctrine/components.json` from component interviews and **deterministic** decision-domain routing (`cursor_hub/doctrine/routing.py`). You should not need to hand-edit paths or `required_doctrine_refs` for normal onboarding.

Example shape (for maintainers):

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
        ".cursor/skills/engineering-doctrine/decision/algorithm-selection.md"
      ]
    }
  ]
}
```

Empty `components` disables write gates (policy rules still apply).

## Hooks — what they guarantee

When Cursor runs project hooks:

- **preToolUse (Write family):** If repository setup is `INCOMPLETE`, `INVALID`, or `STALE_SCHEMA`, denies substantive writes until `cursor-hub doctrine setup .` completes successfully. `COMPLETE_WITH_UNKNOWNS` is allowed — unknown facts must not be invented by agents.
- **postToolUse (Read):** Tracks reads under `.cursor/doctrine/`, `.cursor/skills/`, and `components.json`. **Mandatory context** is satisfied only when the hook records **`full_text`** (Read tool output matches the file SHA-256) or **`hook_supplied`** (complete file emitted via `additional_context` for a path-only Read, file ≤512KB). Path-only or partial Read output does **not** unlock classified writes. File-change invalidation uses stored fingerprints.
- **preCompact:** Clears read credits for the session (re-read required after compaction).
- **preToolUse (Write family):** Denies writes to classified paths until mandatory context is satisfied for that session; rejects path traversal and unrecognized multi-file mutation payloads where extraction is required.

**Invalid `components.json`:** If the file **exists** but cannot be parsed or validated, **all substantive file writes** are denied until it is fixed. An empty valid `components: []` disables classification gates (policy rules still apply).

**Session keys:** Prefer Cursor `conversation_id` when present. Otherwise hooks use a **process+workspace ephemeral key** (`ephemeral:pid-…:root-…`) — not a global shared bucket. Reads recorded under one conversation id do not satisfy another.

**Limitations (document honestly):**

- **Engineering-process enforcement, not a security boundary.** Hook coverage is limited to supported Cursor file-write tools. Shell redirects, MCP writes, and other paths bypass the gate until Cursor exposes reliable hooks for them.
- Satisfying the gate means **verified full content** was recorded for that path version, not that the model understood it — the ambient rule still requires using doctrine in reasoning.
- **Ephemeral session (residual):** Keys are `ephemeral:pid-<pid>:root-<hash>`. This removes the old global `default` bucket but **does not** isolate two chats in the **same Cursor process and workspace** when **both** lack `conversation_id` — they can share read state. For the real-repo experiment, confirm whether Cursor normally sends `conversation_id` in hook payloads; if yes, this edge case is rare. See [experiment-engineering-doctrine.md](experiment-engineering-doctrine.md).
- Hooks do not auto-invoke skills; the ambient rule asks the model to load the skill when relevant.

## Real-repo experiment

Before adding harness features, run the **one-component** A/B procedure and scorecard in [experiment-engineering-doctrine.md](experiment-engineering-doctrine.md). Success means better engineering judgment in ordinary chat, not only a denied first write.

## Ownership

| Artifact | Ownership |
|----------|-----------|
| Hub rules/commands/agents | Hub-managed; `--overwrite` refreshes on collision |
| Hub hook scripts | Hub-managed; refreshed on doctrine install |
| `hooks.json` | **Merged** — user entries kept; hub entries (`doctrine_enforcement.py`, `doctrine_setup_gate.py`) refreshed on reinstall |
| `.cursor/doctrine/*` (after bootstrap) | **Project-managed** — never overwritten by install |
| `.cursor/skills/*` | Hub files added/updated with `--overwrite`; existing files skipped otherwise |
| Design logs `NNN-*.md` | **Project-managed** (unchanged) |
