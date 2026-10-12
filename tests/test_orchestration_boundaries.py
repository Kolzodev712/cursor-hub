"""Additional isolation, optional-dependency and concurrent checkpoint tests."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from cursor_hub.orchestration.contracts import ContractError
from cursor_hub.orchestration.journal import replay, simulate

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "skills/system-orchestration/examples/repository-analysis.json"
HAS_VALIDATOR = importlib.util.find_spec("jsonschema") is not None


class OptionalDependencyTests(unittest.TestCase):
    def invoke_without_site_packages(self, *args):
        return subprocess.run([sys.executable, "-S", "-m", "cursor_hub", *args], cwd=ROOT, text=True, capture_output=True, timeout=30)

    def test_legacy_help_without_optional_dependency(self):
        for args in (("install", "--help"), ("doctrine", "status", "--help")):
            with self.subTest(args=args):
                result = self.invoke_without_site_packages(*args)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_schema_export_without_optional_dependency(self):
        result = self.invoke_without_site_packages("orchestration", "schema", "mission")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("$defs", json.loads(result.stdout))

    def test_missing_optional_dependency_has_actionable_error(self):
        result = self.invoke_without_site_packages("orchestration", "validate", str(FIXTURE))
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn(".[orchestration]", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


@unittest.skipUnless(HAS_VALIDATOR, "install .[orchestration] to run orchestration tests")
class PersistenceBoundaryTests(unittest.TestCase):
    def fixture(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_two_appenders_serialize_without_duplicate_progress(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "simulation.sqlite"
            fixture = self.fixture()
            simulate(fixture, path, steps=0)
            with ThreadPoolExecutor(max_workers=2) as pool:
                futures = [pool.submit(simulate, fixture, path, 3) for _ in range(2)]
                reports = [future.result(timeout=20) for future in futures]
            self.assertEqual(sorted(report["processed"] for report in reports), [3, 6])
            self.assertEqual(replay(path)["processed"], 6)
            self.assertEqual(simulate(fixture, path), simulate(fixture))

    def test_hardlinked_journal_is_refused_without_modification(self):
        if not hasattr(os, "link"):
            self.skipTest("hardlinks unavailable")
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "simulation.sqlite"
            alias = Path(folder) / "alias.sqlite"
            simulate(self.fixture(), path, steps=0)
            before = path.read_bytes()
            os.link(path, alias)
            with self.assertRaises(ContractError):
                simulate(self.fixture(), alias)
            self.assertEqual(path.read_bytes(), before)

    def test_in_memory_default_leaves_working_directory_unchanged(self):
        fixture = self.fixture()
        script = "import json,sys; from cursor_hub.orchestration.journal import simulate; simulate(json.loads(sys.stdin.read()))"
        with tempfile.TemporaryDirectory() as folder:
            environment = dict(os.environ, PYTHONPATH=str(ROOT), PYTHONDONTWRITEBYTECODE="1")
            result = subprocess.run([sys.executable, "-c", script], input=json.dumps(fixture), cwd=folder, env=environment, text=True, capture_output=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(list(Path(folder).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
