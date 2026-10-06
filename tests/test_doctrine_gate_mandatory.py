#!/usr/bin/env python3
"""Mandatory context acquisition for doctrine write gate."""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import unittest

_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from cursor_hub.doctrine_enforcement import (
    extract_write_paths,
    handle_gate_write,
    handle_pre_compact,
    handle_track_read,
    load_state,
)


def _full_read_payload(target: str, rel_path: str, session: str) -> dict:
    abs_path = os.path.join(target, rel_path.replace("/", os.sep))
    with open(abs_path, encoding="utf-8") as f:
        content = f.read()
    return {
        "tool_name": "Read",
        "tool_input": {"path": rel_path},
        "tool_output": {"content": content},
        "conversation_id": session,
        "workspace_root": target,
    }


def _path_only_read(rel_path: str, session: str, target: str) -> dict:
    return {
        "tool_name": "Read",
        "tool_input": {"path": rel_path},
        "conversation_id": session,
        "workspace_root": target,
    }


class MandatoryContextTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp()
        doctrine = os.path.join(self.tmp, ".cursor", "doctrine")
        os.makedirs(doctrine, exist_ok=True)
        with open(os.path.join(doctrine, "objectives.md"), "w", encoding="utf-8") as f:
            f.write("# Engineering objectives\n\n## Selected properties\n\n- Correctness\n")
        with open(os.path.join(doctrine, "components.json"), "w", encoding="utf-8") as f:
            json.dump(
                {
                    "components": [
                        {
                            "id": "core",
                            "patterns": ["src/**"],
                            "required_project_files": [".cursor/doctrine/objectives.md"],
                            "required_doctrine_refs": [],
                        }
                    ]
                },
                f,
            )
        os.makedirs(os.path.join(self.tmp, "src"), exist_ok=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _write(self, session: str) -> dict:
        return handle_gate_write(
            {
                "tool_name": "Write",
                "tool_input": {"path": "src/x.rs"},
                "conversation_id": session,
                "workspace_root": self.tmp,
            },
            self.tmp,
        )

    def test_path_only_read_does_not_unlock(self) -> None:
        big_rel = ".cursor/doctrine/large.md"
        big_path = os.path.join(self.tmp, big_rel.replace("/", os.sep))
        with open(big_path, "w", encoding="utf-8") as f:
            f.write("x" * 600_000)
        with open(os.path.join(self.tmp, ".cursor", "doctrine", "components.json"), "w", encoding="utf-8") as f:
            json.dump(
                {
                    "components": [
                        {
                            "id": "core",
                            "patterns": ["src/**"],
                            "required_project_files": [big_rel],
                            "required_doctrine_refs": [],
                        }
                    ]
                },
                f,
            )
        session = "s-path"
        handle_track_read(_path_only_read(big_rel, session, self.tmp), self.tmp)
        self.assertEqual(self._write(session)["permission"], "deny")

    def test_partial_content_does_not_unlock(self) -> None:
        session = "s-partial"
        handle_track_read(
            {
                "tool_name": "Read",
                "tool_input": {"path": ".cursor/doctrine/objectives.md"},
                "tool_output": {"content": "partial snippet only"},
                "conversation_id": session,
                "workspace_root": self.tmp,
            },
            self.tmp,
        )
        self.assertEqual(self._write(session)["permission"], "deny")

    def test_full_content_unlocks(self) -> None:
        session = "s-full"
        handle_track_read(
            _full_read_payload(self.tmp, ".cursor/doctrine/objectives.md", session),
            self.tmp,
        )
        self.assertEqual(self._write(session)["permission"], "allow")

    def test_changed_file_relocks(self) -> None:
        session = "s-change"
        handle_track_read(
            _full_read_payload(self.tmp, ".cursor/doctrine/objectives.md", session),
            self.tmp,
        )
        self.assertEqual(self._write(session)["permission"], "allow")
        with open(os.path.join(self.tmp, ".cursor", "doctrine", "objectives.md"), "a", encoding="utf-8") as f:
            f.write("\n# edited\n")
        self.assertEqual(self._write(session)["permission"], "deny")

    def test_session_isolation(self) -> None:
        handle_track_read(
            _full_read_payload(self.tmp, ".cursor/doctrine/objectives.md", "a"),
            self.tmp,
        )
        self.assertEqual(self._write("b")["permission"], "deny")

    def test_pre_compact_clears_reads(self) -> None:
        session = "s-compact"
        handle_track_read(
            _full_read_payload(self.tmp, ".cursor/doctrine/objectives.md", session),
            self.tmp,
        )
        self.assertEqual(self._write(session)["permission"], "allow")
        handle_pre_compact({"conversation_id": session, "workspace_root": self.tmp}, self.tmp)
        self.assertEqual(self._write(session)["permission"], "deny")
        state = load_state(self.tmp)
        self.assertEqual(state["sessions"][session]["reads"], {})

    def test_apply_patch_multi_path(self) -> None:
        patch = "*** Update File: src/a.rs\n*** Update File: src/b.rs\n"
        paths, err = extract_write_paths("ApplyPatch", {"patch": patch})
        self.assertIsNone(err)
        self.assertEqual(paths, ["src/a.rs", "src/b.rs"])

    def test_unrecognized_apply_patch_denies(self) -> None:
        out = handle_gate_write(
            {
                "tool_name": "ApplyPatch",
                "tool_input": {"note": "no paths here"},
                "conversation_id": "x",
                "workspace_root": self.tmp,
            },
            self.tmp,
        )
        self.assertEqual(out["permission"], "deny")


if __name__ == "__main__":
    unittest.main()
