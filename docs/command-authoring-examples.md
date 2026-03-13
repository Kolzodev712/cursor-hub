# Command-authoring reference

Short template and full examples so pack authors can copy and adapt when writing slash commands.

## Command template

- **Objective:** One sentence: what the user gets when they run this command.
- **Steps:** Numbered list: gather context → do the work → verify → output/record.
- **Constraints:** What the model must not do (e.g. no prod code changes, no new deps unless asked).
- **Output:** Where to put the result (file path, design log section, or "present in chat and save if user asks").

Commands that change code must end with an explicit verification step (e.g. run tests, run formatter). See [authoring-guidelines.md](authoring-guidelines.md).

---

## Example 1: Code review (standalone)

**Use case:** User runs a command to get a file-by-file PR review with must-fix vs nice-to-have.

**Objective:** Perform a structured PR review: list files, for each file give must-fix and nice-to-have items, then a short summary.

**Steps:**

1. Identify the scope (branch diff, or files user points to).
2. For each relevant file: briefly summarize changes, then list **must-fix** (correctness, safety, API contract) and **nice-to-have** (style, clarity, tests).
3. End with a short overall summary and risk level.

**Constraints:** Do not edit code unless the user explicitly asks to apply fixes. Review only.

**Output:** Present the review in the response. If the user wants it saved, write to a file they specify (e.g. `review.md`); otherwise leave in chat.

---

## Example 2: Run tests and fix (standalone)

**Use case:** User wants the model to run the test suite and fix any failures.

**Objective:** Run the project’s tests and fix any failures until all pass.

**Steps:**

1. Run the project’s test command (e.g. `cargo test --all-features` or `pytest`). If there is a project script (e.g. `just test`), use that.
2. For each failure: identify cause, make minimal code or test changes to fix it, then re-run tests.
3. Repeat until all tests pass. Do not add new features or refactors; only fix failing tests.

**Constraints:** Minimal edits. No new dependencies unless required to fix the failure. Do not change behavior beyond what is needed to make tests pass.

**Output:** Summary of what failed, what was changed, and final test result. Code changes are written to the repo.

**Verification:** The last step is “run tests again”; the command is complete only when the test command exits successfully.

---

## Example 3: Create PR description (standalone)

**Use case:** User has a branch and wants a PR title and description body.

**Objective:** Produce a PR title and description (what changed, why, how to verify) from the current branch’s commits and diff.

**Steps:**

1. Determine the diff (e.g. `main`..`HEAD` or `origin/main`..`HEAD`). List commits and changed files.
2. Summarize the change in one sentence for the title; then write a short description: what changed, why, and how to verify (e.g. run X, check Y).
3. Optionally list breaking changes or follow-ups.

**Constraints:** Base the description only on the actual diff and commits. Do not invent scope.

**Output:** Present the title and body in the response. If the user wants it saved, write to a file (e.g. `pr_description.md`) or the clipboard; otherwise leave in chat for copy-paste.

---

## Naming and placement

- Command filename: `{pack-name}__{task}.md` (e.g. `rust-review__standalone-pr-review.md`).
- Slash command users see: `/rust-review__standalone-pr-review`.
- Put the file in the pack’s `.cursor/commands/` directory.

See [authoring-guidelines.md](authoring-guidelines.md) and [CATALOG.md](../CATALOG.md) for the full list of packs and commands.
