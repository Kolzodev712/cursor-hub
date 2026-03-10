# Architecture doc (standalone)

Produce a **general-level architecture document**: high-level view of the system — main components, boundaries, data flow, and tech stack. Use when onboarding, for ADRs, or to align on structure.

## Steps

1. **Scope:** Confirm the system or repo to document (e.g. this project, a service, or a bounded context). If unclear, ask.
2. **Explore:** Review the codebase layout, entry points, major modules, and dependencies. Check `.cursor/design-log/` for existing architecture notes.
3. **Produce the doc:** Write a concise architecture document with:
   - **Purpose** — One line: what this document describes.
   - **Overview** — 2–4 sentences on what the system does and its main boundaries.
   - **Components** — Main modules, services, or layers; responsibility of each; how they interact.
   - **Data flow** — How data or requests move through the system (high level).
   - **Tech stack** — Languages, frameworks, key libraries, and where they are used.
   - **Diagrams** — Optional: Mermaid or ASCII diagram of components and flow if helpful.
4. **Output:** Present the doc in the response. If the user wants it saved, create or overwrite a file (e.g. `docs/architecture.md` or a path they specify). Otherwise leave it in chat for them to copy.

Keep it general: no deep dive into a single feature. For feature-level detail use `/documentation__standalone-feature-doc`.
