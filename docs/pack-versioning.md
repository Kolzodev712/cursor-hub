# Pack versioning

**pack.yml:** Optional `version` (e.g. `0.1.0`). Patch = typos/clarifications; minor = new rules/commands/agents; major = remove/rename or breaking change.

**Installer:** Merges by copy; no version checks. Same filename = last pack wins unless `--overwrite`.

**Validator:** Checks structure only, not version.
