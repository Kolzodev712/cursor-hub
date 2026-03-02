# Catalog of packs

Packs live under `packs/cursor/`. Each has a `pack.yml` and optional `.cursor/rules/`, `.cursor/commands/`, `.cursor/agents/`. Command filenames use the `pack-name__command-name` convention so installing multiple packs does not collide.

---

## _shared (foundation)

**Purpose:** Design-log methodology: design first, log decisions, append results. Always included when installing any other pack.

**Contents:**

- **Rules:** `design-log.mdc` — when to log, log structure (Background → Problem → Q/A → Design → Plan → Examples → Trade-offs → Verification → Implementation Results), deterministic creation via `tools/new_design_log.py --slug <name>`.

**No commands or agents.** Other packs add those.

---

## rust-design-review

**Purpose:** Question-first design, design review quality bar, ADR creation, decision summaries.

**Rules:**

- `senior-teacher.mdc` — First response: questions and challenge only; bypass phrases: "just do it", "no questions", "draft now".
- `rust-design-review.mdc` — Trade-offs, alternatives, constraints, acceptance criteria; align with design-log structure.

**Commands:**

| Command | Description |
|--------|-------------|
| `/rust-design-review__design-review` | Strict design review: critical questions, recommended option, risks, verification. |
| `/rust-design-review__adr-new` | Create a new design log via `new_design_log.py --slug <name>` and fill template. |
| `/rust-design-review__decision-summary` | Summarize final decision and why alternatives were rejected. |

**Agents:**

- `design-critic.md` — Skeptical reviewer; challenges assumptions and missing constraints.

---

## rust-implementation

**Purpose:** Small diffs, no scope creep, verification loop, Rust anti-footguns.

**Rules:**

- `rust-core.mdc` — Small diffs, no new deps unless asked, avoid unwrap/expect in prod; verification: `cargo fmt`, `cargo clippy -- -D warnings`, `cargo test`.
- `rust-anti-footguns.mdc` — Lifetimes/borrowing, cloning/allocations, error handling, unsafe policy.

**Commands:**

| Command | Description |
|--------|-------------|
| `/rust-implementation__implement-module` | Implement from an approved design log; cite log; stepwise edits; verification loop; append Implementation Results. |
| `/rust-implementation__refactor-safe` | Plan 3–6 steps; limit files per step; run tests after each step; show diff summary. |

**Agents:**

- `rust-implementer.md` — Correct Rust, minimal diffs, compile/test loop.

---

## rust-testing

**Purpose:** TDR, deterministic tests, fixtures, add-tests-only workflow.

**Rules:**

- `rust-testing.mdc` — Unit vs integration, deterministic tests, avoid fragile timing, fixtures, property tests when useful.

**Commands:**

| Command | Description |
|--------|-------------|
| `/rust-testing__bugfix-tdr` | Failing test first, then fix, then fmt/clippy/test. |
| `/rust-testing__add-tests-only` | No prod code changes; only tests/fixtures; justify coverage. |

**Agents:**

- `test-author.md` — Reproducible, meaningful tests; not coverage theater.

---

## rust-review

**Purpose:** PR review checklist, risky-changes scan.

**Rules:**

- `rust-review.mdc` — Checklist: correctness, API stability, error handling, performance, security, unsafe invariants, test adequacy; must-fix vs nice-to-have.

**Commands:**

| Command | Description |
|--------|-------------|
| `/rust-review__pr-review` | File-by-file findings with must-fix vs nice-to-have. |
| `/rust-review__risky-changes-scan` | Flag unsafe, unwrap, panics, new deps, public API breaks. |

**Agents:**

- `reviewer.md` — Strict reviewer; correctness and maintainability.

---

## Installing

From the cursor-hub repo root:

```bash
python tools/install.py <pack> [pack ...] <target_dir>
```

Example: `python tools/install.py rust-design-review rust-implementation /path/to/your/project`
