# Example: one feature from design to review

Scenario: add a "config from env" feature to a Rust binary. Commands to use at each step.

---

**1. Design**

- Ask in chat: *"How would we add config loaded from env vars (PREFIX_*) for the binary?"*  
  → Senior-teacher: agent replies with questions first. Answer them or say *"draft it"*.
- Create the design log:  
  **`/adr-new`** — *slug: config-from-env. Background: we need env-based config. Problem: load PREFIX_* into a struct. Design: Config struct, validation, used in main.*  
  Or let the agent offer: *"Want this in a design log?"* → say yes.
- Optional one-off review:  
  **`/design-review`** — *Review the config-from-env approach: env vs file, validation, defaults.*

---

**2. Implement**

- **`/implement-module`** — *Implement design-log/001-config-from-env.md. Go phase by phase (types, then load, then wire into main).*  
  Agent will follow the log, run fmt/clippy/test after each phase, append Implementation Results.

---

**3. Test**

- Add tests only (no prod changes):  
  **`/add-tests-only`** — *Add tests for Config: valid env, missing required var, invalid value.*  
  Agent adds tests/fixtures and justifies coverage.
- Bugfix with test first:  
  **`/bugfix-tdr`** — *Config panics when PREFIX_PORT is not a number.*  
  Agent writes failing test, then fix, then verification.

---

**4. Review**

- **`/pr-review`** — *Review the config-from-env changes in src/main.rs and src/config.rs.*  
  Agent gives file-by-file, must-fix vs nice-to-have.
- **`/risky-changes-scan`** — *Same files.*  
  Agent flags unwrap, panics, new deps, API breaks.

---

**Summary**

| Step   | Command            | What you say (example) |
|--------|--------------------|-------------------------|
| Design | `/adr-new` or offer | slug + topic, or "yes" when offered |
| Review design | `/design-review` | describe the approach to review |
| Implement | `/implement-module` | design-log/NNN-name.md, phases |
| Add tests | `/add-tests-only` | what to cover |
| Bugfix | `/bugfix-tdr` | describe the bug |
| Review code | `/pr-review` | files or diff |
| Risk scan | `/risky-changes-scan` | files or diff |
