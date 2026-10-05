#!/usr/bin/env python3
"""Structural tests for layered engineering-doctrine layout."""
from __future__ import annotations

import os
import re
import sys
import unittest

_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SKILL = os.path.join(_REPO_ROOT, "skills", "engineering-doctrine")


class DoctrineStructureTests(unittest.TestCase):
    def test_no_legacy_reference_dir(self) -> None:
        self.assertFalse(os.path.isdir(os.path.join(SKILL, "reference")))

    def test_decision_domains_present(self) -> None:
        decision = os.path.join(SKILL, "decision")
        names = {f for f in os.listdir(decision) if f.endswith(".md")}
        for required in (
            "algorithm-selection.md",
            "cpu-execution.md",
            "evidence.md",
            "memory.md",
        ):
            self.assertIn(required, names)

    def test_technique_links_to_existing_domain(self) -> None:
        simd = read(os.path.join(SKILL, "techniques", "simd.md"))
        m = re.search(r"^## Parent decision domain\s*\n\s*([a-z0-9-]+)", simd, re.MULTILINE)
        self.assertIsNotNone(m)
        parent = m.group(1) + ".md"
        self.assertTrue(os.path.isfile(os.path.join(SKILL, "decision", parent)))

    def test_skill_router_no_stale_reference_paths(self) -> None:
        skill = read(os.path.join(SKILL, "SKILL.md"))
        self.assertNotIn("reference/", skill)

    def test_components_example_uses_decision_path(self) -> None:
        doc = read(os.path.join(_REPO_ROOT, "docs", "engineering-doctrine.md"))
        self.assertIn("decision/", doc)
        self.assertNotIn("reference/algorithm-selection", doc)


def read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    unittest.main()
