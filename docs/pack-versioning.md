# Pack versioning

**pack.yml:** Optional `version` (e.g. `0.1.0`). Patch = typos/clarifications; minor = new rules/commands/agents; major = remove/rename or breaking change.

**Command naming:** Command files must be named `{pack-name}__{command-name}.md` (e.g. `rust-design-review__design-review.md`). The slash command is the filename stem (e.g. `/rust-design-review__design-review`). This avoids collisions when multiple packs are installed. The validator fails if a non–`_shared` pack has a command file that does not follow this convention.

**Installer:** Merges by copy; prints installed pack versions from `pack.yml` when present. Same filename = last pack wins unless `--overwrite`. Use `--with-tools` to copy the `tools/` directory into the target project.

**Validator:** Checks structure, frontmatter, command naming convention, and per-pack duplicate command names. Run in CI on every push/PR (see `.github/workflows/validate.yml`).
