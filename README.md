# cursor-hub

[![Validate packs](https://github.com/your-org/cursor-hub/actions/workflows/validate.yml/badge.svg)](https://github.com/your-org/cursor-hub/actions/workflows/validate.yml) — *Replace `your-org/cursor-hub` with your repo for the badge.*

A **public Cursor AI hub**: modular rules, commands, and agents for guiding AI assistants. The content is **language- and model-agnostic** in principle; this repository currently ships **Cursor-only** instructions (rules, slash commands, subagents), with a **Rust-first** set of packs.

## What's in the repo

- **Packs** under `packs/cursor/`: each pack is a folder with `.cursor/rules/`, `.cursor/commands/`, optionally `.cursor/agents/`. The installer also creates `.cursor/design-log/` in the target project for design logs. Install one or more packs into your project.
- **Shared foundation** (`_shared`): design-log methodology and when-to-log guidance. It is always installed when you install any other pack.
- **Tools** under `tools/`: install packs, validate pack layout, create design logs with deterministic numbering, and an optional export stub. They use the Python standard library only; no `pip install` needed (see `tools/requirements.txt`).

## Quick install

**Recommended: use the hub as a submodule and run tools from the hub** (one consistent path):

```bash
# From your project (or clone cursor-hub first)
git submodule add https://github.com/your-org/cursor-hub.git .cursor-hub   # or your hub URL
cd .cursor-hub
python tools/install.py all /path/to/your/project
```

**Option: copy tools into your project** so you can run `new_design_log.py` etc. from the project root:

```bash
# From cursor-hub repo root
python tools/install.py all /path/to/your/project --with-tools
```

### Examples (Unix / macOS)

```bash
# All Rust packs into a project folder next to the hub
python tools/install.py all ../my-project

# One or more packs
python tools/install.py rust-design-review rust-implementation ../my-project

# Dry run
python tools/install.py --dry-run all ../my-project

# Install and copy tools into target (so you can run new_design_log.py from project)
python tools/install.py all ../my-project --with-tools
```

### Examples (Windows)

```powershell
# All Rust packs into a project folder next to the hub
python tools/install.py all ..\my-project

# One or more packs
python tools/install.py rust-design-review rust-implementation ..\my-project

# Install and copy tools into target
python tools/install.py all ..\my-project --with-tools
```

**Note:** Target must be **outside** the hub repo (e.g. `../my-project`). The installer blocks installing into the hub itself.

## Which pack do I use?

| Pack | Use when you want… |
|------|---------------------|
| **rust-design-review** | Design-first workflow: questions before drafting, design review bar, ADR creation, decision summaries. |
| **rust-implementation** | Implementation discipline: small diffs, no scope creep, verification loop (fmt/clippy/test), anti-footguns. |
| **rust-testing** | TDR (failing test first), add-tests-only, deterministic tests, fixtures. |
| **rust-review** | PR review checklist, risky-changes scan (unsafe, unwrap, new deps, API breaks). |

You can install multiple packs; they merge into a single `.cursor/`. Commands are namespaced by pack (e.g. `/rust-design-review__design-review`) so names do not collide. See [CATALOG.md](CATALOG.md) for the full command list.

## Design log (deterministic numbering)

To create the next design log file **without guessing the number**:

- **If you used `--with-tools`:** from your **project** root run:  
  `python tools/new_design_log.py --slug short-name`
- **If you use the hub as a submodule:** from the hub root run:  
  `python tools/new_design_log.py --slug short-name --dir /path/to/your/project/.cursor/design-log`

## Validation

From the cursor-hub repo root:

```bash
python tools/validate_packs.py
```

Checks that every pack has `pack.yml`, rules have valid frontmatter, commands follow the `pack-name__command-name` convention and are non-empty, and there are no duplicate command names per pack.

## Optional: export design logs

`tools/export_design_logs_mongo.py` is a **stub**: it reads `.cursor/design-log/*.md` (by default), extracts metadata (number, slug, title, date), and prints JSON lines. A future version could push to MongoDB if `MONGO_URI` (and optionally `MONGO_DB`) are set; see the script docstring and [docs/pack-versioning.md](docs/pack-versioning.md) for compatibility notes.

## Docs

- [examples/feature-workflow.md](examples/feature-workflow.md) — Sample: design → implement → test → review (commands per step).
- [docs/using-packs.md](docs/using-packs.md) — Task → command, rules vs commands vs agents.
- [CATALOG.md](CATALOG.md) — Packs and primary commands.
- [docs/cursor-primitives.md](docs/cursor-primitives.md) — Rules vs commands vs subagents.
- [docs/authoring-guidelines.md](docs/authoring-guidelines.md) — Sizing and writing commands (including command naming).
- [docs/pack-versioning.md](docs/pack-versioning.md) — Versioning and compatibility.

## License

[MIT](LICENSE). See [CONTRIBUTING.md](CONTRIBUTING.md) if you want to contribute.
