# Create design log (manual)

Use when you want to **create a new design log** without running a full workflow step (e.g. start a log before design, or create a log for a decision made outside the workflow).

Create a new design-log entry with the standard template. Design log location and structure are defined in the **design-log** rule (`_shared`); this command follows that specification.

**Design log directory (CRITICAL):** `./.cursor/design-log/` — create logs only there.

## Steps

1. **Create the file:** From the project root, run:
   `python .cursor/tools/new_design_log.py --slug <short-name>`
   Use a short, kebab-case slug (e.g. `risk-cache`, `auth-refactor`). If the script is not available, list `./.cursor/design-log/`, find max NNN from `NNN-*.md`, use next number (or 001), create `./.cursor/design-log/NNN-<slug>.md`.

2. **Open the file** at the path (from script output or the file you created).

3. **Fill the template** with the user's content: Background → Problem → Questions and Answers → Design → Implementation Plan → Examples → Trade-offs → Verification. Leave "Implementation Results" for later.

4. **Be specific:** Include file paths, types, and verification criteria as appropriate.

**Standard template:** Background, Problem, Questions and Answers, Design, Implementation Plan, Examples, Trade-offs, Verification, Implementation Results (append later).

If the user provided a title or outline, use it to populate the sections. If not, add placeholder headings and 1–2 sentence stubs so the user can edit.

**Note:** When you run workflow commands (wf-1-design-review, wf-1-implement-module, wf-1-add-tests-only, or the bugfix workflow wf-1-investigation, wf-2-proposed-solution, wf-3-resolution), the design log is created or updated **automatically** at the end of that command. Use this command only when you want to create a log manually (e.g. from the slash menu without running a workflow step).
