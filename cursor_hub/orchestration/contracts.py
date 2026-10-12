"""Versioned, closed JSON contracts. Schemas and validation share one definition.

Only bundled schemas are evaluated. User input cannot supply a schema or a
remote reference. jsonschema is an optional dependency of this subcommand.
"""
from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Any

MAX_INPUT_BYTES = 2_000_000
MAX_EVENTS = 1000
STATES = (
    "ADMITTED", "INVESTIGATING", "PROPOSED", "AWAITING_APPROVAL", "AUTHORIZED",
    "EXECUTED", "OUTCOME_UNKNOWN", "VERIFIED", "NO_ACTION", "BLOCKED",
    "REJECTED", "FAILED", "CANCELLED",
)
TERMINAL = frozenset({"VERIFIED", "NO_ACTION", "BLOCKED", "REJECTED", "FAILED", "CANCELLED"})


class ContractError(ValueError):
    """Invalid input, conflicting identity, or incompatible journal."""


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def fingerprint(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ContractError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _bad_constant(value: str) -> Any:
    raise ContractError(f"Non-finite JSON number: {value}")


def decode_json(text: str) -> Any:
    try:
        value = json.loads(text, object_pairs_hook=_unique_object, parse_constant=_bad_constant)
        canonical(value)  # Reject numeric overflow to infinity as well as NaN literals.
        return value
    except (ValueError, RecursionError) as exc:
        raise ContractError(f"Invalid JSON: {exc}") from exc


def load_json(path: str | Path) -> Any:
    with Path(path).open("rb") as stream:
        raw = stream.read(MAX_INPUT_BYTES + 1)
    if len(raw) > MAX_INPUT_BYTES:
        raise ContractError(f"Input exceeds {MAX_INPUT_BYTES} bytes")
    try:
        return decode_json(raw.decode("utf-8"))
    except UnicodeError as exc:
        raise ContractError("Input must be UTF-8") from exc


def obj(**properties: Any) -> dict[str, Any]:
    return {"type": "object", "properties": properties,
            "required": list(properties), "additionalProperties": False}


def text(max_length: int = 4000) -> dict[str, Any]:
    return {"type": "string", "minLength": 1, "maxLength": max_length}


def number(maximum: int, minimum: int = 0) -> dict[str, Any]:
    return {"type": "integer", "minimum": minimum, "maximum": maximum}


def array(items: Any, maximum: int = 32, minimum: int = 0) -> dict[str, Any]:
    return {"type": "array", "items": items, "minItems": minimum,
            "maxItems": maximum, "uniqueItems": True}


ID = {**text(128), "pattern": "^[a-zA-Z0-9][a-zA-Z0-9_.:-]*$"}
HASH = {"type": "string", "pattern": "^[0-9a-f]{64}$"}
ACTION = {"enum": ["emit_report", "request_human_review"]}
BINDING = {"run_id": ID, "snapshot": HASH, "mission_fingerprint": HASH}
USAGE = obj(model_calls=number(100, 1), tokens=number(1_000_000))
VERSION = {"const": 1, "type": "integer"}

# This is deliberately a simulation-only v1 contract, not a universal runtime DSL.
DEFINITIONS: dict[str, Any] = {
    "mission": obj(
        schema_version=VERSION, mission_id=ID, revision=number(1_000_000, 1),
        execution_mode={"const": "simulation"}, objective=text(),
        scope=array(ID, minimum=1), event_sources=array(ID, minimum=1),
        allowed_actions=array(ACTION, 2, 1), approval_required=array(ACTION, 2),
        approvers=array(ID), required_checks=array(ID, minimum=1),
        evidence_producers=array(ID, minimum=1), unresolved=array(text(500)),
        limits=obj(max_runs=number(100, 1), max_events=number(MAX_EVENTS, 1),
                   max_model_calls=number(100, 1), max_tokens=number(1_000_000, 1),
                   max_duration_seconds=number(86400, 1)),
    ),
    "observation": obj(run_id=ID, source=ID, origin={"enum": ["external", "supervisor"]},
                       scope=ID, snapshot=HASH),
    "proposal": obj(
        **BINDING, proposal_id=ID, action=ID, summary=text(), usage=USAGE,
        classification={"enum": ["demonstrated_violation", "hypothesis",
                                  "requirement_gap", "no_material_finding"]},
    ),
    "approval": obj(**BINDING, proposal_fingerprint=HASH, approver=ID,
                    expires_at=number(2**53 - 1)),
    "receipt": obj(**BINDING, proposal_fingerprint=HASH, operation_id=ID,
                   outcome={"enum": ["succeeded", "failed", "unknown"]}),
    "evidence": obj(**BINDING, proposal_fingerprint=HASH, operation_id=ID,
                    evidence_id=ID, check=ID, producer=ID,
                    outcome={"enum": ["pass", "fail", "unknown"]}, artifact_digest=HASH),
}

RUN = obj(run_id=ID)
REASON = obj(run_id=ID, reason=text())
PAYLOADS = {
    "observe": {"$ref": "#/$defs/observation"},
    "investigate": RUN,
    "worker_result": {"$ref": "#/$defs/proposal"},
    "worker_failed": obj(run_id=ID, usage=USAGE, reason=text()),
    "approve": {"$ref": "#/$defs/approval"},
    "authorize": RUN,
    "execute": {"$ref": "#/$defs/receipt"},
    "reconcile": {"$ref": "#/$defs/receipt"},
    "evidence": {"$ref": "#/$defs/evidence"},
    "verify": RUN,
    "snapshot_changed": obj(run_id=ID, snapshot=HASH),
    "policy_changed": obj(run_id=ID, mission_fingerprint=HASH),
    "pause": REASON, "resume": REASON, "cancel": REASON, "no_action": REASON,
}
DEFINITIONS["event"] = {"oneOf": [
    obj(schema_version=VERSION, event_id=ID, at=number(2**53 - 1),
        kind={"const": kind}, payload=payload)
    for kind, payload in PAYLOADS.items()
]}
DEFINITIONS["scenario"] = obj(
    schema_version=VERSION, mission={"$ref": "#/$defs/mission"},
    events={"type": "array", "items": {"$ref": "#/$defs/event"}, "maxItems": MAX_EVENTS},
    expected={"type": "object", "propertyNames": ID,
              "additionalProperties": {"enum": list(STATES)}, "maxProperties": 100},
)


def schema(kind: str) -> dict[str, Any]:
    if kind not in DEFINITIONS:
        raise ContractError(f"Unknown contract: {kind}")
    return {"$schema": "https://json-schema.org/draft/2020-12/schema",
            "$ref": f"#/$defs/{kind}", "$defs": deepcopy(DEFINITIONS)}


@lru_cache(maxsize=16)
def _validator(kind: str) -> Any:
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        raise ContractError("Install orchestration tooling: pip install -e '.[orchestration]'") from exc
    spec = schema(kind)
    Draft202012Validator.check_schema(spec)
    return Draft202012Validator(spec)


def validate(kind: str, value: Any) -> None:
    error = next(_validator(kind).iter_errors(value), None)
    if error:
        path = ".".join(str(part) for part in error.absolute_path) or "$"
        raise ContractError(f"{kind} {path}: {error.message[:1500]}")
    if kind == "mission":
        if not set(value["approval_required"]) <= set(value["allowed_actions"]):
            raise ContractError("Approval actions must also be allowed actions")
        if value["approval_required"] and not value["approvers"]:
            raise ContractError("Approval-required missions need named approvers")
    if kind == "scenario":
        validate("mission", value["mission"])
        if len(value["events"]) > value["mission"]["limits"]["max_events"]:
            raise ContractError("Scenario exceeds mission event budget")
        previous = -1
        identities: dict[str, str] = {}
        for event in value["events"]:
            if event["at"] < previous:
                raise ContractError("Event time must be nondecreasing")
            previous = event["at"]
            digest = fingerprint(event)
            old = identities.setdefault(event["event_id"], digest)
            if old != digest:
                raise ContractError("Conflicting event_id in scenario")
