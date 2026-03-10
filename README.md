# cursor-hub

[![Validate packs](https://github.com/your-org/cursor-hub/actions/workflows/validate.yml/badge.svg)](https://github.com/your-org/cursor-hub/actions/workflows/validate.yml) — *Replace `your-org/cursor-hub` with your repo for the badge.*

A **public Cursor AI hub**: modular rules, commands, and agents for guiding AI assistants. The content is **language- and model-agnostic** in principle; this repository currently ships **Cursor-only** instructions (rules, slash commands, agents), with a **Rust-first** set of packs.

## What's in the repo

- **Packs** under `packs/cursor/`: each pack is a folder with `.cursor/rules/`, `.cursor/commands/`, optionally `.cursor/agents/`. The installer also creates `.cursor/design-log/` and copies scripts into `.cursor/tools/` in the target project. Install one or more packs into your project.
- **Tools** under `tools/`: install script, validate pack layout, new_design_log script, and an optional export stub. When you install packs, these are copied into the target's `.cursor/tools/` so they work from any repo. No `pip install` needed (see `tools/requirements.txt`).

- **Shared foundation** (`_shared`): design-log methodology and when-to-log guidance. It is always installed when you install any other pack.

## Quick install

**Recommended: use the hub as a submodule and run the install script from the hub** (one consistent path):

```bash
# From your project (or clone cursor-hub first)
git submodule add https://github.com/your-org/cursor-hub.git .cursor-hub   # or your hub URL
cd .cursor-hub
python tools/install.py all /path/to/your/project
```

The installer copies packs into the target's `.cursor/` (rules, commands, agents, design-log, tools). You can then run `python .cursor/tools/new_design_log.py --slug <name>` from the target project root.

### Examples (Unix / macOS)

```bash
# All Rust packs into a project folder next to the hub
python tools/install.py all ../my-project

# One or more packs
python tools/install.py rust-design-review rust-implementation ../my-project

# Dry run
python tools/install.py --dry-run all ../my-project
```

### Examples (Windows)

```powershell
# All Rust packs into a project folder next to the hub
python tools/install.py all ..\my-project

# One or more packs
python tools/install.py rust-design-review rust-implementation ..\my-project
```

**Note:** Target must be **outside** the hub repo (e.g. `../my-project`). The installer blocks installing into the hub itself.

## Which pack do I use?

| Pack | Use when you want… |
|------|---------------------|
| **design-log** | Design log creation and automatic recording after each workflow step (each pack's wf-1); manual `/design-log__create` and `/design-log__record-step`. |
| **rust-design-review** | Design-first workflow: questions before drafting, design review bar, ADR creation, decision summaries. |
| **rust-implementation** | Implementation discipline: small diffs, no scope creep, verification loop (fmt/clippy/test), anti-footguns. |
| **rust-testing** | TDR (failing test first), add-tests-only, deterministic tests, fixtures. |
| **rust-bugfix** | Fix small bugs (standalone) or non-trivial bugs (3-step workflow: investigation → proposed solution → resolution). Separate from main design/implement/test flow. |
| **documentation** | Standalone commands to create architecture docs, feature docs, workflow docs, and bug summaries. |
| **rust-review** | PR review checklist, risky-changes scan (unsafe, unwrap, new deps, API breaks). |

You can install multiple packs; they merge into a single `.cursor/`. Commands are namespaced by pack (e.g. `/rust-design-review__wf-1-design-review`). Use the **main workflow** (design, implement, test) in any order or on their own — each pack numbers its own steps (e.g. wf-1). **Standalone** commands: gates, refactor, PR review, etc. See [CATALOG.md](CATALOG.md) for the full list.

## Design log (deterministic numbering)

To create the next design log file **without guessing the number**:

- **From your project root** (after installing packs, tools are in `.cursor/tools/`):  
  `python .cursor/tools/new_design_log.py --slug short-name`
- **From the hub repo** (e.g. hub as submodule, creating a log in a project):  
  `python tools/new_design_log.py --slug short-name --dir /path/to/your/project/.cursor/design-log`

**Workflow validator (workflow commands only):** After running a workflow command (not a standalone), the command instructs the model to run `python .cursor/tools/validate_workflow_design_log.py --step <step>` to verify the design log was updated. Steps: `design-review`, `implement`, `add-tests`, `investigation`, `proposed-solution`, `resolution`. Standalone commands do not run this validator.

## Validation

From the cursor-hub repo root:

```bash
python tools/validate_packs.py
```

Checks that every pack has `pack.yml`, rules have valid frontmatter, commands follow the `pack-name__command-name` convention and are non-empty, and there are no duplicate command names per pack.

## Optional: export design logs

`tools/export_design_logs_mongo.py` is a **stub**: it reads `.cursor/design-log/*.md` (by default), extracts metadata (number, slug, title, date), and prints JSON lines. A future version could push to MongoDB if `MONGO_URI` (and optionally `MONGO_DB`) are set; see the script docstring and [docs/pack-versioning.md](docs/pack-versioning.md) for compatibility notes.

## Docs

- [examples/feature-workflow.md](examples/feature-workflow.md) — Main workflow and standalone commands with examples.
- [docs/using-packs.md](docs/using-packs.md) — How to use commands: main workflow vs standalone.
- [CATALOG.md](CATALOG.md) — All packs and commands.
- [docs/cursor-primitives.md](docs/cursor-primitives.md) — Rules vs commands vs agents.
- [docs/authoring-guidelines.md](docs/authoring-guidelines.md) — Sizing and writing commands (including command naming).
- [docs/pack-versioning.md](docs/pack-versioning.md) — Versioning and compatibility.

## License

[MIT](LICENSE). See [CONTRIBUTING.md](CONTRIBUTING.md) if you want to contribute.
