# cursor-hub corrective review (archive)

**Status:** Merged to `main` as **`7ab851dd75fd31720616bf585dbe5f56205a3df2`** (`fix(doctrine): close corrective gaps for gate, setup, and hooks`). This document records the review that led to that commit; it is not a description of uncommitted work.

**Audited base:** `a9390b96f74fdb37c0d17b3489bd567ca5cd6068`
**External bundle:** No `APPLY.md` / `MANIFEST.json` / `apply.py` bundle was present; corrections were applied directly in the checkout.

## Confirmed defects on base (severity)

| ID | Severity | Issue |
|----|----------|--------|
| D1 | **High** | Component interview traits/responsibility not round-tripped in `components.json` (reload lost routing inputs). |
| D2 | **High** | `explicit_sync` (mutex) incorrectly mapped to **atomics** decision domain. |
| D3 | **High** | Setup could be structurally “complete” without explicit final **W** approval (`approved_at` missing). |
| D4 | **Medium** | Read gate credited path-only Reads; no `additional_context` for small docs; no `preCompact` invalidation. **Addressed in 7ab851d:** mandatory context requires `full_text` or `hook_supplied`; path-only/partial do not unlock writes; `preCompact` clears credits; `additional_context` for path-only reads when hook supplies full file (≤512KB). |
| D5 | **Medium** | Path traversal not rejected on classified write paths. |
| D6 | **Low** | Summary could mis-report domains when in-memory traits missing (partially addressed). |

## Corrective changes (shipped in 7ab851d)

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
python3 -m unittest discover -s tests -v        — OK (52 tests at merge; 59 after fault-first pack added later)
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

- Full **10-area** checklist (installer manifest retirement, SQLite state, exhaustive unknown-review UX) remains **partial**; hook merge refresh and multi-path write extraction were added in 7ab851d.
- **Four byte-identical hook modules:** repo ships **two** hub-synced modules (`doctrine_enforcement.py`, `doctrine_setup_gate.py`).
- **v1 → v2 migration:** existing `setup.json` with `schema_version: 1` → `STALE_SCHEMA`; requires interactive setup/re-approval (legacy markdown preserved).
- **Power-loss:** journal records attempts; not a full transactional DB.
- **ll-cache:** not installed (per review scope).

## Follow-on work (post-7ab851d)

- **Frozen doctrine baseline:** `7ab851d` for ll-cache Phase 1 (disposable clone, doctrine setup, hook `conversation_id` check).
- **Optional pack:** `fault-first` (read-only failure analysis) — see [fault-first.md](fault-first.md); not part of `--lang` bundles.
- **Pilot target:** disposable **ll-cache** clone, not trading-system.
