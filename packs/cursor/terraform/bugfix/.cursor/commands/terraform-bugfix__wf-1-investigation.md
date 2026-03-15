# Bug investigation and evidence collection (Bugfix WF Step 1)

**Part of the bugfix workflow** — separate from the main design-review/implement/test flow. Use when the bug is non-trivial and needs structured investigation before a fix.

**Follow with:** Bugfix Step 2 — Proposed solution (`/terraform-bugfix__wf-2-proposed-solution`), then Step 3 — Resolution (`/terraform-bugfix__wf-3-resolution`).

## Steps

1. **Reproduce:** Confirm the bug from issue, user description, or stack trace. Document steps to reproduce and environment (e.g. branch, env vars, inputs).
2. **Evidence:** Collect evidence: stack traces, logs, failing test output, relevant code paths. Identify the component(s) and call sites involved.
3. **Scope:** Describe what is broken (expected vs actual), and what is *not* in scope for this fix.
4. **Hypotheses:** List 1–3 plausible root causes or contributing factors. Note what would confirm or rule each out.
5. **Output:** Summarize: reproduction steps, evidence, scope, hypotheses. Do not propose the fix yet; that is Step 2.
6. **Record in design log (mandatory):** Create or update the design log for this bugfix workstream. If no log exists, run `python .cursor/tools/new_design_log.py --slug bugfix-<short-name>` (or fallback: create the file in `./.cursor/design-log/`). Append (or fill) an **Investigation** section: reproduction steps, evidence, scope, hypotheses. Create logs only in `./.cursor/design-log/`. Do not ask — do it.
7. **Verify:** Run `python .cursor/tools/validate_workflow_design_log.py --step investigation` from the project root. If it fails, add the missing Investigation content and re-run the validator. Do not consider the command complete until the validator passes.

This workflow uses its own design logs; it does not assume a log from terraform-design-review or terraform-implementation.
