# Design Review

Strict, critical design review. Question assumptions and produce a recommended option with risks and verification.

## Steps

1. **Understand the ask:** Identify the problem, scope, and any stated constraints.
2. **Challenge:** List 2–4 critical questions or risks (missing constraints? alternatives? failure modes?).
3. **Alternatives:** Propose 1–2 alternative approaches with pros/cons.
4. **Recommendation:** State the recommended option and why; call out remaining risks.
5. **Verification:** Define how we will verify the design (tests, invariants, metrics).
6. **Output:** Summarize in a short block: Recommended option, Risks, Verification steps.

Do not create or edit design log files in this command unless the user explicitly asks to record the result. If they do, use `python tools/new_design_log.py --slug <short-name>` to create the log, then fill it following the design-log structure.
