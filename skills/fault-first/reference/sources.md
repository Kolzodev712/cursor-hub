# Method references and limits

The following are **method starting points**, not evidence that any particular software system fails or passes. Follow current official versions and project-specific standards where applicable.

- **IEC 60812:2018** — *Failure modes and effects analysis (FMEA and FMECA)*, IEC catalog: https://webstore.iec.ch/ . Formal standard; access may require purchase. This skill uses failure-mode reasoning but does not claim standard-compliant FMEA.
- **IEC 61025:2006** — *Fault tree analysis (FTA)*, IEC catalog: https://webstore.iec.ch/ . A causal list is not automatically a formal fault tree; boolean gate semantics and dependencies matter.
- **Nancy G. Leveson, Engineering a Safer World** — STAMP/STPA systems-safety foundations: https://mitpress.mit.edu/9780262533690/engineering-a-safer-world/ . Use when unsafe control actions and system interactions are central, not as a universal software checklist.
- **NIST SP 800-160 Vol. 1 Rev. 1** — *Engineering Trustworthy Secure Systems*: https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final (DOI https://doi.org/10.6028/NIST.SP.800-160v1r1). Security-oriented systems engineering reference; not proof of functional correctness.
- **Hypothesis** — property-based testing documentation: https://hypothesis.readthedocs.io/ ; **proptest** Rust crate docs: https://docs.rs/proptest/ . Tools for generating test cases; success does not establish exhaustive correctness.
- **Principles of Chaos Engineering** — https://principlesofchaos.org/ . Controlled fault injection is a separate, opt-in verification activity; never use production fault injection as a default analysis step.

**Epistemic boundary:** methodology sources justify an investigative method, not the likelihood, severity, or existence of a specific defect. Application findings require the system's contracts and direct evidence.
