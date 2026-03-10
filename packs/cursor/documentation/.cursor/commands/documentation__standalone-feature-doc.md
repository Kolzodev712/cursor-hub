# Feature doc (standalone)

Produce an **in-depth, feature-specific document**: detailed behavior, APIs, examples, and edge cases for one feature or area. Use for developer docs, runbooks, or handoffs.

## Steps

1. **Scope:** Identify the feature or area to document (e.g. "config loading", "auth flow", "payment retries"). The user may point to a design log, module, or ticket. If unclear, ask.
2. **Gather:** Read the relevant code, types, and entry points. Use design logs in `.cursor/design-log/` if they cover this feature.
3. **Produce the doc:** Write a focused document with:
   - **Purpose** — One line: what this feature/area is and why it exists.
   - **Behavior** — What the feature does: inputs, outputs, main flows, and failure behavior.
   - **API / surface** — Public types, functions, or endpoints; signatures and contracts where useful.
   - **Examples** — Good usage examples and, if relevant, anti-patterns or pitfalls.
   - **Edge cases** — Known limitations, error handling, and configuration that affects behavior.
   - **Verification** — How to test or validate the feature (tests, manual steps).
4. **Output:** Present the doc in the response. If the user wants it saved, create or overwrite a file (e.g. `docs/features/<name>.md` or a path they specify). Otherwise leave it in chat.

Keep it feature-specific: no broad architecture. For high-level architecture use `/documentation__standalone-architecture-doc`.
