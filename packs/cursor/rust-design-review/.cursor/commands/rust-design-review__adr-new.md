# ADR New (Create design log)

Create a new design-log entry with the standard template. Do not guess the next NNN.

## Steps

1. **Create the file:** Run `python tools/new_design_log.py --slug <short-name>` from the project root. Use a short, kebab-case slug (e.g. `risk-cache`, `auth-refactor`). The script prints the created file path.
2. **Open the file** at the path printed by the script.
3. **Fill the template** with the user's design content, following the structure: Background → Problem → Questions and Answers → Design → Implementation Plan → Examples → Trade-offs → Verification. Leave "Implementation Results" for later.
4. **Be specific:** Include file paths, types, and verification criteria as appropriate.

If the user provided a title or outline, use it to populate the sections. If not, add placeholder headings and 1–2 sentence stubs so the user can edit.
