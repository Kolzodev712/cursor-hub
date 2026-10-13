# Machine-readable contracts

`cursor_hub/orchestration/contracts.py` is the single executable schema definition. Export standard Draft 2020-12 JSON Schema with:

```bash
cursor-hub orchestration schema mission
cursor-hub orchestration schema observation
cursor-hub orchestration schema proposal
cursor-hub orchestration schema approval
cursor-hub orchestration schema receipt
cursor-hub orchestration schema evidence
cursor-hub orchestration schema event
cursor-hub orchestration schema scenario
```

Output goes to standard output; redirect it to a project-owned path only when deliberately creating a schema artifact. All references are bundled/local. User input cannot provide a custom schema or external reference. No remote schema resolution is needed.

Validate a single contract with `cursor-hub orchestration validate --kind mission <mission.json>`. The default kind is `scenario`. Unknown fields, malformed JSON, duplicate keys, non-finite numbers, oversized input and unsupported live mode fail. Runtime validation additionally checks cross-field policy and event-order constraints; a generic schema validator alone is insufficient.

The contracts describe the simulation-only v1 reference implementation. A live WorkItem/ActionRequest/worker/executor protocol is a project design output, not an already implemented universal API. State remains a versioned internal representation verified by replay, not a supported external write interface.
