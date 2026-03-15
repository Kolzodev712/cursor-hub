# Fix small bug (standalone)

Point the agent in the right direction for **identifying and fixing a small bug**. No multi-step workflow; use when the bug is localized, root cause is findable quickly, and a minimal fix is appropriate.

## Steps

1. **Identify:** Reproduce the bug from the user's description, issue, or stack trace. Locate the relevant code and behavior.
2. **Root cause:** Narrow down the cause (e.g. wrong type, missing check, off-by-one). Keep scope minimal.
3. **Fix:** Make the minimal code change that fixes the bug. Do not refactor unrelated code.
4. **Verify:** Run tests (`npm test`) and any format/lint the project uses. Fix any failures.
5. **Summarize:** Briefly state what was wrong and what change fixed it.

**Design log:** For small bugs you may skip a design log. If the fix has non-obvious trade-offs or the user wants it recorded, create or append a log in `./.cursor/design-log/` (e.g. run `python .cursor/tools/new_design_log.py --slug bugfix-<name>` and add a short Bugfix section). Do not require the user to run the full bugfix workflow for trivial fixes.

If the bug suggests a larger design flaw, say so and suggest the **bugfix workflow** (wf-1-investigation → wf-2-proposed-solution → wf-3-resolution) or the main design-review workflow instead.
