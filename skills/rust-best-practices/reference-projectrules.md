# Distilled Rust practices (layout, patterns, tooling)

Condensed from the **Project Rules** Rust playbook ([projectrules.ai/rules/rust](https://www.projectrules.ai/rules/rust)) for use with **`rust-best-practices`**. Use [SKILL.md](SKILL.md) + **[reference-api-guidelines.md](reference-api-guidelines.md)** for crate **API surface** specifics.

## Structure

- Typical roots: **`src/`** (`main.rs`, `lib.rs`, optional **`bin/`**), **`tests/`** integration, **`examples/`**, **`benches/`** (e.g. Criterion).
- **`Cargo.toml`**: edition, deps, **`[features]`** additive semantics; **`Cargo.lock`** for binaries pinned in CI.
- Module files **`snake_case.rs`**; **`mod` / `pub mod`** intentionally; expose minimal surface **`pub`** / **`pub(crate)`**.

## Patterns

- Ownership first: clones only when mandated by API or proven necessary.
- Prefer **`Result` + `?`**, enums for errors (`thiserror` in libs; `anyhow` often at bin boundary).
- Concurrency: message passing (`std::sync::mpsc` / async channels where appropriate); shared state behind **`Arc<Mutex<_>>`/atomics**/typed actors; parallelism via **`rayon`** when workloads fit.
- Async: **`async fn`/`await`**; **`Send`** bounds at spawn boundaries; propagate cancellation/`JoinError` thoughtfully.

## Performance

Profile before rewriting (`perf`, **`cargo flamegraph`**, `puffin`, etc.). Prefer iterators and stack where hot; benchmarks (`criterion`) to guard regressions. Release profile: **`lto`**, stripping symbols sensible for deploy artifacts.

## Security (high level)

Validate & bound external input (files, nets, subprocess args). Prefer typed APIs over stringly shell. Avoid secrets in-repo; encrypt at rest/transit TLS; parameterized DB / sanitization paths as domain requires.

## Testing

Unit tests **`#[cfg(test)]`** colocated or `tests/` sibling modules; integration tests **`tests/`** crate root; table-driven/param cases for combinatorics. Mock via traits/`mockall`/adapters sparingly consistent with project norms.

## Tooling baseline

**`rustfmt`**, **`clippy`** (`-D warnings` CI), **`rust-analyzer`**. CI: cache target, **`cargo build`**, **`test`**, **`clippy`** (fmt check optional parity with hub packs).
