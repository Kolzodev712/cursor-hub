# cursor-hub corrective review (local candidate)

**Audited base (remote):** `a9390b96f74fdb37c0d17b3489bd567ca5cd6068`  
**Working tree:** corrective changes **not committed** (per review gate).  
**External bundle:** No `APPLY.md` / `MANIFEST.json` / `apply.py` bundle was present in the repo or agent stores; corrections were applied directly against the checkout at `a9390b9`.

## Confirmed defects on base (severity)

| ID | Severity | Issue |
|----|----------|--------|
| D1 | **High** | Component interview traits/responsibility not round-tripped in `components.json` (reload lost routing inputs). |
| D2 | **High** | `explicit_sync` (mutex) incorrectly mapped to **atomics** decision domain. |
| D3 | **High** | Setup could be structurally “complete” without explicit final **W** approval (`approved_at` missing). |
| D4 | **Medium** | Read gate credited path-only Reads; no `additional_context` for small docs; no `preCompact` invalidation. |
| D5 | **Medium** | Path traversal not rejected on classified write paths. |
| D6 | **Low** | Summary could mis-report domains when in-memory traits missing (partially addressed). |

## Corrective changes (this candidate)

- **Schema v2** (`DOCTRINE_SETUP_SCHEMA_VERSION = 2`): `approved_at`, `awaiting_final_approval`, `approval_revision` in `setup.json`.
- **Staging** (`.cursor/doctrine/.setup-staging.json`) + **publication journal** (`.setup-publication.journal.json`) with per-file `os.replace`.
- **Final W required** to approve; `C`/`Q`/empty/invalid summary input does not approve.
- **`components.json` `interview` block** preserves responsibility, all traits (incl. `atomics_usage` vs `explicit_sync`), extras, and `suggested_doctrine_refs`.
- **Routing:** concurrency only when `concurrent_access=yes`; atomics only when `atomics_usage=yes` (not mutex alone).
- **Hooks:** `preCompact` clears session read credits; path-only Read may return `additional_context` (Cursor docs: hook JSON output — **live editor not exercised here**).
- **Tests:** `tests/test_doctrine_corrective.py` + updates to existing doctrine tests.

## Verification commands (this environment)

```text
python3 tools/validate_packs.py                 — passed
python3 tools/validate_doctrine_sources.py      — passed
python3 -m unittest discover -s tests -v        — OK (35 tests)
```

**Python runtimes tested:** `python3.12.3` only (`python3.10` / `python3.11` / `python3.13` not present on this host).

**Test harness fix (review):** Wizard scripts on empty installs have no candidate-component list, so `s` (skip candidates) was mis-consumed as “add custom?” and shifted `n`/`w` off the summary prompt. Helpers now use `n` + `w` only for the components step when there are no scan candidates.

## Live Cursor / hooks

- **Source-backed:** [Cursor Hooks docs](https://cursor.com/docs/hooks) fetched 2026-10-06 (`preCompact`, JSON stdin/stdout, `permission` / deny exit 2).
- **Live editor:** **Unverified** — no sanitized payload capture from this IDE session; `additional_context` behavior is implemented per docs but not end-to-end tested in Cursor.

## Terminal walkthrough

**2026-10-06 (this pass):** `script(1)` PTY against a fresh `engineering-doctrine` install at `/tmp/doctrine-pty-test`:

```bash
cursor-hub install engineering-doctrine /tmp/doctrine-pty-test
# heredoc-fed inputs: repo text, objectives 1+3, rank, Y scope, one invariant + D, workload 2, add-custom N, summary W
cursor-hub doctrine setup /tmp/doctrine-pty-test
```

- Summary showed `Setup result: INCOMPLETE` until **W** (schema v2 gate).
- Exit **0**; `setup.json`: `schema_version: 2`, `status: COMPLETE`, `approved_at` set (UTC).
- **Not exercised in PTY this pass:** cancel at summary, `--review-unknowns`, component interview with traits, reinstall.

## Known limitations / unverified

- Full **10-area** checklist (installer manifest retirement, SQLite state, multi-file patch adapter, exhaustive unknown-review field classes, hook merge refresh policy) is **not fully implemented** in this candidate — only items tied to confirmed D1–D5.
- **Four byte-identical hook modules:** repo ships **two** hub-synced modules (`doctrine_enforcement.py`, `doctrine_setup_gate.py`).
- **v1 → v2 migration:** existing `setup.json` with `schema_version: 1` → `STALE_SCHEMA`; requires interactive setup/re-approval (legacy markdown preserved).
- **Power-loss:** journal records attempts; not a full transactional DB.
- **ll-cache:** not installed (per review scope).

## Recommendation

Review the local diff, re-run PTY walkthrough + `discover -s tests -v`, then commit/push when you authorize. First pilot target remains a **disposable ll-cache clone**, not trading-system.
