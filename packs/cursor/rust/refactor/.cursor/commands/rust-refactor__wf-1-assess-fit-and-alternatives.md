# Refactor — assess fit and alternatives (rust-refactor WF Step 1)

**Goal:** Decide whether this crate, subsystem, abstraction, or dependency **still earns its place** using **engineering best practices** and **idiomatic Rust**, and whether **better alternatives** exist (different crate, restructuring, shrinking scope). **Analysis only** unless the user asks for a spike; defer large edits to Step 2.

**Follow with:** `/rust-refactor__wf-2-execute-refactor` after you have explicit agreement to refactor or replace.

## Steps

1. **Check existing logs:** Read `./.cursor/design-log/` for related entries; extend one workstream log if it already covers this refactor.
2. **Scope:** Identify the boundary under review (crate, module cluster, trait object layer, FFI edge, persistent dependency chain). State what problem it serves today.
3. **Systems / tech assessment:** Lifecycle, coupling to callers, observability/debuggability, security and trust boundaries, migration and rollback, operational cost. Note gaps vs what the domain typically expects (e.g. config, versioning, deterministic behavior).
4. **Rust idioms and API quality:** Public surface, stability story, errors vs panics at boundaries, async vs blocking, generics vs trait objects, duplication, visibility, `#![deny(unsafe_code)]`-style conventions where relevant, docs and semver risk.
5. **Usefulness verdict:** Is this still justified? Categories: **keep with minor refactor**, **refactor internally**, **replace dependency or pattern**, **remove / merge / split crate**, **needs spike** (time-box proof).
6. **Alternatives (concrete):** List 1–3 options with **pros/cons**, **estimated effort**, **risks**, and **when you would pick each**. Avoid generic “rewrite”; name specific patterns or crates when applicable (and cite repo evidence).
7. **Recommendation:** Preferred path for Step 2, **acceptance criteria** for “success,” and **signals** that would mean abandoning this direction.
8. **Record in design log (mandatory):** Append section **Refactor assessment** with the verdict, alternatives, recommendation, and verification plan (what we will measure before/after). If no log exists, run `python .cursor/tools/new_design_log.py --slug <short-name>` (or fallback numbering from `./.cursor/design-log/`). **Workflow stamp:** Append exactly one standalone line `[cursor-hub workflow] step=refactor-assessment`.
9. **Verify:** Run `python .cursor/tools/validate_workflow_design_log.py --step refactor-assessment` from the project root until it passes.

Do **not** start a broad implementation in this step unless the user explicitly requests a bounded spike to inform the assessment.
