# Doctrine setup wizard — question-quality audit (v0.6.0)

Each prompt was reviewed against:

- Could two competent engineers interpret this differently?
- Does it combine two separate questions?
- Are units explicit where relevant?
- Is UNKNOWN available when the fact matters but is unknown?
- Is N/A available only where the concept can genuinely not apply?
- Does it explain what the answer will affect?
- Does it ask something inspection already knows (without offering Accept)?
- Does wording require cursor-hub internals?

| Step | Prompt (summary) | Audit notes |
|------|------------------|-------------|
| 1 Repository | Externally meaningful responsibility; not modules | Affects `architecture.md`. README offered Accept/Edit/Unknown only when detected. UNKNOWN allowed. |
| 2 Objectives list | Fixed engineering properties | Affects tradeoff ranking in `objectives.md`. U = objectives not yet chosen. |
| 2 Other follow-up | Name additional property; examples | Replaces bare "Other" label; ranks like any objective. |
| 2 Priority | Rank **selected** items when they conflict | Single question. U = priority order unknown. |
| 2 Scope | Priorities repo-wide vs per-component | Single question. U allowed. |
| 3 Invariants | Definition + examples + anti-examples | One invariant per line. U = none known yet. |
| 4 Performance gate | Whether speed/latency/throughput/memory matter for acceptance | Branches detail questions. N/A via skipped block when "no". U allowed. |
| 4 Workload fields | Label + unit examples + U/N/A | Each line one fact → `workload.md`. N/A when field does not apply. |
| 5 Components | Select detected roots; optional custom | Affects `components.json` gates only; no doctrine filenames. |
| 5 Interview | Plain-language Y/N/U/N/A per trait | Each trait one question; N/A when trait irrelevant (e.g. latency on static config). |
| 5 Static scan | Optional hint apply | Explicitly "may be wrong"; user confirms. |
| Summary | Shows derived decision topics | User confirms before final write. |

Component trait wording lives in `COMPONENT_INTERVIEW` in `cursor_hub/doctrine/setup.py` (source of truth).

## Manual acceptance (2026-10-05)

- **Full walkthrough:** `script(1)` pseudo-TTY + `python3 -m cursor_hub install --lang rust engineering-doctrine /tmp/doctrine-test` (ConsoleIO / `input()`, not `ScriptIO`). Transcript: `/tmp/doctrine-full3.transcript`.
- **Cancel/resume:** Ctrl+C during setup after repository + objectives → `doctrine status` shows those sections complete, later sections incomplete; resume via `cursor-hub doctrine setup .` (verified on `/tmp/doctrine-cancel`, interrupt exit 120).
- **Reinstall:** `install --overwrite --lang rust engineering-doctrine /tmp/doctrine-test` prints `COMPLETE_WITH_UNKNOWNS`, does not launch wizard; `objectives.md` unchanged.
- **Routing human review** (market-data-style profile: concurrent yes, atomics no, external I/O yes, latency yes, numeric no):

  Expected decision topics: **concurrency**, **io**, **memory**, **benchmarking**, **evidence** — not **atomics**, not **cpu-execution** (cpu-execution requires numeric compute, not perf alone). Verified in `test_market_data_style_routing`.

  When feeding answers through a PTY too quickly, component interview answers can misalign; typed real-time input avoids that. Re-run component section via `--review` if needed.
