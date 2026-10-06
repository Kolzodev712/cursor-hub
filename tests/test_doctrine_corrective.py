#!/usr/bin/env python3
"""Regression tests for doctrine setup corrective behavior (schema v2)."""
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

from cursor_hub.doctrine.model import NOT_APPLICABLE, UNKNOWN, ComponentProfile
from cursor_hub.doctrine.render import load_answers_from_project, render_components_json
from cursor_hub.doctrine.routing import domains_for_component
from cursor_hub.doctrine.setup import run_setup
from cursor_hub.doctrine.setup_io import ScriptIO
from cursor_hub.doctrine.staging import load_staging, publish_answers
from cursor_hub.doctrine.validate import validate_doctrine_setup
from cursor_hub.doctrine.model import doctrine_paths


def _full_inputs() -> list[str]:
    return [
        "Repo duty text",
        "1,12",
        "startup time",
        "1",
        "y",
        "Inv: no duplicate orders",
        "D",
        "2",
        "n",
        "w",
    ]


class ComponentRoundTripTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.tmp, ".cursor", "doctrine"), exist_ok=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_interview_preserved_in_components_json(self) -> None:
        comp = ComponentProfile(
            id="md",
            patterns=["crates/md/**"],
            responsibility="Ingest feeds",
            concurrent_access="yes",
            explicit_sync="yes",
            atomics_usage="no",
            external_data="yes",
            latency_sensitive="yes",
            numeric_compute=NOT_APPLICABLE,
            extra_required_doctrine_refs=[".cursor/skills/engineering-doctrine/decision/io.md"],
        )
        from cursor_hub.doctrine.model import SetupAnswers

        ans = SetupAnswers(components=[comp])
        text = render_components_json(ans)
        reloaded = load_answers_from_project(
            {**doctrine_paths(self.tmp), "components": os.path.join(self.tmp, ".cursor", "doctrine", "c.json")},
            project_root=self.tmp,
        )
        # write to temp file for parser
        path = os.path.join(self.tmp, ".cursor", "doctrine", "components.json")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        reloaded = load_answers_from_project(doctrine_paths(self.tmp), project_root=self.tmp)
        self.assertEqual(len(reloaded.components), 1)
        c = reloaded.components[0]
        self.assertEqual(c.responsibility, "Ingest feeds")
        self.assertEqual(c.atomics_usage, "no")
        self.assertEqual(c.explicit_sync, "yes")
        self.assertIn("io.md", c.extra_required_doctrine_refs[0])
        self.assertIn("concurrency", domains_for_component(c))
        self.assertNotIn("atomics", domains_for_component(c))

    def test_mutex_without_atomics_does_not_map_atomics_domain(self) -> None:
        c = ComponentProfile(
            id="x",
            patterns=["src/**"],
            concurrent_access="yes",
            explicit_sync="yes",
            atomics_usage="no",
        )
        self.assertIn("concurrency", domains_for_component(c))
        self.assertNotIn("atomics", domains_for_component(c))

    def test_cancel_at_summary_does_not_approve(self) -> None:
        with mock.patch(
            "cursor_hub.doctrine.install_integration.run_setup",
            side_effect=lambda t, io, **kw: 1,
        ), mock.patch("sys.stdin.isatty", return_value=False), mock.patch(
            "sys.stdout.isatty", return_value=False
        ):
            from cursor_hub import installer

            installer.run_install(_REPO_ROOT, self.tmp, ["engineering-doctrine"], dry_run=False)
        inputs = _full_inputs()[:-1] + ["c"]
        rc = run_setup(self.tmp, ScriptIO(inputs=inputs))
        self.assertEqual(rc, 1)
        result = validate_doctrine_setup(self.tmp)
        self.assertFalse(result.ok_for_install)


class ApprovalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_w_required_for_approval(self) -> None:
        os.makedirs(os.path.join(self.tmp, ".cursor", "doctrine"), exist_ok=True)
        from cursor_hub.doctrine.model import SetupAnswers

        ans = SetupAnswers(repository_responsibility="Known")
        ok, _ = publish_answers(self.tmp, ans)
        self.assertTrue(ok)
        # Without lifecycle approved_at, validation must fail install check
        result = validate_doctrine_setup(self.tmp)
        self.assertFalse(result.ok_for_install)


if __name__ == "__main__":
    unittest.main()
