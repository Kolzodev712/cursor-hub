# Specific workflow doc (standalone)

Produce an **in-depth, specific workflow document**: step-by-step guide for one concrete workflow — every step, inputs/outputs, commands, and examples. Use for runbooks, playbooks, or training.

## Steps

1. **Scope:** Identify the workflow to document in detail (e.g. "adding a new feature from design to merge", "fixing a bug with the bugfix workflow", "releasing a new version"). The user may reference a design log or a pack's workflow. If unclear, ask.
2. **Gather:** Trace the workflow from start to finish: commands, scripts, checks, and artifacts (e.g. design log, tests, PR). Use `.cursor/commands/` and design-log structure if relevant.
3. **Produce the doc:** Write a detailed workflow document with:
   - **Purpose** — One line: what this workflow accomplishes.
   - **When to use it** — Triggers or context (e.g. "when starting a new feature", "when fixing a non-trivial bug").
   - **Prerequisites** — What must be in place (branch, design log, tools installed, etc.).
   - **Steps** — Numbered steps. For each: what to do, which command or action, what the output or artifact is, and how to verify before moving on.
   - **Examples** — One concrete example (e.g. "Feature X: from design review to merged PR" or "Bug Y: from investigation to resolution").
   - **Troubleshooting** — Common failures and how to recover (e.g. validator fails, tests fail mid-flow).
4. **Output:** Present the doc in the response. If the user wants it saved, create or overwrite a file (e.g. `docs/workflows/<workflow-name>.md` or a path they specify). Otherwise leave it in chat.

Keep it specific: one workflow, full detail. For a high-level overview of all workflows use `/documentation__standalone-workflow-doc`.
