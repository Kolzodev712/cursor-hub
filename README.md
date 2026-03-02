# AI_Rules_Kolzo

A **public Cursor AI hub**: modular rules, commands, and agents for guiding AI assistants. The content is **language- and model-agnostic** in principle; this repository currently ships **Cursor-only** instructions (rules, slash commands, subagents), with a **Rust-first** set of packs.

## What’s in the repo

- **Packs** under `packs/cursor/`: each pack is a folder with `.cursor/rules/`, `.cursor/commands/`, and optionally `.cursor/agents/`. Install one or more packs into your project.
- **Shared foundation** (`_shared`): design-log methodology and when-to-log guidance. It is always installed when you install any other pack.
- **Tools** under `tools/`: install packs, validate pack layout, create design logs with deterministic numbering, and an optional export stub. They use the Python standard library only; no `pip install` needed (see `tools/requirements.txt`).

## Quick install

1. Clone this repo (or add it as a submodule).

2. **Recommended:** From **this repo**, run: **what to install**, then **target directory last**. Use **`all`** for every Rust pack:
   ```bash
   cd C:\Users\nikol\Desktop\AI_Rules_Kolzo
   python tools/install.py all ..\test-project
   ```
   The `.` means “current directory”, so create or go to your project folder first, or use a path like `.\my-project` (folder next to the hub) or `C:\Users\nikol\Desktop\my-project`.  
   Use two dots `..\test-project` for the folder next to the hub; one dot would create inside the hub (script blocks that).

3. **Alternative:** If you’re already inside your project folder, you can install into the current directory:
   ```bash
   cd C:\Users\nikol\Desktop\my-project
   python C:\Users\nikol\Desktop\AI_Rules_Kolzo\tools\install.py rust-design-review
   ```
   (No target path = install into current directory.)

4. This merges the `_shared` pack and the chosen pack(s) into your project’s `.cursor/` and creates `design-log/README.md` if missing.

**Examples (run from AI_Rules_Kolzo; use your real path, not the literal “path/to/project”):**

- **All Rust packs (target last):**  
  `python tools/install.py all ..\test-project`
- One or more packs:  
  `python tools/install.py rust-design-review ..\test-project`
- Dry run:  
  `python tools/install.py --dry-run all ..\test-project`
- Overwrite:  
  `python tools/install.py --overwrite all ..\test-project`

## Which pack do I use?

| Pack | Use when you want… |
|------|---------------------|
| **rust-design-review** | Design-first workflow: questions before drafting, design review bar, ADR creation, decision summaries. |
| **rust-implementation** | Implementation discipline: small diffs, no scope creep, verification loop (fmt/clippy/test), anti-footguns. |
| **rust-testing** | TDR (failing test first), add-tests-only, deterministic tests, fixtures. |
| **rust-review** | PR review checklist, risky-changes scan (unsafe, unwrap, new deps, API breaks). |

You can install multiple packs; they merge into a single `.cursor/` (same command name in two packs overwrites when using `--overwrite`).

## Design log (deterministic numbering)

To create the next design log file **without guessing the number**, run from your **project** root:

```bash
python tools/new_design_log.py --slug short-name
```

The script creates `design-log/NNN-short-name.md` and prints its path. Copy the `tools/` folder into your project, or run the script from this repo and pass `--dir` to point at your project’s design-log directory.

## Validation

From the AI_Rules_Kolzo repo root:

```bash
python tools/validate_packs.py
```

Checks that every pack has `pack.yml`, rules have valid frontmatter, commands are non-empty, and there are no duplicate command names per pack.

## Optional: export design logs

`tools/export_design_logs_mongo.py` is a **stub**: it reads `design-log/*.md`, extracts metadata (number, slug, title, date), and prints JSON lines. A future version could push to MongoDB if `MONGO_URI` (and optionally `MONGO_DB`) are set; see the script docstring and [docs/pack-versioning.md](docs/pack-versioning.md) for compatibility notes.

## Docs

- [examples/feature-workflow.md](examples/feature-workflow.md) — Sample: design → implement → test → review (commands per step).
- [docs/using-packs.md](docs/using-packs.md) — Task → command, rules vs commands vs agents.
- [CATALOG.md](CATALOG.md) — Packs and primary commands.
- [docs/cursor-primitives.md](docs/cursor-primitives.md) — Rules vs commands vs subagents.
- [docs/authoring-guidelines.md](docs/authoring-guidelines.md) — Sizing and writing commands.
- [docs/pack-versioning.md](docs/pack-versioning.md) — Versioning and compatibility.

## License

See repository license file.
