#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import sys
import tempfile
import unittest

_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from cursor_hub.doctrine.markdown_merge import LEGACY_RECONCILE_MARKER, merge_managed_markdown
from cursor_hub.doctrine.model import SetupAnswers
from cursor_hub.doctrine.render import MARKER_REPO, render_architecture
from cursor_hub.doctrine.setup import _persist_partial


class MarkdownPreservationTests(unittest.TestCase):
    def test_preamble_and_epilogue_survive_merge(self) -> None:
        existing = (
            "## Team notes\n\nKeep this paragraph.\n\n"
            "# Repository responsibility\n\nOLD BODY\n\n"
            f"{MARKER_REPO}\n\n"
            "## Appendix\n\nStill here.\n"
        )
        new_managed = render_architecture(SetupAnswers(repository_responsibility="NEW BODY"))
        merged = merge_managed_markdown(
            existing,
            new_managed,
            section_header="# Repository responsibility",
            marker=MARKER_REPO,
        )
        self.assertIn("Keep this paragraph.", merged)
        self.assertIn("NEW BODY", merged)
        self.assertNotIn("OLD BODY", merged)
        self.assertIn("## Appendix", merged)
        self.assertIn("Still here.", merged)

    def test_legacy_file_preserved_with_notice(self) -> None:
        legacy = "# Custom architecture essay\n\nWe do not use the wizard header.\n"
        new_managed = render_architecture(SetupAnswers(repository_responsibility="Managed"))
        merged = merge_managed_markdown(
            legacy,
            new_managed,
            section_header="# Repository responsibility",
            marker=MARKER_REPO,
        )
        self.assertIn("Custom architecture essay", merged)
        self.assertIn(LEGACY_RECONCILE_MARKER, merged)
        self.assertIn("Managed", merged)

    def test_persist_partial_preserves_preamble(self) -> None:
        tmp = tempfile.mkdtemp()
        try:
            path = os.path.join(tmp, ".cursor", "doctrine", "architecture.md")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write("## Human prose\n\nDo not delete.\n\n")
            ans = SetupAnswers(repository_responsibility="From wizard")
            _persist_partial(tmp, ans, ("architecture",))
            with open(path, encoding="utf-8") as f:
                text = f.read()
            self.assertIn("Do not delete.", text)
            self.assertIn("From wizard", text)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
