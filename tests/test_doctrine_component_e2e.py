#!/usr/bin/env python3
"""End-to-end component interview, cancel/resume, and approval contract."""
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
from cursor_hub.doctrine.model import NOT_APPLICABLE, UNKNOWN, doctrine_paths
from cursor_hub.doctrine.render import load_answers_from_project
from cursor_hub.doctrine.routing import domains_for_component
from cursor_hub.doctrine.setup import run_setup
from cursor_hub.doctrine.setup_io import ScriptIO
from cursor_hub.doctrine.staging import load_staging
from cursor_hub.doctrine.validate import validate_doctrine_setup


def _component_wizard_inputs(*, final: str) -> list[str]:
    traits = ["y", "n", "u", "na", "y", "n", "u", "na", "y", "n", "u", "na", "y", "n"]
    return [
        "Routes orders in the larger system.",
        "1",
        "1",
        "y",
        "Must not duplicate live orders",
        "d",
        "2",
        "y",
        "order-router",
        "src/router/**",
        "Matches venues to internal order ids.",
        *traits,
        final,
    ]


class ComponentLifecycleE2ETests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _install(self) -> None:
        with mock.patch("sys.stdin.isatty", return_value=False), mock.patch(
            "sys.stdout.isatty", return_value=False
        ):
            rc = installer.run_install(_REPO_ROOT, self.tmp, ["engineering-doctrine"], dry_run=False)
        self.assertEqual(rc, 1)

    def test_cancel_then_resume_approve_round_trip(self) -> None:
        self._install()
        rc = run_setup(self.tmp, ScriptIO(inputs=_component_wizard_inputs(final="c")))
        self.assertEqual(rc, 1)
        setup_path = doctrine_paths(self.tmp)["setup"]
        with open(setup_path, encoding="utf-8") as f:
            meta = json.load(f)
        self.assertIsNone(meta.get("approved_at"))
        staged = load_staging(self.tmp)
        self.assertIsNotNone(staged)
        assert staged is not None
        self.assertEqual(len(staged.components), 1)
        c = staged.components[0]
        self.assertEqual(c.responsibility, "Matches venues to internal order ids.")
        self.assertEqual(c.concurrent_access, "yes")
        self.assertEqual(c.atomics_usage, UNKNOWN)
        self.assertEqual(c.explicit_sync, "no")

        rc2 = run_setup(self.tmp, ScriptIO(inputs=["w"]))
        self.assertEqual(rc2, 0)
        with open(setup_path, encoding="utf-8") as f:
            meta2 = json.load(f)
        self.assertTrue(meta2.get("approved_at"))
        reloaded = load_answers_from_project(doctrine_paths(self.tmp), project_root=self.tmp)
        self.assertEqual(reloaded.components[0].responsibility, c.responsibility)
        comp_path = doctrine_paths(self.tmp)["components"]
        with open(comp_path, encoding="utf-8") as f:
            raw = json.load(f)
        interview = raw["components"][0]["interview"]
        self.assertEqual(interview["traits"]["atomics_usage"], UNKNOWN)
        self.assertIn("concurrency", domains_for_component(reloaded.components[0]))
        result = validate_doctrine_setup(self.tmp)
        self.assertIn(result.status, ("COMPLETE", "COMPLETE_WITH_UNKNOWNS"))


if __name__ == "__main__":
    unittest.main()
