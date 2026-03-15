# cursor-hub

A **public Cursor AI hub**: modular rules, commands, and agents for guiding AI assistants. The content is **language- and model-agnostic** in principle; this repository ships **Cursor-only** instructions (rules, slash commands, agents) for **Rust**, **Python**, **JS/TS**, and **Terraform**, each with the same workflow structure (design-review → implementation → testing, plus bugfix and review).

## What's in the repo

- **Packs** under `packs/cursor/`: language-specific packs live in `packs/cursor/rust/`, `packs/cursor/python/`, `packs/cursor/js-ts/`, and `packs/cursor/terraform/` (each with design-review, implementation, testing, bugfix, review), plus shared packs `design-log`, `documentation`, `security`. Each pack has a `pack.yml` and optional `.cursor/rules/`, `.cursor/commands/`, `.cursor/agents/`. The installer creates `.cursor/design-log/` and copies scripts into `.cursor/tools/` in the target project. Install one or more packs into your project.
- **CLI and tools:** `cursor-hub` CLI (from `pip install -e .`) or `python tools/install.py` install packs; `tools/` also has validate_packs, new_design_log, and an optional export stub. When you install packs, scripts are copied into the target's `.cursor/tools/`. Use `pip install -e .` for the CLI, or run the script from the hub repo (see `tools/requirements.txt` if needed).

- **Shared foundation** (`_shared`): design-log methodology and when-to-log guidance. It is always installed when you install any other pack.

## Quick install

**Option 1 — CLI (recommended):** Install the hub in editable mode, then use the `cursor-hub` command from anywhere the hub repo is available:

```bash
# Clone or add as submodule
git clone https://github.com/your-org/cursor-hub.git .cursor-hub
cd .cursor-hub
pip install -e .

# Install packs into your project (from any directory that can see the hub)
cursor-hub install all /path/to/your/project
cursor-hub install --lang python all .          # current directory
cursor-hub install rust-design-review rust-implementation ../my-project
```

**Option 2 — Run the script from the hub repo:** No pip install; run the script from the hub directory:

```bash
cd .cursor-hub
python tools/install.py all /path/to/your/project
python tools/install.py --lang python all ../my-project
```

You can also run `python -m cursor_hub install all .` from the hub repo without installing the package.

The installer copies packs into the target's `.cursor/` (rules, commands, agents, design-log, tools). Then run `python .cursor/tools/new_design_log.py --slug <name>` from the target project root.

### Examples (Unix / macOS)

```bash
# CLI
cursor-hub install all ../my-project
cursor-hub install --lang python all .
cursor-hub install --dry-run all .

# Or script from hub repo
python tools/install.py all ../my-project
python tools/install.py --lang python all ../my-project
python tools/install.py rust-design-review rust-implementation ../my-project
```

### Examples (Windows)

```powershell
cursor-hub install all ..\my-project
cursor-hub install --lang python all ..
# Or: python tools\install.py all ..\my-project
```

**Note:** Target must be **outside** the hub repo (e.g. `../my-project`). The installer blocks installing into the hub itself.

## Which pack do I use?

| Pack | Use when you want… |
|------|---------------------|
| **design-log** | Design log creation and automatic recording after each workflow step (each pack's wf-1); manual `/design-log__create` and `/design-log__record-step`. |
| **rust-design-review** / **python-design-review** / **js-ts-design-review** / **terraform-design-review** | Design-first workflow: questions before drafting, design review bar, ADR creation, decision summaries. |
| **rust-implementation** / **python-implementation** / **js-ts-implementation** / **terraform-implementation** | Implementation discipline: small diffs, no scope creep, verification loop (language-appropriate: cargo/pytest, black/ruff, npm test, terraform fmt/validate). |
| **rust-testing** / **python-testing** / **js-ts-testing** / **terraform-testing** | Add-tests-only, deterministic tests, fixtures. |
| **rust-bugfix** / **python-bugfix** / **js-ts-bugfix** / **terraform-bugfix** | Fix small bugs (standalone) or non-trivial bugs (3-step workflow: investigation → proposed solution → resolution). Separate from main design/implement/test flow. |
| **documentation** | Standalone commands to create architecture docs, feature docs, workflow docs, and bug summaries. |
| **rust-review** / **python-review** / **js-ts-review** / **terraform-review** | PR review checklist, risky-changes scan (language-appropriate patterns). |
| **security** | Security audit agent and `/security__standalone-audit`: vulnerabilities, deps, secrets, auth, crypto, misconfiguration, CI/CD. |

You can install multiple packs; they merge into a single `.cursor/`. Commands are namespaced by pack (e.g. `/rust-design-review__wf-1-design-review`, `/python-design-review__wf-1-design-review`). Use the **main workflow** (design, implement, test) in any order or on their own — each pack numbers its own steps (e.g. wf-1). **Standalone** commands: gates, refactor, PR review, etc. See [CATALOG.md](CATALOG.md) for the full list.

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

## Languages

- Language profiles are built into the installer (CLI and `tools/install.py`) via the `--lang` flag.
- **`--lang rust`** installs: design-log, documentation, security, and all Rust packs (rust-design-review, rust-implementation, rust-testing, rust-bugfix, rust-review).
- **`--lang python`** installs: design-log, documentation, security, and all Python packs (python-design-review, python-implementation, python-testing, python-bugfix, python-review).
- **`--lang js-ts`** installs: design-log, documentation, security, and all JS/TS packs (js-ts-design-review, js-ts-implementation, js-ts-testing, js-ts-bugfix, js-ts-review).
- **`--lang terraform`** installs: design-log, documentation, security, and all Terraform packs (terraform-design-review, terraform-implementation, terraform-testing, terraform-bugfix, terraform-review).

Use `cursor-hub install --lang <language> all <target_dir>` (or `python tools/install.py ...` from the hub repo) to install the full set for a language.
## Meta / authoring

- **[AGENTS.md](AGENTS.md)** — Contract for contributors and agents working on the hub: purpose, where packs/commands/rules live, present drafts for approval.
- **Generate-* skills:** The hub can support authoring via Cursor skills (e.g. generate-rules, generate-commands) that follow the same workflow: gather requirements → draft → present → write after approval. Skills may live in the hub repo (for maintainers) or in an optional meta pack that installs into a project’s `.cursor/skills/`. If adopted, ensure skills use the hub’s paths and naming (`.cursor/design-log/`, pack names). See [AGENTS.md](AGENTS.md) and the present-before-writing rule in `_shared`.

## License

[MIT](LICENSE). See [CONTRIBUTING.md](CONTRIBUTING.md) if you want to contribute.
