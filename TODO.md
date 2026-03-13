# TODO: Cursor-hub potential improvements

Suggested improvements for the hub. Items are grouped by type and ordered by suggested priority.

---

## 1. Workflow improvements

### 1.1 Human-in-the-loop: "present before writing"

- [ ] Add an explicit rule (or section in `_shared` or design-log) that: for generated artifacts (new rules, new commands, new design log sections beyond the template), **present the full draft to the user and wait for explicit approval before writing files**.
- [ ] Ensure workflow commands and design-log methodology reference this where relevant (e.g. when creating a new rule or appending to a log).

### 1.2 Language × topic rules (Rust idioms)

- [ ] Add a **language-idiom layer** that complements existing workflow rules.
- [ ] For Rust: add the following rule files as a new pack or merge into `rust-implementation`:
  - [ ] `rust-design-patterns.mdc` (iterators, newtype, extension traits, `non_exhaustive`, `Result<Option<T>,E>`)
  - [ ] `rust-testing.mdc` (unit vs integration, property testing, miri, coverage) — reconcile with existing `rust-testing` pack
  - [ ] `rust-error-handling.mdc`
  - [ ] Optionally: `rust-project-organization.mdc`, `rust-tooling.mdc`
- [ ] Keep rules short (<50 lines), glob-activated, with good/bad examples.

### 1.3 Security as a first-class agent

- [ ] Add a **security pack** (e.g. `packs/cursor/security/` or similar):
  - [ ] One agent file covering: code vulnerabilities, dependency audit, secrets, auth, crypto, misconfiguration, CI/CD, severity levels, report format.
  - [ ] Optionally: a slash command (e.g. `/security-audit` or `security__standalone-audit`) that triggers a security review.
- [ ] Document in CATALOG.md and README; ensure it can be installed alongside existing packs.

### 1.4 Command-authoring reference

- [ ] Add a **command-authoring reference** (e.g. in `docs/command-authoring-examples.md` or a section in `docs/authoring-guidelines.md`):
  - [ ] Short "command template" (objective, steps, constraints, output).
  - [ ] 2–3 full examples (e.g. code review, run tests and fix, create PR) that pack authors can copy and adapt.
- [ ] Link from README or CATALOG so new command authors have a clear starting point.

---

## 2. Utilities and docs the hub lacks

### 2.1 AGENTS.md

- [ ] Add **AGENTS.md** at repo root:
  - [ ] Purpose of the hub (design-log, workflow, packs).
  - [ ] Design-log and workflow as non-negotiable; where packs, commands, and rules live.
  - [ ] When adding new packs/commands: follow authoring-guidelines and present drafts for approval.
  - [ ] Keep it a single "AI contract" file for contributors and agents working on the hub itself.

### 2.2 Rules vs commands vs agents (and skills) table

- [ ] Add a **compact comparison table** to `docs/cursor-primitives.md` (and/or README). The doc already has Rules/Commands/Agents in prose; add one table with columns: location, format, how activated, purpose, scope. Rows: Rules, Commands, Agents, (Skills if adopted). Quick reference for choosing or authoring.

### 2.3 Rule templates and naming convention

- [ ] Add a **rule templates** section to `docs/authoring-guidelines.md` (it already has naming and frontmatter; extend with copy-paste templates):
  - [ ] One "alwaysApply" template and one "globs" (file-scoped) template.
  - [ ] Naming convention for language-scoped rules: e.g. `{language}-{concern}.mdc`.
  - [ ] Examples for common rule types (always-on, file-scoped, testing, API).

### 2.4 Generate-* skills (meta/authoring)

- [ ] Decide where skills live: hub repo only (for maintainers) vs optional pack that installs into a project’s `.cursor/skills/`.
- [ ] If adopting in hub:
  - [ ] Copy or adapt **generate-rules** skill (gather requirements → draft → present → write after approval).
  - [ ] Copy or adapt **generate-commands** skill (same workflow for slash commands).
  - [ ] Optionally: **generate-subagents**, **generate-skills**.
- [ ] Ensure skills use hub’s paths and naming (e.g. `.cursor/design-log/`, pack names).
- [ ] Document in README or a new "Meta / authoring" section.

### 2.5 Language-aware install (optional)

- [ ] Evaluate demand for "install by language" (e.g. `install.py --lang rust python`).
- [ ] If desired: add a **language-oriented front-end** to `tools/install.py`:
  - [ ] Map languages to predefined pack sets (e.g. rust → design-log + rust-* packs).
  - [ ] Optional interactive mode (e.g. questionary) to choose languages and extras.
  - [ ] Reuse existing copy/install logic; no change to pack layout.

### 2.6 Publishable CLI package (optional)

- [ ] Only if the goal is "install cursor-hub from PyPI/private index":
  - [ ] Add Python package layout (`pyproject.toml`, `src/` or equivalent).
  - [ ] Build step that bundles packs (or a minimal set) into the package (e.g. `_bundled_data/` or similar).
  - [ ] Script or command (e.g. `cursor-hub install <target>`) that runs the same install logic as `tools/install.py`.
  - [ ] Document install via `uv tool install` or `pip install`.
  - [ ] If publishing: add **justfile** (or Makefile) and a **build script** (e.g. `build_data.sh`) for wheel builds. If staying with "clone + install.py": optionally add a justfile for `validate_packs`, `install.py --dry-run`, and future steps.

### 2.7 Cursor plugins and MCP (exploration)

- [ ] **Explore Cursor plugins:** Research what Cursor plugins are, how they are built and distributed, and how they integrate with the IDE (docs, SDK, marketplace if any).
- [ ] **Make this repo a plugin:** Document or implement a path to ship cursor-hub as a Cursor plugin (e.g. install from IDE, one-click add of packs/rules/commands to a project).
- [ ] **MCP server support:** Explore how to add MCP (Model Context Protocol) server support — e.g. a small MCP server that exposes hub capabilities (install packs, list commands, validate design log) so the agent can call them via MCP tools; or document how projects using the hub can add their own MCP servers. Capture findings in a design log or doc.

---

## 3. Summary checklist (by priority)

| Priority | Item | Status |
|----------|------|--------|
| 1 | Add AGENTS.md at repo root | [ ] |
| 2 | Add rules/commands/agents (and skills) table to docs | [ ] |
| 3 | Add "present before writing" to shared rules or design-log | [ ] |
| 4 | Add command-authoring examples doc | [ ] |
| 5 | Add Rust idiom rules (new pack or merge into rust-implementation) | [ ] |
| 6 | Add security pack (agent + optional command) | [ ] |
| 7 | Add rule templates doc | [ ] |
| 8 | Adopt generate-rules and generate-commands skills (hub or meta pack) | [ ] |
| 9 | Optional: language-aware install front-end | [ ] |
| 10 | Optional: publishable CLI package + justfile/build script | [ ] |
| 11 | Explore Cursor plugins; make repo a plugin; add MCP server support | [ ] |

---

## 4. Notes

- **Role agents:** The hub already has the concept — agents are personas (design critic, implementer, reviewer, test author, etc.) in `.cursor/agents/`, and you use them by running the **matching command**. No separate "role agents pack" needed.
- **1.1 and 2.1:** The "present before writing" rule (1.1) and AGENTS.md (2.1) should align — both state that drafts are presented for approval before writing; implement once and reference in both.
- **Design log:** Consider creating a design log (e.g. `design-log/NNN-hub-improvements.md`) to record decisions as you implement these items.
- **Validation:** After adding new packs or rules, run `python tools/validate_packs.py` and update CATALOG.md and README as needed.
