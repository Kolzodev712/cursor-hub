#!/usr/bin/env python3
"""Doctrine setup wizard, validation, routing, and install integration."""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import unittest
from unittest import mock

_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from cursor_hub import installer
from cursor_hub.doctrine.install_integration import post_install_doctrine_setup
from cursor_hub.doctrine.model import ComponentProfile, UNKNOWN, NOT_APPLICABLE
from cursor_hub.doctrine.routing import domains_for_component, doctrine_refs_for_component
from cursor_hub.doctrine.setup import run_setup
from cursor_hub.doctrine.setup_io import ScriptIO
from cursor_hub.doctrine.validate import validate_doctrine_setup
from cursor_hub.doctrine_enforcement import handle_gate_write
from cursor_hub.doctrine.inspect import inspect_repository


def minimal_setup_inputs(*, repo_text: str = "Consumes market data and routes orders.") -> list[str]:
    return [
        repo_text,
        "1,3",
        "1,2",
        "y",
        "",
        "2",
        "s",
        "n",
        "w",
    ]


def complete_minimal_setup(target: str, *, extra: list[str] | None = None) -> int:
    inputs = minimal_setup_inputs()
    if extra:
        inputs.extend(extra)
    return run_setup(target, ScriptIO(inputs=inputs))


class DoctrineRoutingTests(unittest.TestCase):
    def test_concurrent_maps_concurrency(self) -> None:
        c = ComponentProfile(id="x", patterns=["src/**"], concurrent_access="yes")
        self.assertIn("concurrency", domains_for_component(c))

    def test_atomics_and_numeric_and_io(self) -> None:
        c = ComponentProfile(
            id="x",
            patterns=["src/**"],
            explicit_sync="yes",
            numeric_compute="yes",
            external_data="yes",
            latency_sensitive="yes",
        )
        domains = domains_for_component(c)
        self.assertIn("atomics", domains)
        self.assertIn("cpu-execution", domains)
        self.assertIn("io", domains)
        self.assertIn("benchmarking", domains)
        self.assertIn("evidence", domains)
        refs = doctrine_refs_for_component(c)
        self.assertEqual(len(refs), len(set(refs)))
        self.assertIn("atomics", domains)

    def test_not_applicable_does_not_add_domains(self) -> None:
        c = ComponentProfile(id="x", patterns=["src/**"], concurrent_access=NOT_APPLICABLE)
        self.assertNotIn("concurrency", domains_for_component(c))

    def test_market_data_style_routing(self) -> None:
        """Human-reviewed scenario: concurrent + external I/O + perf; not atomics/numeric."""
        c = ComponentProfile(
            id="market-data",
            patterns=["crates/md/**"],
            concurrent_access="yes",
            explicit_sync="no",
            external_data="yes",
            latency_sensitive="yes",
            numeric_compute="no",
        )
        domains = domains_for_component(c)
        self.assertIn("concurrency", domains)
        self.assertIn("io", domains)
        self.assertIn("benchmarking", domains)
        self.assertNotIn("atomics", domains)
        self.assertNotIn("cpu-execution", domains)


class InspectTests(unittest.TestCase):
    def test_workspace_members_detected(self) -> None:
        tmp = tempfile.mkdtemp()
        try:
            os.makedirs(os.path.join(tmp, "crates", "a"), exist_ok=True)
            with open(os.path.join(tmp, "Cargo.toml"), "w", encoding="utf-8") as f:
                f.write('[workspace]\nmembers = ["crates/a"]\n')
            report = inspect_repository(tmp)
            self.assertTrue(report.rust_workspace)
            self.assertTrue(any("crates/a" in p for _, p in report.candidate_components))
        finally:
            shutil.rmtree(tmp)


class SetupWizardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp()
        self.target = self.tmp

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _install(self) -> None:
        rc = installer.run_install(
            _REPO_ROOT,
            self.target,
            ["engineering-doctrine"],
            dry_run=False,
        )
        self.assertEqual(rc, 0, "install should succeed after setup")

    def test_unknown_workload_allows_complete_with_unknowns(self) -> None:
        with mock.patch(
            "cursor_hub.doctrine.install_integration.run_setup",
            side_effect=lambda t, io, **kw: complete_minimal_setup(t),
        ), mock.patch("sys.stdin.isatty", return_value=True), mock.patch(
            "sys.stdout.isatty", return_value=True
        ):
            installer.run_install(
                _REPO_ROOT,
                self.target,
                ["engineering-doctrine"],
                dry_run=False,
            )
        inputs = [
            "Repo duty",
            "1",
            "u",
            "u",
            "u",
            "1",
            "u",
            "u",
            "s",
            "n",
            "w",
        ]
        rc = run_setup(self.tmp, ScriptIO(inputs=inputs))
        self.assertEqual(rc, 0)
        result = validate_doctrine_setup(self.tmp)
        self.assertEqual(result.status, "COMPLETE_WITH_UNKNOWNS")

    def test_resume_after_partial(self) -> None:
        with mock.patch(
            "cursor_hub.doctrine.install_integration.run_setup",
            side_effect=lambda t, io, **kw: 1,
        ), mock.patch("sys.stdin.isatty", return_value=True), mock.patch(
            "sys.stdout.isatty", return_value=True
        ):
            self.assertEqual(
                installer.run_install(_REPO_ROOT, self.target, ["engineering-doctrine"], dry_run=False),
                1,
            )
        io1 = ScriptIO(["First responsibility", "1", "1", "y"])
        # Stop early by not providing rest — simulate cancel at summary
        from cursor_hub.doctrine.setup import run_section_repository, run_section_objectives
        from cursor_hub.doctrine.render import load_answers_from_project
        from cursor_hub.doctrine.model import doctrine_paths

        answers = load_answers_from_project(doctrine_paths(self.tmp))
        report = inspect_repository(self.tmp)
        run_section_repository(self.tmp, answers, io1, report)
        run_section_objectives(self.tmp, answers, io1)
        result = validate_doctrine_setup(self.tmp)
        self.assertEqual(result.status, "INCOMPLETE")
        rc = complete_minimal_setup(self.tmp)
        self.assertEqual(rc, 0)
        result = validate_doctrine_setup(self.tmp)
        self.assertIn(result.status, ("COMPLETE", "COMPLETE_WITH_UNKNOWNS"))

    def test_other_objective_prompt_and_persistence(self) -> None:
        with mock.patch(
            "cursor_hub.doctrine.install_integration.run_setup",
            side_effect=lambda t, io, **kw: 1,
        ), mock.patch("sys.stdin.isatty", return_value=False), mock.patch(
            "sys.stdout.isatty", return_value=False
        ):
            installer.run_install(
                _REPO_ROOT,
                self.target,
                ["engineering-doctrine"],
                dry_run=False,
            )
        inputs = [
            "Repo duty",
            "1,12",
            "reproducibility",
            "1",
            "y",
            "u",
            "2",
            "s",
            "n",
            "w",
        ]
        rc = run_setup(self.tmp, ScriptIO(inputs=inputs))
        self.assertEqual(rc, 0)
        with open(os.path.join(self.tmp, ".cursor", "doctrine", "objectives.md"), encoding="utf-8") as f:
            text = f.read()
        self.assertIn("reproducibility", text)
        self.assertNotIn("- Other", text)

    def test_na_not_counted_as_unknown(self) -> None:
        with mock.patch(
            "cursor_hub.doctrine.install_integration.run_setup",
            side_effect=lambda t, io, **kw: complete_minimal_setup(t),
        ), mock.patch("sys.stdin.isatty", return_value=True), mock.patch(
            "sys.stdout.isatty", return_value=True
        ):
            installer.run_install(_REPO_ROOT, self.target, ["engineering-doctrine"], dry_run=False)
        rc = complete_minimal_setup(self.tmp)
        self.assertEqual(rc, 0)
        with open(os.path.join(self.tmp, ".cursor", "doctrine", "workload.md"), encoding="utf-8") as f:
            text = f.read()
        self.assertIn(NOT_APPLICABLE, text)


class InstallIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp()
        self.target = self.tmp

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_non_tty_fresh_install_fails(self) -> None:
        with mock.patch("sys.stdin.isatty", return_value=False), mock.patch(
            "sys.stdout.isatty", return_value=False
        ):
            rc = installer.run_install(
                _REPO_ROOT,
                self.target,
                ["engineering-doctrine"],
                dry_run=False,
            )
        self.assertEqual(rc, 1)
        self.assertTrue(
            os.path.isfile(os.path.join(self.target, ".cursor", "rules", "engineering-doctrine-ambient.mdc"))
        )

    def test_configured_reinstall_succeeds(self) -> None:
        with mock.patch(
            "cursor_hub.doctrine.install_integration.run_setup",
            side_effect=lambda t, io, **kw: complete_minimal_setup(t),
        ), mock.patch("sys.stdin.isatty", return_value=True), mock.patch(
            "sys.stdout.isatty", return_value=True
        ):
            rc = installer.run_install(
                _REPO_ROOT,
                self.target,
                ["engineering-doctrine"],
                dry_run=False,
            )
        self.assertEqual(rc, 0)
        with mock.patch("sys.stdin.isatty", return_value=False), mock.patch(
            "sys.stdout.isatty", return_value=False
        ):
            rc = installer.run_install(
                _REPO_ROOT,
                self.target,
                ["engineering-doctrine"],
                dry_run=False,
            )
        self.assertEqual(rc, 0)

    def test_dry_run_reports_incomplete(self) -> None:
        buf = []
        with mock.patch("builtins.print", side_effect=lambda *a, **k: buf.append(" ".join(str(x) for x in a))):
            rc = post_install_doctrine_setup(self.target, ["engineering-doctrine"], dry_run=True)
        self.assertEqual(rc, 0)
        joined = "\n".join(buf)
        self.assertIn("INCOMPLETE", joined)


class ValidationTests(unittest.TestCase):
    def test_stale_schema(self) -> None:
        tmp = tempfile.mkdtemp()
        try:
            d = os.path.join(tmp, ".cursor", "doctrine")
            os.makedirs(d, exist_ok=True)
            with open(os.path.join(d, "setup.json"), "w", encoding="utf-8") as f:
                json.dump({"schema_version": 0, "status": "COMPLETE"}, f)
            for name in ("architecture.md", "objectives.md", "invariants.md", "workload.md", "components.json"):
                open(os.path.join(d, name), "w", encoding="utf-8").close()
            result = validate_doctrine_setup(tmp)
            self.assertEqual(result.status, "STALE_SCHEMA")
        finally:
            shutil.rmtree(tmp)


class HookSetupGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp()
        self.target = self.tmp

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_incomplete_setup_blocks_write(self) -> None:
        with mock.patch("sys.stdin.isatty", return_value=False), mock.patch(
            "sys.stdout.isatty", return_value=False
        ):
            installer.run_install(_REPO_ROOT, self.target, ["engineering-doctrine"], dry_run=False)
        payload = {
            "tool_name": "Write",
            "tool_input": {"path": "src/main.rs"},
            "workspace_root": self.target,
        }
        out = handle_gate_write(payload, self.target)
        self.assertEqual(out["permission"], "deny")

    def test_complete_with_unknowns_allows_unclassified_write(self) -> None:
        with mock.patch(
            "cursor_hub.doctrine.install_integration.run_setup",
            side_effect=lambda t, io, **kw: complete_minimal_setup(t),
        ), mock.patch("sys.stdin.isatty", return_value=True), mock.patch(
            "sys.stdout.isatty", return_value=True
        ):
            installer.run_install(_REPO_ROOT, self.target, ["engineering-doctrine"], dry_run=False)
        payload = {
            "tool_name": "Write",
            "tool_input": {"path": "src/main.rs"},
            "workspace_root": self.target,
        }
        out = handle_gate_write(payload, self.target)
        self.assertEqual(out["permission"], "allow")


if __name__ == "__main__":
    unittest.main()
