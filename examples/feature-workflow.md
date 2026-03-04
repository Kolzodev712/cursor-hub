# Example: one feature from design to review

Scenario: add a "config from env" feature to a Rust binary. Commands to use at each step.

---

**1. Design**

- Ask in chat: *"How would we add config loaded from env vars (PREFIX_*) for the binary?"*  
  → Senior-teacher: agent replies with questions first. Answer them or say *"draft it"*.
- **Strict design-first (hard gate):**  
  **`/rust-design-review__design-gate`** — Agent refuses to propose a solution until you provide complete architecture (modules, data flow, alternatives, etc.); responds with BLOCKED + MISSING + questions until then; then outputs PROPOSED PLAN only. Use when you want to drive the design yourself and only get a plan at the end.
- Create the design log:  
  **`/rust-design-review__adr-new`** — *slug: config-from-env. Background: we need env-based config. Problem: load PREFIX_* into a struct. Design: Config struct, validation, used in main.*  
  Or let the agent offer: *"Want this in a design log?"* → say yes.
- Optional one-off review:  
  **`/rust-design-review__design-review`** — *Review the config-from-env approach: env vs file, validation, defaults.*

---

**2. Implement**

- **`/rust-implementation__implement-module`** — *Implement .cursor/design-log/001-config-from-env.md. Go phase by phase (types, then load, then wire into main).*  
  Agent will follow the log, run fmt/clippy/test after each phase, append Implementation Results.
- **Strict API-first (hard gate):**  
  **`/rust-implementation__impl-gate`** — Agent refuses to write code until you provide types, error types, function signatures, and wiring; then implements only function bodies. Use when you want to own the API shape.

---

**3. Test**

- Add tests only (no prod changes):  
  **`/rust-testing__add-tests-only`** — *Add tests for Config: valid env, missing required var, invalid value.*  
  Agent adds tests/fixtures and justifies coverage.
- **Strict test-plan-first (hard gate):**  
  **`/rust-testing__test-gate`** — Agent refuses to write test code until you provide a full test breakdown (cases, assertions, unit/integration, fixtures); then implements tests exactly as specified. Use when you want to own the test plan.
- Bugfix with test first:  
  **`/rust-testing__bugfix-tdr`** — *Config panics when PREFIX_PORT is not a number.*  
  Agent writes failing test, then fix, then verification.

---

**4. Review**

- **`/rust-review__pr-review`** — *Review the config-from-env changes in src/main.rs and src/config.rs.*  
  Agent gives file-by-file, must-fix vs nice-to-have.
- **`/rust-review__risky-changes-scan`** — *Same files.*  
  Agent flags unwrap, panics, new deps, API breaks.

---

**Summary**

| Step   | Command            | What you say (example) |
|--------|--------------------|-------------------------|
| Design | `/rust-design-review__adr-new` or offer | slug + topic, or "yes" when offered |
| Design (hard gate) | `/rust-design-review__design-gate` | provide full architecture; get BLOCKED + MISSING until complete, then PROPOSED PLAN |
| Review design | `/rust-design-review__design-review` | describe the approach to review |
| Implement | `/rust-implementation__implement-module` | .cursor/design-log/NNN-name.md, phases |
| Implement (hard gate) | `/rust-implementation__impl-gate` | provide types, signatures, wiring; then get implementation only |
| Add tests | `/rust-testing__add-tests-only` | what to cover |
| Test (hard gate) | `/rust-testing__test-gate` | provide full test breakdown; then get tests exactly as specified |
| Bugfix | `/rust-testing__bugfix-tdr` | describe the bug |
| Review code | `/rust-review__pr-review` | files or diff |
| Risk scan | `/rust-review__risky-changes-scan` | files or diff |
