"""CLI registration is dependency-light; jsonschema is loaded only when validating."""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys

from .contracts import ContractError, DEFINITIONS, fingerprint, load_json, schema, validate
from .journal import replay, simulate


def run(args: argparse.Namespace) -> int:
    try:
        if args.orchestration_cmd == "schema":
            result = schema(args.kind)
        elif args.orchestration_cmd == "validate":
            value = load_json(args.path)
            validate(args.kind, value)
            mission = value if args.kind == "mission" else value.get("mission") if args.kind == "scenario" else None
            unresolved = mission["unresolved"] if mission else []
            result = {"valid": True, "kind": args.kind, "fingerprint": fingerprint(value),
                      "simulation_ready": not bool(unresolved), "unresolved": unresolved,
                      "live_execution": False}
            print(json.dumps(result, indent=2))
            return 3 if unresolved else 0
        elif args.orchestration_cmd == "simulate":
            if args.journal:
                from pathlib import Path
                if Path(args.path).resolve() == Path(args.journal).resolve():
                    raise ContractError("Input and journal must be different files")
            result = simulate(load_json(args.path), args.journal, args.steps)
        else:
            result = replay(args.journal)
        print(json.dumps(result, indent=2))
        return 1 if result.get("expectations_met") is False else 0
    except (ContractError, OSError, sqlite3.Error) as exc:
        print(f"orchestration: {exc}", file=sys.stderr)
        return 2


def configure_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("orchestration", help="Validate contracts and simulate recorded events; never run live agents")
    commands = parser.add_subparsers(dest="orchestration_cmd", required=True)
    command = commands.add_parser("schema", help="Print a bundled JSON Schema (no file writes)")
    command.add_argument("kind", choices=sorted(DEFINITIONS))
    command.set_defaults(func=run)
    command = commands.add_parser("validate", help="Validate a JSON contract; unresolved mission facts exit 3")
    command.add_argument("path")
    command.add_argument("--kind", choices=sorted(DEFINITIONS), default="scenario")
    command.set_defaults(func=run)
    command = commands.add_parser("simulate", help="Process fixtures in memory, or explicitly checkpoint to --journal")
    command.add_argument("path")
    command.add_argument("--journal", help="Explicit local SQLite checkpoint path; never a project target")
    command.add_argument("--steps", type=int, help="Maximum additional events; 0 creates/checks a checkpoint only")
    command.set_defaults(func=run)
    command = commands.add_parser("replay", help="Reconstruct a journal without advancing or writing it")
    command.add_argument("--journal", required=True)
    command.set_defaults(func=run)


def main() -> int:
    parser = argparse.ArgumentParser(prog="python -m cursor_hub.orchestration")
    subparsers = parser.add_subparsers(dest="command", required=True)
    configure_parser(subparsers)
    # Same arguments as the root CLI after its `orchestration` subcommand.
    args = parser.parse_args(["orchestration", *sys.argv[1:]])
    return args.func(args)
