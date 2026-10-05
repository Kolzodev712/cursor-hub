# Cursor skills (hub-maintained)

These are **Cursor Agent Skills** (`SKILL.md` + optional reference files). They are **not** installed by `cursor-hub install` today (that flow only merges packs: rules, commands, agents, tools).

To use a skill in a project:

```bash
mkdir -p /path/to/project/.cursor/skills
cp -r /path/to/cursor-hub/skills/rust-best-practices /path/to/project/.cursor/skills/
```

Or symlink for development. Cursor discovers skills under **`.cursor/skills/<name>/`** in the project.

**Pack install:** Packs can declare skill dependencies in `pack.yml` (`skills:` list). Installing e.g. `rust-implementation` or `engineering-doctrine` copies the listed trees into `.cursor/skills/` (existing files are kept unless you pass `--overwrite`). Nested deps may be listed in `skills/<name>/skill-deps.json`.

| Skill | Purpose |
|-------|---------|
| [rust-best-practices](rust-best-practices/SKILL.md) | Rust idioms, API guidelines checklist, security/tooling baseline; see references inside. |
