"""Structural/behavioral-contract tests for the opt-in fault-first pack.

Run from a full cursor-hub checkout: python3 -m unittest discover -s tests -v
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "packs/cursor/fault-first"
SKILL = ROOT / "skills/fault-first"

class FaultFirstPackTests(unittest.TestCase):
    def test_pack_manifest_and_skill(self):
        manifest = (PACK / "pack.yml").read_text()
        self.assertIn("name: fault-first", manifest)
        self.assertIn("- fault-first", manifest)
        self.assertNotIn("hooks_merge: true", manifest)
        skill = (SKILL / "SKILL.md").read_text()
        self.assertTrue(skill.startswith("---\n"))
        self.assertIn("name: fault-first", skill)
        self.assertIn("reference/method.md", skill)
        self.assertIn("reference/report.md", skill)

    def test_namespaced_command_and_agent(self):
        command = PACK / ".cursor/commands/fault-first__analyze.md"
        agent = PACK / ".cursor/agents/fault-first-analyst.md"
        self.assertTrue(command.is_file())
        self.assertTrue(agent.is_file())
        self.assertIn("read-only", command.read_text().lower())
        self.assertIn("fault-first", agent.read_text())

    def test_no_ambient_or_enforcement_side_effects(self):
        self.assertFalse((PACK / ".cursor/rules").exists())
        self.assertFalse((PACK / ".cursor/hooks").exists())
        self.assertFalse((PACK / ".cursor/doctrine").exists())
        self.assertFalse((PACK / ".cursor/hooks.fragment.json").exists())
        self.assertFalse((PACK / ".cursor/design-log").exists())

    def test_explicit_epistemic_and_stop_contract(self):
        texts = [
            (SKILL / "SKILL.md").read_text(),
            (SKILL / "reference/method.md").read_text(),
            (SKILL / "reference/report.md").read_text(),
        ]
        combined = "\n".join(texts)
        for token in ("CONFIRMED_DEFECT", "CREDIBLE_HYPOTHESIS", "REQUIREMENT_GAP", "EXCLUDED", "UNKNOWN", "NOT_APPLICABLE", "falsif", "STOP"):
            self.assertIn(token.lower(), combined.lower())
        self.assertIn("no automatic writes", combined.lower())
        self.assertIn("human approval", combined.lower())

    def test_source_refs_exist(self):
        for name in ("method.md", "report.md", "sources.md"):
            self.assertTrue((SKILL / "reference" / name).is_file())
        source = (SKILL / "reference/sources.md").read_text()
        self.assertIn("IEC 60812", source)
        self.assertIn("IEC 61025", source)
        self.assertIn("NIST", source)

    def test_bounded_scope_in_skill_and_command(self):
        combined = (
            (SKILL / "SKILL.md").read_text()
            + (PACK / ".cursor/commands/fault-first__analyze.md").read_text()
        )
        lower = combined.lower()
        self.assertTrue("3–7" in combined or "3-7" in combined)
        self.assertIn("at most three", lower)
        self.assertIn("confirmed_defect", lower)

    def test_install_smoke_no_hooks(self):
        import shutil
        import subprocess
        import sys
        import tempfile

        tmp = tempfile.mkdtemp(prefix="ff-smoke-")
        try:
            subprocess.run(
                [sys.executable, "-m", "cursor_hub.cli", "install", "fault-first", tmp],
                cwd=ROOT,
                env={**__import__("os").environ, "PYTHONPATH": str(ROOT)},
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertFalse((Path(tmp) / ".cursor/hooks.json").exists())
            self.assertTrue((Path(tmp) / ".cursor/commands/fault-first__analyze.md").is_file())
            self.assertTrue((Path(tmp) / ".cursor/skills/fault-first/SKILL.md").is_file())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
