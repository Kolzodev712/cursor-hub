---
name: rust-best-practices
description: >-
  Applies idiomatic Rust: API design per rust-lang API guidelines naming/interop/docs/predictability
  futures, plus project layout, errors, concurrency, perf, security, and tooling (rustfmt/clippy/test).
  Use when writing or reviewing Rust, public APIs, crates, async, unsafe boundaries, semver, or when
  the user mentions Rust standards, idioms, rustdoc, Send/Sync errors, clippy, or cargo.
---

# Rust best practices

## When this skill applies

- Designing or refactoring **public APIs**, modules, crates, traits, macros, builders.
- **Reviews** where Rust idioms, semver, docs, errors, unsafety, or async boundaries matter.
- After **compilation/lifetime/Send/Sync/clippy** issues where pattern choice drives the fix.

## Priority sources (consult details in reference files)

1. **[Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)** — authoritative API bar; summarized in [reference-api-guidelines.md](reference-api-guidelines.md).
2. **Project layout, security, tooling, testing** — distilled from Project Rules Rust in [reference-projectrules.md](reference-projectrules.md) (upstream: [projectrules.ai Rust](https://www.projectrules.ai/rules/rust)).

Prefer **official guidelines** where they conflict with generic prose.

## Verification loop (hands-on Rust)

Unless the repo agrees otherwise:

- Format: `cargo fmt --all` (often after `cargo fmt --all -- --check`).
- Lint: `cargo clippy --fix --allow-dirty --all-targets --all-features -- -D warnings`.
- Tests: `cargo test --all-features`; add `cargo check --all-targets --all-features` / `cargo audit` when relevant.

Prefer project `justfile` equivalents when present.

## API design — condensed checklist

Work through Naming → Interoperability → Documentation → Predictability → Flexibility → Type safety → Dependability → Debuggability → Future-proofing → Necessities before stabilizing APIs. Canonical labels (C-…) and full rationale live in the guideline chapters:

| Area | Highlights | Detail |
|------|-------------|--------|
| Naming | RFC 430 casing; `as_`/`to_`/`into_`; iterators `iter`/`iter_mut`/`into_iter` | [naming](https://rust-lang.github.io/api-guidelines/naming.html) |
| Interoperability | Common traits (`Debug`, `Clone`, …); implement `From`/`TryFrom`/`AsRef`/`AsMut` not `Into`; good errors (`Error + Send + Sync`); serde behind `serde` feature | [interoperability](https://rust-lang.github.io/api-guidelines/interoperability.html) |
| Macros | Evocative syntax; compose with attrs; visibility; flexible `$ty` fragments | [macros](https://rust-lang.github.io/api-guidelines/macros.html) |
| Documentation | Crate + item examples; **`?`** in docs not `unwrap`/`try!`; Errors / Panics / Safety sections | [documentation](https://rust-lang.github.io/api-guidelines/documentation.html) |
| Predictability | Conversions on most specific type; methods vs free fns with receiver; no out-params; sensible `ops`/`Deref` | [predictability](https://rust-lang.github.io/api-guidelines/predictability.html) |
| Flexibility | Expose intermediate results; generics over needless concrete types; object-safe traits when useful | [flexibility](https://rust-lang.github.io/api-guidelines/flexibility.html) |
| Type safety | Newtypes; meaningful enums vs booleans; `bitflags` for flags; builders for heavy construction | [type-safety](https://rust-lang.github.io/api-guidelines/type-safety.html) |
| Dependability | Prefer types enforcing invariants over “accept anything”; destructor infallibility / blocking guidance | [dependability](https://rust-lang.github.io/api-guidelines/dependability.html) |
| Debuggability | `Debug` on public types; non-empty Debug | [debuggability](https://rust-lang.github.io/api-guidelines/debuggability.html) |
| Future proofing | Private fields / sealed traits / avoid redundant derives-as-bounds on generics | [future-proofing](https://rust-lang.github.io/api-guidelines/future-proofing.html) |
| Necessities | Stable public deps for stable crates; permissive licensing alignment | [necessities](https://rust-lang.github.io/api-guidelines/necessities.html) |

Full one-page checklist: [checklist.html](https://rust-lang.github.io/api-guidelines/checklist.html).

## Error and panic policy

- **Libraries:** Fallible APIs return `Result<_, E>` with a real error type implementing `std::error::Error` (+ `Send + Sync`) where surfaced across threads/sync boundaries; prefer `thiserror`/typed errors vs `()` / stringly errors.
- **Applications:** `anyhow`-style ergonomics acceptable at the boundary layer if the team agrees.
- **`panic!`/`unwrap`/`expect`:** Reserve for invariant violations or prototypes; justified `expect("…")` with non-null internal reasons.
- **Unsafe:** Smallest capsule; document **Safety** invariants; Miri / tests where subtle.

## Security and input (applications / networking)

Treat untrusted bytes and strings hostile: bounded reads, parameterized queries / encoding, sanitize outputs, bounded allocation, timeouts, TLS with correct cert verification. Never shell-out with interpolated user strings. Prefer checked integer ops at trust boundaries.

## Repo layout reminders

- Typical tree: `src/{lib.rs,main.rs,bin/,…}`, **`tests/`** integration, **`benches/`**, **`examples/`**, `Cargo.toml` / **`Cargo.lock` committed for binaries**.
- Prefer **feature flags** additive; **`no_std`/std** spelled `std`, not placeholders like `with-std`.
- Respect **semver** when changing public signatures or trait impls callers rely on.

## Anti-patterns to flag early

Unnecessary `clone()`, widened `.unwrap()`, `unsafe` leakage, ignoring warnings, ambiguous `bool`/`Option` APIs, **`Deref`** on non-smart-pointer types to inject methods, public fields that destroy invariants.

## Conflict resolution

Official **Rust API Guidelines** win over anecdotal prose. When scope is ambiguous, note trade-offs briefly and steer toward reversible changes (additive APIs, deprecation path).
