# Bug summary (standalone)

Produce a **bug summary document**: what was wrong, root cause, fix, and verification. Use for tickets, handoffs, postmortems, or release notes.

## Steps

1. **Scope:** Identify the bug to summarize. The user may describe it, point to a fix (diff/PR), or reference a design log (e.g. from the bugfix workflow). If unclear, ask.
2. **Gather:** From the conversation, design log, or code: reproduction, root cause, change that fixed it, and how it was verified.
3. **Produce the doc:** Write a short bug summary with:
   - **Title** — One line: brief description of the bug or fix (e.g. "Config panics when PREFIX_PORT is not a number").
   - **Summary** — 1–3 sentences: what was wrong and what we did about it.
   - **Root cause** — Why it happened (code path, missing check, wrong assumption).
   - **Fix** — What changed (files, behavior). Link to commit or PR if available.
   - **Verification** — How we confirmed the fix (tests added or run, manual check).
   - **Impact** — Optional: who or what was affected, severity, or follow-ups.
4. **Output:** Present the doc in the response. If the user wants it saved, create or overwrite a file (e.g. `docs/bugs/<slug>.md`, a ticket body, or a path they specify). Otherwise leave it in chat for them to paste into an issue or report.

For investigating or fixing the bug, use the **bugfix pack for your language** (e.g. rust-bugfix, python-bugfix, js-ts-bugfix, terraform-bugfix — standalone fix or full workflow). This command only documents an already-understood bug.
