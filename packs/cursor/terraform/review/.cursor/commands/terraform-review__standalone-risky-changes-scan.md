# Risky changes scan (Standalone)

Flag risky patterns: state changes, sensitive values, destroy/replace, new resources or providers.

## Steps

1. **Scan** the changed files (or the whole Terraform config if the user does not specify) for:
   - **State-affecting changes:** Any change that could cause destroy or replace. Note resource address and reason (e.g. force_new attribute change).
   - **Sensitive values:** Any secret or sensitive data in .tf or .tfvars. Note whether variables/outputs are marked sensitive.
   - **New resources or providers:** New provider requirements or resource types. Note version and why needed.
   - **Lifecycle and state:** lifecycle blocks, state removal, or migration hints. Note if destructive.
2. **Report:** For each category, list occurrences with file/resource or a short reference. Summarize overall risk (low / medium / high) and recommend follow-up (e.g. "run plan and review destroy set", "move secret to variable").

Do not fix the config in this command unless the user asks; focus on identification and prioritization.
