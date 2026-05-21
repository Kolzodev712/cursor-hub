# Pack versioning

**pack.yml:** Optional `version` (e.g. `0.2.0`). Patch = typos/clarifications; minor = new rules/commands/agents; major = remove/rename or breaking change.

**Command naming:** Command files must be named `{pack-name}__{command-name}.md` (e.g. `rust-design-review__wf-1-design-review.md`, `python-design-review__wf-1-design-review.md`). The slash command is the filename stem. Same convention for all language packs (rust-*, python-*, js-ts-*, terraform-*). This avoids collisions when multiple packs are installed. The validator fails if a non–`_shared` pack has a command file that does not follow this convention.

**Installer:** Run with `cursor-hub install` (after `pip install -e .`) or `python tools/install.py` from the hub repo. Merges only **rules, commands, agents** from packs plus hub scripts into `.cursor/tools/`. **Never** syncs **`NNN-*.md`** project logs from the hub (`--overwrite` replaces rules/commands/agents collisions only); optional **`--refresh-design-log-readme`** overwrites **`README.md` only.** Packs must not ship `.cursor/design-log/` (`validate_packs`). Prints installed pack versions from `pack.yml` when present. Same hub filename merged from multiple packs: last wins unless `--overwrite`.

**Validator:** Checks structure, frontmatter, command naming convention, per-pack duplicate command names, and that packs do not ship `.cursor/design-log/`. Run in CI on every push/PR (see `.github/workflows/validate.yml`). The **design-log** pack also provides `validate_workflow_design_log.py`, used by workflow commands to verify the design log was updated (see README).
