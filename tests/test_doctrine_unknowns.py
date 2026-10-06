#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import unittest

_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from cursor_hub.doctrine.model import NOT_APPLICABLE, UNKNOWN, ComponentProfile, SetupAnswers
from cursor_hub.doctrine.unknowns import apply_unknown_resolution, collect_unknown_fields


class UnknownReviewTests(unittest.TestCase):
    def test_na_not_listed_as_unknown(self) -> None:
        comp = ComponentProfile(id="x", patterns=["p/**"], latency_sensitive=NOT_APPLICABLE)
        ans = SetupAnswers(
            repository_responsibility="Done",
            objectives_selected=["Correctness"],
            objectives_priority=["Correctness"],
            objectives_per_component="yes",
            invariants=["Always valid"],
            performance_importance="no",
            components=[comp],
        )
        ids = {r.field_id for r in collect_unknown_fields(ans)}
        self.assertNotIn("component.x.trait.latency_sensitive", ids)

    def test_resolve_workload_field_only(self) -> None:
        ans = SetupAnswers(
            repository_responsibility="R",
            objectives_selected=["Correctness"],
            objectives_priority=["Correctness"],
            objectives_per_component="yes",
            invariants=["I"],
            performance_importance="yes",
            workload_fields={"Latency target": UNKNOWN, "Other fact": "10ms"},
        )
        ok, err = apply_unknown_resolution(ans, "workload.field.Latency target", "5ms p99")
        self.assertTrue(ok)
        self.assertIsNone(err)
        self.assertEqual(ans.workload_fields["Latency target"], "5ms p99")
        self.assertEqual(ans.workload_fields["Other fact"], "10ms")

    def test_component_trait_resolution(self) -> None:
        comp = ComponentProfile(id="md", patterns=["src/**"], atomics_usage=UNKNOWN)
        ans = SetupAnswers(
            repository_responsibility="R",
            objectives_selected=["Correctness"],
            objectives_priority=["Correctness"],
            objectives_per_component="yes",
            invariants=["I"],
            performance_importance="no",
            components=[comp],
        )
        ok, _ = apply_unknown_resolution(ans, "component.md.trait.atomics_usage", "n/a")
        self.assertTrue(ok)
        self.assertEqual(comp.atomics_usage, NOT_APPLICABLE)
        self.assertNotEqual(comp.atomics_usage, UNKNOWN)


if __name__ == "__main__":
    unittest.main()
