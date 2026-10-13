"""Transactional SQLite checkpoints for offline simulation, not a live scheduler.

One invocation commits a prefix atomically. An interrupted transaction rolls back;
resume replays the last committed prefix. No external effect needs compensating.
Hashes detect accidental inconsistency, not a malicious writer with database access.
"""
from __future__ import annotations

import os
import sqlite3
import stat
from pathlib import Path
from typing import Any

from .contracts import ContractError, MAX_INPUT_BYTES, canonical, decode_json, fingerprint, validate
from .simulation import initial_state, transition

FORMAT_VERSION = 1
APPLICATION_ID = 0x43554831


def _connect(path: str | Path | None, *, readonly: bool = False) -> tuple[sqlite3.Connection, bool]:
    if path is None:
        if readonly:
            raise ContractError("Replay requires an existing journal")
        return sqlite3.connect(":memory:", isolation_level=None), True
    target = Path(path).absolute()
    created = False
    try:
        info = target.lstat()
    except FileNotFoundError:
        if readonly:
            raise ContractError("Journal does not exist") from None
        fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        os.close(fd)
        created = True
    else:
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise ContractError("Journal must be a regular, non-symlink, single-link file")
    mode = "ro" if readonly else "rw"
    db = sqlite3.connect(target.as_uri() + f"?mode={mode}", uri=True, timeout=5, isolation_level=None)
    if not created and db.execute("PRAGMA application_id").fetchone()[0] != APPLICATION_ID:
        db.close()
        raise ContractError("Not a cursor-hub simulation journal; refusing to modify it")
    db.execute("PRAGMA trusted_schema=OFF")
    return db, created


def _create(db: sqlite3.Connection, scenario: dict[str, Any]) -> None:
    db.execute(f"PRAGMA application_id={APPLICATION_ID}")
    db.execute("CREATE TABLE header (id INTEGER PRIMARY KEY CHECK(id=1), version INTEGER NOT NULL, "
               "scenario TEXT NOT NULL, digest TEXT NOT NULL, checkpoint INTEGER NOT NULL, state_hash TEXT NOT NULL)")
    db.execute("CREATE TABLE events (seq INTEGER PRIMARY KEY, input TEXT NOT NULL, "
               "decision TEXT NOT NULL, state_hash TEXT NOT NULL)")
    db.execute("INSERT INTO header VALUES (1,?,?,?,?,?)",
               (FORMAT_VERSION, canonical(scenario), fingerprint(scenario), 0, fingerprint(initial_state())))


def _read(db: sqlite3.Connection) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    header = db.execute("SELECT version,scenario,digest,checkpoint,state_hash FROM header WHERE id=1").fetchone()
    if not header or header[0] != FORMAT_VERSION:
        raise ContractError("Unsupported or missing journal format; no automatic migration")
    if len(header[1].encode("utf-8")) > MAX_INPUT_BYTES:
        raise ContractError("Journal scenario exceeds input size limit")
    scenario = decode_json(header[1])
    validate("scenario", scenario)
    if fingerprint(scenario) != header[2]:
        raise ContractError("Journal scenario hash mismatch")
    rows = db.execute("SELECT seq,input,decision,state_hash FROM events ORDER BY seq LIMIT 1001").fetchall()
    if len(rows) != header[3] or len(rows) > len(scenario["events"]):
        raise ContractError("Journal checkpoint/count mismatch")
    state = initial_state()
    history: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        event = scenario["events"][index]
        if row[0] != index + 1 or row[1] != canonical(event):
            raise ContractError("Journal event order/content mismatch")
        state, decision = transition(state, event, scenario["mission"])
        if row[2] != canonical(decision) or row[3] != fingerprint(state):
            raise ContractError("Journal replay mismatch (corruption or incompatible reducer)")
        history.append({"seq": index + 1, "event_id": event["event_id"], **decision})
    if fingerprint(state) != header[4]:
        raise ContractError("Journal checkpoint state mismatch")
    return scenario, state, history


def _report(scenario: dict[str, Any], state: dict[str, Any], history: list[dict[str, Any]]) -> dict[str, Any]:
    complete = len(history) == len(scenario["events"])
    statuses = {key: run["state"] for key, run in state["runs"].items()}
    return {
        "mode": "simulation", "live_execution": False,
        "scenario_fingerprint": fingerprint(scenario), "processed": len(history),
        "total": len(scenario["events"]), "complete": complete,
        "expectations_met": statuses == scenario["expected"] if complete else None,
        "state": state, "history": history,
    }


def simulate(scenario: dict[str, Any], journal: str | Path | None = None, steps: int | None = None) -> dict[str, Any]:
    """Process at most `steps` additional events. Omit journal for no file writes."""
    validate("scenario", scenario)
    if len(canonical(scenario).encode("utf-8")) > MAX_INPUT_BYTES:
        raise ContractError("Scenario exceeds input size limit")
    if steps is not None and (type(steps) is not int or steps < 0):
        raise ContractError("steps must be a nonnegative integer")
    db, created = _connect(journal)
    try:
        db.execute("PRAGMA synchronous=FULL")
        db.execute("BEGIN IMMEDIATE")  # Serialize appenders, including their replay/read.
        if created:
            _create(db, scenario)
        stored, state, history = _read(db)
        if fingerprint(stored) != fingerprint(scenario):
            raise ContractError("Scenario/mission changed; use a new journal")
        start = len(history)
        stop = len(scenario["events"]) if steps is None else min(start + steps, len(scenario["events"]))
        for index in range(start, stop):
            event = scenario["events"][index]
            state, decision = transition(state, event, scenario["mission"])
            db.execute("INSERT INTO events VALUES (?,?,?,?)",
                       (index + 1, canonical(event), canonical(decision), fingerprint(state)))
            history.append({"seq": index + 1, "event_id": event["event_id"], **decision})
        db.execute("UPDATE header SET checkpoint=?,state_hash=? WHERE id=1", (len(history), fingerprint(state)))
        db.commit()
        return _report(scenario, state, history)
    except BaseException:
        db.rollback()
        raise
    finally:
        db.close()


def replay(journal: str | Path) -> dict[str, Any]:
    """Read-only reconstruction; neither advances the journal nor invokes a worker."""
    db, _ = _connect(journal, readonly=True)
    try:
        db.execute("BEGIN")  # Read header and events from one consistent snapshot.
        scenario, state, history = _read(db)
        return _report(scenario, state, history)
    finally:
        db.close()
