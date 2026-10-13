# System orchestration sources and claim boundaries

Public primary documentation checked on 2026-10-12. This is a construction kit, not a certification or a claim that any cited framework is a dependency. Only the optional `jsonschema` Python package is introduced by this feature.

| Source | Mechanism supported | Does not establish |
|---|---|---|
| [Kubernetes controllers](https://kubernetes.io/docs/concepts/architecture/controller/) | Repeated comparison of observed and desired state; controller responsibilities | Convergence or correctness of arbitrary model-generated actions |
| [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Application-defined workflows versus model-directed behavior; composable tool-using systems | Reliability of this implementation or authorization to run agents |
| [Python sqlite3 documentation](https://docs.python.org/3/library/sqlite3.html) | SQLite transactions and connection behavior | Exactly-once external effects, tamper-proof logs, or a distributed scheduler |
| [jsonschema validation documentation](https://python-jsonschema.readthedocs.io/en/stable/validate/) | Draft-specific validators, schema checks and validation errors | Truth, safety, authenticity or completeness of a schema-valid model response |

## Epistemic classes

MECHANISM means scoped behavior supported by the primary references above. POLICY means a chosen project design constraint, not a universal scientific result. IMPLEMENTED means behavior expressed by the current code and checked only to the extent documented by tests. UNVERIFIED means a live adapter, security boundary or real-world claim not exercised here.

The separation of supervisor authority, action receipts and verification is a POLICY informed by these mechanisms. The synthetic fixture identities and check results are assertions supplied by the test author, not authenticated evidence. No performance, production-safety, or model-accuracy claims are made.
