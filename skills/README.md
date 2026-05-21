# Cursor skills (hub-maintained)

These are **Cursor Agent Skills** (`SKILL.md` + optional reference files). They are **not** installed by `cursor-hub install` today (that flow only merges packs: rules, commands, agents, tools).

To use a skill in a project:

```bash
mkdir -p /path/to/project/.cursor/skills
cp -r /path/to/cursor-hub/skills/rust-best-practices /path/to/project/.cursor/skills/
```

Or symlink for development. Cursor discovers skills under **`.cursor/skills/<name>/`** in the project.

| Skill | Purpose |
|-------|---------|
| [rust-best-practices](rust-best-practices/SKILL.md) | Rust idioms, API guidelines checklist, security/tooling baseline; see references inside. |
