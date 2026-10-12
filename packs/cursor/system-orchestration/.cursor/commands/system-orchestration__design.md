# Design a bounded AI operating system

Read `.cursor/skills/system-orchestration/SKILL.md`; follow its design workflow for the user-named system. This is a design workflow, not permission to deploy or implement it.

First inspect the supplied project facts read-only. Produce a charter, an explicit transition/authority table, adapter contracts, and an evaluation plan. Mark unresolved facts instead of selecting invented objectives, budgets, owners, credentials, or acceptance criteria. Propose ordinary software where model judgment is unnecessary.

Present the design and operating-contract draft in chat. Wait for approval before writing new artifacts; never write implementation code under this command. Use the existing deterministic design-log tool only when recording has been explicitly authorized. Do not automatically promote findings to doctrine.

For an approved simulation fixture, validate it with `cursor-hub orchestration validate --kind scenario <fixture.json>` and run `cursor-hub orchestration simulate <fixture.json>`. These commands require the hub tooling with its orchestration extra. Report command exit codes, expected versus observed states, and what remains unverified. Do not interpret a successful fixture as a verified real system.
