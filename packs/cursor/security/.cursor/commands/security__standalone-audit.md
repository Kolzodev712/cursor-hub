# Security audit (standalone)

Run a one-pass security review of the codebase and configuration.

## Objective

Produce a short security report: critical/high/medium/low findings with location, issue, and recommendation. Use the **security** agent’s scope and severity levels.

## Steps

1. **Scope:** Identify the area to review (whole repo, or paths the user specifies). If unclear, default to application code, config, and CI.
2. **Review:** Walk through code vulnerabilities, dependencies (run `cargo audit` or equivalent if available), secrets and auth, crypto usage, misconfiguration, and CI/CD. Classify each finding by severity.
3. **Report:** Output a structured summary:
   - Critical / High: issue, location, recommendation.
   - Medium / Low: brief list or "see below" with details.
4. **Recommendations:** For critical/high, give concrete next steps (e.g. upgrade dep X, remove secret from Y, add auth to Z).

## Constraints

- Do not make invasive changes unless the user explicitly asks to apply fixes. This command is review-only by default.
- If the project has a lockfile or manifest, run the ecosystem’s audit tool (e.g. `cargo audit`, `npm audit`) and include results in the report.

## Output

Present the report in the response. If the user wants it saved, write to a file they specify (e.g. `security-audit.md`); otherwise leave in chat.
