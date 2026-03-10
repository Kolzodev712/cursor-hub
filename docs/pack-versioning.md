# Pack versioning

**pack.yml:** Optional `version` (e.g. `0.2.0`). Patch = typos/clarifications; minor = new rules/commands/agents; major = remove/rename or breaking change.

**Command naming:** Command files must be named `{pack-name}__{command-name}.md` (e.g. `rust-design-review__wf-1-design-review.md`). The slash command is the filename stem (e.g. `/rust-design-review__wf-1-design-review`). This avoids collisions when multiple packs are installed. The validator fails if a non–`_shared` pack has a command file that does not follow this convention.

**Installer:** Merges by copy; prints installed pack versions from `pack.yml` when present. Same filename = last pack wins unless `--overwrite`. Installer copies scripts into the target's `.cursor/tools/`.

**Validator:** Checks structure, frontmatter, command naming convention, and per-pack duplicate command names. Run in CI on every push/PR (see `.github/workflows/validate.yml`). The **design-log** pack also provides `validate_workflow_design_log.py`, used by workflow commands to verify the design log was updated (see README).
