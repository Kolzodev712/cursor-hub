# Risky changes scan (Standalone)

Flag risky patterns: eval/exec, broad except, new deps, public API breaks.

## Steps

1. **Scan** the changed files (or the whole codebase if the user does not specify) for:
   - **eval / exec:** Any dynamic code execution. Note location and whether inputs are controlled.
   - **Bare except / broad except:** Catching `Exception` or base without re-raise or careful handling. Note if it could hide bugs.
   - **New dependencies:** Any new entries in pyproject.toml, requirements*.txt, or setup.py. Note license, maturity, and why they are needed.
   - **Public API changes:** New public names, changed signatures, or removed exports. Note breaking vs additive.
2. **Report:** For each category, list occurrences with file/line or a short reference. Summarize overall risk (low / medium / high) and recommend follow-up (e.g. "narrow the except", "document breaking change in changelog").

Do not fix the code in this command unless the user asks; focus on identification and prioritization.
