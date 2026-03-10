# Design review (rust-design-review WF Step 1)

Strict, critical design review. Question assumptions and produce a recommended option with risks and verification. You can use this command on its own — no requirement to run implementation or testing afterward.

**After this command:** The design log is updated automatically (see Step 8). To create a new log manually, use `/design-log__create`.

## Steps

1. **Check existing logs:** List or read `./.cursor/design-log/` for any related or overlapping design logs. If one exists for this topic, reference it and extend or refine rather than starting from zero; if none, proceed to create new content.
2. **Understand the ask:** Identify the problem, scope, and any stated constraints.
3. **Challenge:** List 2–4 critical questions or risks (missing constraints? alternatives? failure modes?).
4. **Alternatives:** Propose 1–2 alternative approaches with pros/cons.
5. **Recommendation:** State the recommended option and why; call out remaining risks.
6. **Verification:** Define how we will verify the design (tests, invariants, metrics).
7. **Output:** Summarize in a short block: Recommended option, Risks, Verification steps.
8. **Record in design log (mandatory):** Create or update the design log as part of this response. If a log for this workstream already exists (user cited it or you used it earlier), append a **Design discussion** section with: Recommended option, Risks, Verification steps. If no log exists, run `python .cursor/tools/new_design_log.py --slug <short-name>` (or fallback: list `./.cursor/design-log/`, take max NNN + 1, create `./.cursor/design-log/NNN-<slug>.md`) and fill it with at least Background/Problem/Design discussion (option, risks, verification). Use the project root; create logs only in `./.cursor/design-log/`. Do not ask — do it.
9. **Verify:** Run `python .cursor/tools/validate_workflow_design_log.py --step design-review` from the project root. If it fails, add the missing Design discussion content to the log and re-run the validator. Do not consider the command complete until the validator passes.
