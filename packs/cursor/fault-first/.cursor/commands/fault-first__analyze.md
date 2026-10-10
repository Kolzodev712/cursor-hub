# Fault-first analysis — explicit, read-only workflow

Analyze **the component, boundary, design, or failure outcome named by the user**. This command is deliberately opt-in. It is not an ambient rule and does not replace design review, implementation, testing, or project doctrine.

1. Load the `fault-first` skill (`.cursor/skills/fault-first/SKILL.md`) and follow its full protocol. If engineering-doctrine is installed, use its applicable project objectives, invariants, workload, and decision-domain guidance. Do not require engineering-doctrine to be installed.
2. Clarify only the essential missing scope or intended behavior; otherwise proceed with clearly labeled assumptions. Read source, tests, documentation, and design logs as needed. Treat unknown requirements as unknown, not defects.
3. Produce a bounded failure analysis using the skill's output contract (`reference/report.md`): system boundary, guarantees, undesirable outcomes, causal hypotheses, evidence, ranked risks, test proposals, unknowns, and stop decision. Normally **3–7 material findings** for the scoped target; fewer for tiny components.
4. Label every finding with exactly one status: `CONFIRMED_DEFECT` (only with demonstrated contract violation), `CREDIBLE_HYPOTHESIS`, `REQUIREMENT_GAP`, or `EXCLUDED`. Seek counterevidence before escalating severity.
5. Remain **read-only**. Do not modify source, tests, doctrine, design logs, or configuration. Do not run test commands (`cargo test`, `pytest`, etc.), inject faults, start live external actions, or create files unless the user separately authorizes them. Reading source and existing tests is permitted; executing tests is not part of this command.
6. Do not invent numerical failure probabilities, severity scores, test results, or sources.
7. End with at most **three** highest-priority next investigations and explicit questions that need human decisions. Stop after the bounded analysis; do not enter an autonomous implementation loop.

If the user asks to implement or verify one proposed test later, treat that as a separate task requiring explicit authorization and its own acceptance criteria.
