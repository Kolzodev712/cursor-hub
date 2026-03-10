# Example: one feature from design to review

Scenario: add a "config from env" feature to a Rust binary. Use the **main workflow** (design, implement, test — in any order or on their own), or pick **standalone** commands when you have a specific need.

---

## Main workflow (use in any order or on their own)

**Design review** (rust-design-review)

- Run **`/rust-design-review__wf-1-design-review`** — *"How would we add config loaded from env vars (PREFIX_*) for the binary?"*  
  Agent: questions, alternatives, recommended option, risks, verification. Answer and refine until you have an approved design. **The design log is created or updated automatically at the end** (Design discussion section).
- Or ask in chat first; senior-teacher rule gives questions only until you say "draft it".

**Implement** (rust-implementation)

- Run **`/rust-implementation__wf-1-implement-module`** — *Implement .cursor/design-log/001-config-from-env.md. Go phase by phase (types, then load, then wire into main).*  
  Agent follows the log, runs fmt/clippy/test after each phase. Implementation Results are appended to the design log automatically.

**Add tests** (rust-testing)

- **`/rust-testing__wf-1-add-tests-only`** — *Add tests for Config: valid env, missing required var, invalid value.*  
  Only tests/fixtures; justifies coverage. Test session is recorded in the design log automatically.

**Bugfix (separate workflow):** For a small bug use **`/rust-bugfix__standalone-fix-small-bug`**. For a non-trivial bug use the 3-step flow: **`/rust-bugfix__wf-1-investigation`** → **`/rust-bugfix__wf-2-proposed-solution`** → **`/rust-bugfix__wf-3-resolution`** (e.g. *Config panics when PREFIX_PORT is not a number* — each step records in its own design log).

**Manual design log:** To create a new log without running a workflow step (e.g. start a log before design), use **`/design-log__create`** — *slug: config-from-env*.

**Optional — Review**

- **`/rust-review__standalone-pr-review`** — *Review the config-from-env changes in src/main.rs and src/config.rs.*  
- **`/rust-review__standalone-risky-changes-scan`** — same files; flags unwrap, panics, new deps, API breaks.

---

## Standalone commands (when you need them)

Use these **instead of** or **in addition to** the main workflow when they fit.

**Gates (strict / dev-led)** — You provide all inputs; the model refuses to propose or write until you do.

| Command | Use when |
|---------|----------|
| `/rust-design-review__gate-design` | You want to drive the full architecture yourself; get BLOCKED + MISSING + questions until complete, then PROPOSED PLAN only. |
| `/rust-implementation__gate-impl` | You want to define types, signatures, and wiring yourself; then get only function bodies. |
| `/rust-testing__gate-test` | You want to define the full test breakdown yourself; then get tests exactly as specified. |

**Other standalone**

| Command | Use when |
|---------|----------|
| `/rust-design-review__standalone-decision-summary` | You want a short block summarizing the decision and rejected alternatives (e.g. to paste into a log). |
| `/rust-implementation__standalone-refactor-safe` | Refactor without behavior change; 3–6 steps, tests after each. |
| `/rust-review__standalone-pr-review`, `/rust-review__standalone-risky-changes-scan` | Review a PR or scan for risky patterns. |
| `/documentation__standalone-architecture-doc`, `standalone-feature-doc`, `standalone-workflow-doc`, `standalone-specific-workflow-doc`, `standalone-bug-summary` | Create architecture, feature, workflow, or bug-summary docs. |

---

## Summary table

| Step / need | Command | What you say (example) |
|-------------|---------|------------------------|
| **Main workflow** | | |
| Design review | `/rust-design-review__wf-1-design-review` | describe the approach to review (design log updated automatically) |
| Implement | `/rust-implementation__wf-1-implement-module` | .cursor/design-log/NNN-name.md, phases |
| Add tests | `/rust-testing__wf-1-add-tests-only` | what to cover |
| **Bugfix (separate)** | | |
| Small bug | `/rust-bugfix__standalone-fix-small-bug` | describe the bug |
| Non-trivial bug | wf-1: `/rust-bugfix__wf-1-investigation` → wf-2: `/rust-bugfix__wf-2-proposed-solution` → wf-3: `/rust-bugfix__wf-3-resolution` | investigation → solution → resolution |
| **Design log (manual)** | | |
| Create log | `/design-log__create` | slug + topic (when you want a log without running a workflow step) |
| Record step | `/design-log__record-step` | step type + context |
| **Standalone — gates** | | |
| Design gate | `/rust-design-review__gate-design` | provide full architecture; get PROPOSED PLAN at the end |
| Impl gate | `/rust-implementation__gate-impl` | provide types, signatures, wiring; get implementation only |
| Test gate | `/rust-testing__gate-test` | provide full test breakdown; get tests as specified |
| **Standalone — other** | | |
| Decision summary | `/rust-design-review__standalone-decision-summary` | summarize decision for log/ADR |
| Refactor | `/rust-implementation__standalone-refactor-safe` | refactor scope |
| Review / scan | `/rust-review__standalone-pr-review`, `standalone-risky-changes-scan` | files or diff |
| **Documentation** | | |
| Architecture doc | `/documentation__standalone-architecture-doc` | scope (repo/service) |
| Feature doc | `/documentation__standalone-feature-doc` | feature or area |
| Workflow doc | `/documentation__standalone-workflow-doc` | what workflow |
| Specific workflow doc | `/documentation__standalone-specific-workflow-doc` | which workflow in detail |
| Bug summary | `/documentation__standalone-bug-summary` | bug or fix to summarize |
