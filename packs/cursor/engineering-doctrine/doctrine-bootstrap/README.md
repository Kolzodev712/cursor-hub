# Project doctrine (local system truth)

Files here are **owned by the project**. The cursor-hub installer creates missing templates only; it **never overwrites** existing doctrine on reinstall or `--overwrite`.

Fill these in for your system:

| File | Purpose |
|------|---------|
| `objectives.md` | What the system must achieve; success metrics |
| `invariants.md` | Non-negotiable constraints (correctness, safety, SLOs) |
| `architecture.md` | Major components, boundaries, data flow |
| `workload.md` | Traffic shape, hot paths, data sizes, latency budgets |
| `findings.md` | Open performance/reliability findings and evidence |
| `components.json` | Path patterns → required reads before edits (see schema) |

Generic hub doctrine lives in `.cursor/skills/engineering-doctrine/`. Project facts override generic optimization preferences.
