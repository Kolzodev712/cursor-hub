# Record workflow step in design log (manual)

Use when you want to **record a completed step** in the design log without re-running a workflow command (e.g. you did design or a bugfix in chat and want to log it).

Append (or create) a design log entry for one step type: **Design discussion**, **Implementation Results**, **Test session**, or (bugfix workflow) **Investigation**, **Proposed solution / Trade-offs**, **Resolution**.

## Steps

1. **Identify the step type** from the user's message (design review, implementation, test session, bugfix).
2. **Find or create the log:** If the user has an existing log for this workstream, use it. Otherwise run `python .cursor/tools/new_design_log.py --slug <short-name>` and create the file.
3. **Append the section** using the format from the **design-log-record** rule:
   - **Design discussion:** Recommended option, Risks, Verification.
   - **Implementation Results:** What was done, deviations, test outcome.
   - **Test session:** What was covered, how tests were run.
   - **Bugfix workflow:** Investigation (evidence, hypotheses), Proposed solution / Trade-offs, or Resolution (what was done, verification).
   - **Bugfix (single):** What was wrong, what fixed it, test that passes.
4. **Keep it short:** A few sentences to a short paragraph per section.

Location: `./.cursor/design-log/` only. Prefer the numbering script for new files.
