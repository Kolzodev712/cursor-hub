"""Pure, bounded reference supervisor over recorded fixture events.

No event invokes a model, shell, network, repository tool, or physical device.
Approver/producer identities and receipts are fixture assertions, NOT authenticated
permissions or real execution evidence. A live runtime must replace that boundary.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any

from .contracts import ContractError, TERMINAL, fingerprint, validate


def initial_state() -> dict[str, Any]:
    return {"runs": {}, "seen": {}, "observations": {}, "last_at": -1}


def _fresh(run: dict[str, Any], record: dict[str, Any]) -> bool:
    return (record["run_id"] == run["run_id"]
            and record["snapshot"] == run["snapshot"] == run["initial_snapshot"]
            and record["mission_fingerprint"] == run["mission_fingerprint"] == run["initial_policy"])


def _bound(run: dict[str, Any], record: dict[str, Any]) -> bool:
    return _fresh(run, record) and record["proposal_fingerprint"] == run["proposal_fingerprint"]


def _approval_ok(run: dict[str, Any], mission: dict[str, Any], at: int) -> bool:
    if run["proposal"]["action"] not in mission["approval_required"]:
        return True
    approval = run["approval"]
    return bool(approval and _bound(run, approval)
                and approval["approver"] in mission["approvers"] and at < approval["expires_at"])


def transition(state: dict[str, Any], event: dict[str, Any], mission: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return a new state and decision; never mutate caller-owned input."""
    validate("event", event)
    validate("mission", mission)
    new = deepcopy(state)
    event_hash = fingerprint(event)
    if event["event_id"] in new["seen"]:
        if new["seen"][event["event_id"]] != event_hash:
            raise ContractError("Conflicting event identity")
        return new, {"result": "ignored", "reason": "duplicate_event"}
    if event["at"] < new["last_at"]:
        raise ContractError("Event time moved backwards")
    if len(new["seen"]) >= mission["limits"]["max_events"]:
        raise ContractError("Event budget exhausted")
    new["seen"][event["event_id"]] = event_hash
    new["last_at"] = event["at"]
    kind, payload, at = event["kind"], event["payload"], event["at"]
    run_id = payload["run_id"]
    policy = fingerprint(mission)

    def answer(result: str, reason: str) -> tuple[dict[str, Any], dict[str, Any]]:
        return new, {"result": result, "reason": reason, "run_id": run_id}

    if kind == "observe":
        if payload["origin"] != "external":
            return answer("ignored", "self_trigger")
        if payload["source"] not in mission["event_sources"] or payload["scope"] not in mission["scope"]:
            return answer("ignored", "outside_mission")
        key = fingerprint([policy, payload["scope"], payload["snapshot"]])
        if key in new["observations"]:
            return answer("ignored", "duplicate_observation")
        if run_id in new["runs"]:
            raise ContractError("run_id already identifies a different observation")
        if len(new["runs"]) >= mission["limits"]["max_runs"]:
            return answer("ignored", "run_budget")
        run = {
            "run_id": run_id, "state": "BLOCKED" if mission["unresolved"] else "ADMITTED",
            "scope": payload["scope"], "snapshot": payload["snapshot"],
            "initial_snapshot": payload["snapshot"], "mission_fingerprint": policy,
            "initial_policy": policy, "started_at": at, "paused": False,
            "model_calls": 0, "tokens": 0, "proposal": None, "proposal_fingerprint": None,
            "approval": None, "receipt": None, "evidence": {},
        }
        new["runs"][run_id] = run
        new["observations"][key] = run_id
        return answer("accepted", "unresolved_mission" if mission["unresolved"] else "admitted")
    run = new["runs"].get(run_id)
    if run is None:
        return answer("rejected_event", "unknown_run")
    if run["state"] in TERMINAL:
        return answer("rejected_event", "terminal_run")
    if run["paused"] and kind not in {"resume", "cancel", "snapshot_changed", "policy_changed", "reconcile"}:
        return answer("rejected_event", "paused")

    if kind in {"pause", "resume"}:
        run["paused"] = kind == "pause"
        return answer("accepted", kind)
    if kind == "cancel":
        if run["state"] == "OUTCOME_UNKNOWN":
            return answer("rejected_event", "reconcile_before_cancelling")
        run["state"] = "CANCELLED"
        return answer("accepted", "cancelled")
    if kind in {"snapshot_changed", "policy_changed"}:
        field = "snapshot" if kind == "snapshot_changed" else "mission_fingerprint"
        run[field] = payload[field]
        return answer("accepted", kind)

    allowed = {
        "investigate": {"ADMITTED"}, "worker_result": {"INVESTIGATING"},
        "worker_failed": {"INVESTIGATING"}, "no_action": {"ADMITTED"},
        "approve": {"PROPOSED", "AWAITING_APPROVAL", "AUTHORIZED"},
        "authorize": {"PROPOSED", "AWAITING_APPROVAL"},
        "execute": {"AUTHORIZED"}, "reconcile": {"OUTCOME_UNKNOWN"},
        "evidence": {"EXECUTED"}, "verify": {"EXECUTED"},
    }
    if run["state"] not in allowed.get(kind, set()):
        return answer("rejected_event", "illegal_transition")
    limits = mission["limits"]
    if kind in {"investigate", "worker_result", "worker_failed", "authorize", "execute"}:
        if at - run["started_at"] > limits["max_duration_seconds"]:
            run["state"] = "BLOCKED"
            return answer("accepted", "deadline_exhausted")
    if kind == "investigate":
        if run["model_calls"] >= limits["max_model_calls"] or run["tokens"] >= limits["max_tokens"]:
            run["state"] = "BLOCKED"
            return answer("accepted", "worker_budget_exhausted")
        run["state"] = "INVESTIGATING"
        return answer("accepted", "investigating_fixture")
    if kind in {"worker_result", "worker_failed"}:
        run["model_calls"] += payload["usage"]["model_calls"]
        run["tokens"] += payload["usage"]["tokens"]
        if run["model_calls"] > limits["max_model_calls"] or run["tokens"] > limits["max_tokens"]:
            run["state"] = "BLOCKED"
            return answer("accepted", "worker_budget_exhausted")
        if kind == "worker_failed":
            exhausted = (run["model_calls"] >= limits["max_model_calls"] or run["tokens"] >= limits["max_tokens"])
            run["state"] = "BLOCKED" if exhausted else "ADMITTED"
            return answer("accepted", "worker_budget_exhausted" if exhausted else "bounded_retry_available")
        if not _fresh(run, payload):
            run["state"] = "BLOCKED"
            return answer("accepted", "stale_proposal")
        if payload["action"] not in mission["allowed_actions"]:
            run["state"] = "REJECTED"
            return answer("accepted", "action_not_allowed")
        run["proposal"] = deepcopy(payload)
        run["proposal_fingerprint"] = fingerprint(payload)
        run["state"] = "PROPOSED"
        return answer("accepted", "proposal_recorded")
    if kind == "no_action":
        run["state"] = "NO_ACTION"
        return answer("accepted", "no_action_not_a_correctness_claim")
    if kind == "approve":
        if not _bound(run, payload) or payload["approver"] not in mission["approvers"] or at >= payload["expires_at"]:
            return answer("rejected_event", "invalid_approval")
        run["approval"] = deepcopy(payload)
        return answer("accepted", "fixture_approval_recorded")
    if kind in {"authorize", "execute", "verify"}:
        if not _fresh(run, run["proposal"]):
            run["state"] = "BLOCKED"
            return answer("accepted", "stale_snapshot_or_policy")
    if kind == "authorize":
        run["state"] = "AUTHORIZED" if _approval_ok(run, mission, at) else "AWAITING_APPROVAL"
        return answer("accepted", "authorization_evaluated")
    if kind in {"execute", "reconcile"}:
        # Reconciliation refers to the original attempted operation, even if the
        # world changed while its outcome was unknown. It never retries it.
        original = run["proposal"]
        binding_ok = (payload["run_id"] == original["run_id"]
                      and payload["snapshot"] == original["snapshot"]
                      and payload["mission_fingerprint"] == original["mission_fingerprint"]
                      and payload["proposal_fingerprint"] == run["proposal_fingerprint"])
        if not binding_ok:
            return answer("rejected_event", "receipt_binding_mismatch")
        if kind == "execute" and not _approval_ok(run, mission, at):
            run["state"] = "BLOCKED"
            return answer("accepted", "approval_expired_or_missing")
        if kind == "reconcile":
            if payload["operation_id"] != run["receipt"]["operation_id"] or payload["outcome"] == "unknown":
                return answer("rejected_event", "invalid_reconciliation")
        run["receipt"] = deepcopy(payload)
        run["state"] = {"succeeded": "EXECUTED", "failed": "FAILED", "unknown": "OUTCOME_UNKNOWN"}[payload["outcome"]]
        return answer("accepted", "simulated_receipt_recorded")
    if kind == "evidence":
        if (not _bound(run, payload) or payload["operation_id"] != run["receipt"]["operation_id"]
                or payload["producer"] not in mission["evidence_producers"]
                or payload["check"] not in mission["required_checks"]):
            return answer("rejected_event", "untrusted_or_unbound_evidence")
        existing = run["evidence"].get(payload["evidence_id"])
        if existing is not None and existing != payload:
            raise ContractError("Evidence identity reused with different content")
        run["evidence"][payload["evidence_id"]] = deepcopy(payload)
        return answer("accepted", "fixture_evidence_recorded")
    if kind == "verify":
        evidence = list(run["evidence"].values())
        if any(item["outcome"] == "fail" for item in evidence):
            run["state"] = "FAILED"
        elif (any(item["outcome"] == "unknown" for item in evidence)
              or {item["check"] for item in evidence} != set(mission["required_checks"])):
            run["state"] = "BLOCKED"
        else:
            run["state"] = "VERIFIED"
        return answer("accepted", "simulated_checks_evaluated")
    raise ContractError(f"Unhandled event: {kind}")
