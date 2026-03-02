# Risky Changes Scan

Flag risky patterns: unsafe, unwrap, panics, new deps, public API breaks.

## Steps

1. **Scan** the changed files (or the whole codebase if the user does not specify) for:
   - **unsafe:** Any `unsafe` block. Note location and whether an invariant is documented.
   - **unwrap / expect:** In non-test code. Note if it's in a hot path or could panic on user input.
   - **panic! / unreachable!:** Note where and under what condition.
   - **New dependencies:** Any new entries in `Cargo.toml`. Note license, maturity, and why they are needed.
   - **Public API changes:** New public items, changed signatures, or removed items. Note breaking vs additive.
2. **Report:** For each category, list occurrences with file/line or a short reference. Summarize overall risk (low / medium / high) and recommend follow-up (e.g. "add invariant comment", "replace unwrap with ?", "document breaking change in changelog").

Do not fix the code in this command unless the user asks; focus on identification and prioritization.
