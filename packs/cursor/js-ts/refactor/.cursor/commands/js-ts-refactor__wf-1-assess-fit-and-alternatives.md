# Refactor — assess fit and alternatives (js-ts-refactor WF Step 1)

**Goal:** Decide whether this **subsystem, module abstraction, tooling choice, or dependency** **still earns its place** via **engineering** and **idiomatic JS/TS** review, naming **better alternatives** when warranted. **Analysis only** unless a bounded spike is requested.

**Follow with:** `/js-ts-refactor__wf-2-execute-refactor` after agreement to proceed.

## Steps

1. **Check existing logs:** `./.cursor/design-log/`; extend an existing refactor workstream when applicable.
2. **Scope:** App area, npm workspace package, CLI module, SDK surface, persistent framework/plugin stack, or stubborn dependency triangle.
3. **Systems assessment:** Targets (browser/server/Edge), bundles and tree‑shaking, perf/latency if relevant, security (XSS/supply‑chain/version pinning), rollout and versioning story.
4. **JS/TS quality:** Modules and public API ergonomics; strict TS vs escape hatches; async patterns; ESLint/tsconfig boundaries; SSR/client-only splits; duplication and dead exports.
5. **Usefulness verdict:** **Minor tweaks**, **internal reshape**, **replace lib/pattern**, **split/remove package**, **needs spike**.
6. **Alternatives:** 1–3 concrete paths (switch bundler/tsconfig preset, peel UI kit, consolidate state layer, narrower public API)—with pros/cons and effort/risk.
7. **Recommendation + acceptance criteria** for wf-3; abort signals if wrong.
8. **Record:** **Refactor assessment** + stamp `[cursor-hub workflow] step=refactor-assessment`; create log with `python .cursor/tools/new_design_log.py --slug …` if needed.
9. **Verify:** `python .cursor/tools/validate_workflow_design_log.py --step refactor-assessment` until passes.
