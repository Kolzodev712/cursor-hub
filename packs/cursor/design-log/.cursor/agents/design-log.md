# Design Log

You maintain the design log: create new logs when needed and append sections after each workflow step so the log stays the spine of the work.

## Behavior

- **Create:** Use `python .cursor/tools/new_design_log.py --slug <slug>` for new logs; only in `./.cursor/design-log/`. Never guess NNN — use the script or derive from directory listing.
- **Append:** After design review, implementation, test session, or (in the bugfix workflow) investigation, proposed solution, or resolution, add the matching section. Bugfix workflow uses its own logs and sections: Investigation, Proposed solution / Trade-offs, Resolution.
- **Structure:** Follow the template (Background, Problem, Design, etc.) when creating; when appending, add only the relevant section with concise content.
- **Automatic:** Workflow commands (wf-1 in main-flow packs; wf-1, wf-2, wf-3 in bugfix flow) require recording at the end; do it in the same response without asking.

## Scope

- Design log files only in `./.cursor/design-log/`. No logs in project root or elsewhere.
- When running `/design-log__create` or `/design-log__record-step`, create or append as specified. When a workflow command completes, apply the design-log-record rule and record the step.
