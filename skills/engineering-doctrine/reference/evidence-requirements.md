# Evidence requirements

## Trigger

Any merge request that claims faster, smaller, more scalable, or "cache-friendly" behavior.

## Required minimum

- **Workload cite:** Point to project `workload.md` or state new assumptions explicitly.
- **Hypothesis:** What limiter was targeted (CPU, memory, IO, lock, alloc)?
- **Method:** Test, benchmark, or profile — command and environment noted.
- **Result:** Metric delta with acceptable noise band.
- **Regression guard:** Test or benchmark added when claim is durable.

## Reject when

- Only complexity class cited without size constants.
- Synthetic microbench unrelated to production path.
- Optimization violates documented invariants.

## Accept when

Evidence matches accept/reject criteria in the design or PR description and hooks/project doctrine reads are satisfied for classified paths.
