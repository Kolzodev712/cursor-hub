#!/usr/bin/env python3
"""Integration tests for engineering-doctrine install and hook gate behavior."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from cursor_hub import installer
from cursor_hub.doctrine_enforcement import handle_gate_write, handle_track_read, load_state
from cursor_hub.hooks_merge import merge_hooks_json
from tests.test_doctrine_setup import complete_minimal_setup
from unittest import mock


def _scripted_doctrine_setup(target, io, **kwargs):
    return complete_minimal_setup(target)


class InstallerDoctrineTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.mkdtemp(prefix="cursor-hub-install-")
        self.target = self._tmp

    def tearDown(self) -> None:
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _install(self, *, overwrite: bool = False, twice: bool = False, complete_setup: bool = True) -> None:
        patches = [
            mock.patch("sys.stdin.isatty", return_value=True),
            mock.patch("sys.stdout.isatty", return_value=True),
        ]
        if complete_setup:
            patches.append(
                mock.patch(
                    "cursor_hub.doctrine.install_integration.run_setup",
                    side_effect=_scripted_doctrine_setup,
                )
            )
        for p in patches:
            p.start()
        try:
            rc = installer.run_install(
                _REPO_ROOT,
                self.target,
                ["engineering-doctrine"],
                overwrite=overwrite,
                dry_run=False,
            )
            self.assertEqual(rc, 0 if complete_setup else rc)
        finally:
            for p in reversed(patches):
                p.stop()
        if twice:
            with mock.patch("sys.stdin.isatty", return_value=True), mock.patch(
                "sys.stdout.isatty", return_value=True
            ):
                rc = installer.run_install(
                    _REPO_ROOT,
                    self.target,
                    ["engineering-doctrine"],
                    overwrite=overwrite,
                    dry_run=False,
                )
            self.assertEqual(rc, 0)

    def test_fresh_install_layout(self) -> None:
        self._install()
        cursor = os.path.join(self.target, ".cursor")
        self.assertTrue(os.path.isfile(os.path.join(cursor, "rules", "engineering-doctrine-ambient.mdc")))
        self.assertTrue(os.path.isfile(os.path.join(cursor, "skills", "engineering-doctrine", "SKILL.md")))
        self.assertTrue(os.path.isfile(os.path.join(cursor, "hooks", "doctrine_enforcement.py")))
        hooks = json.load(open(os.path.join(cursor, "hooks.json"), encoding="utf-8"))
        self.assertIn("preToolUse", hooks.get("hooks", {}))
        self.assertTrue(os.path.isfile(os.path.join(cursor, "doctrine", "objectives.md")))
        self.assertTrue(os.path.isfile(os.path.join(cursor, "doctrine", "components.json")))

    def test_existing_doctrine_preserved_on_overwrite(self) -> None:
        doctrine = os.path.join(self.target, ".cursor", "doctrine")
        os.makedirs(doctrine, exist_ok=True)
        custom = os.path.join(doctrine, "objectives.md")
        with open(custom, "w", encoding="utf-8") as f:
            f.write("CUSTOM_OBJECTIVES\n")
        with mock.patch("sys.stdin.isatty", return_value=False), mock.patch(
            "sys.stdout.isatty", return_value=False
        ):
            rc = installer.run_install(
                _REPO_ROOT,
                self.target,
                ["engineering-doctrine"],
                overwrite=True,
                dry_run=False,
            )
        self.assertEqual(rc, 1)
        with open(custom, encoding="utf-8") as f:
            self.assertEqual(f.read(), "CUSTOM_OBJECTIVES\n")

    def test_hooks_merge_idempotent(self) -> None:
        cursor = os.path.join(self.target, ".cursor")
        os.makedirs(cursor, exist_ok=True)
        existing = {
            "version": 1,
            "hooks": {
                "beforeShellExecution": [{"command": ".cursor/hooks/user.sh", "matcher": "curl"}]
            },
        }
        with open(os.path.join(cursor, "hooks.json"), "w", encoding="utf-8") as f:
            json.dump(existing, f)
        self._install(twice=True)
        merged = json.load(open(os.path.join(cursor, "hooks.json"), encoding="utf-8"))
        self.assertEqual(len(merged["hooks"]["beforeShellExecution"]), 1)
        pre = merged["hooks"]["preToolUse"]
        self.assertEqual(len(pre), 1)
        self._install(twice=True)
        merged2 = json.load(open(os.path.join(cursor, "hooks.json"), encoding="utf-8"))
        self.assertEqual(len(merged2["hooks"]["preToolUse"]), 1)

    def test_rust_lang_install_without_doctrine_by_default(self) -> None:
        rc = installer.run_install(
            _REPO_ROOT,
            self.target,
            installer.expand_pack_names(["all"], ["rust"]),
            overwrite=False,
            dry_run=False,
        )
        self.assertEqual(rc, 0)
        self.assertFalse(os.path.isdir(os.path.join(self.target, ".cursor", "doctrine")))
        self.assertTrue(
            os.path.isfile(os.path.join(self.target, ".cursor", "skills", "rust-best-practices", "SKILL.md"))
        )

    def test_context_gate_flow(self) -> None:
        self._install()
        components = {
            "components": [
                {
                    "id": "core",
                    "patterns": ["src/core/**"],
                    "required_project_files": [
                        ".cursor/doctrine/objectives.md",
                        ".cursor/doctrine/invariants.md",
                    ],
                    "required_doctrine_refs": [
                        ".cursor/skills/engineering-doctrine/decision/evidence.md",
                    ],
                }
            ]
        }
        comp_path = os.path.join(self.target, ".cursor", "doctrine", "components.json")
        with open(comp_path, "w", encoding="utf-8") as f:
            json.dump(components, f)
        os.makedirs(os.path.join(self.target, "src", "core"), exist_ok=True)

        session = "sess-1"
        write_payload = {
            "tool_name": "Write",
            "tool_input": {"path": "src/core/hot.rs"},
            "conversation_id": session,
            "workspace_root": self.target,
        }
        deny = handle_gate_write(write_payload, self.target)
        self.assertEqual(deny["permission"], "deny")
        self.assertIn("objectives.md", deny["agent_message"])

        read_payload = {
            "tool_name": "Read",
            "tool_input": {"path": ".cursor/doctrine/objectives.md"},
            "conversation_id": session,
            "workspace_root": self.target,
        }
        handle_track_read(read_payload, self.target)
        still = handle_gate_write(write_payload, self.target)
        self.assertEqual(still["permission"], "deny")

        for path in (
            ".cursor/doctrine/invariants.md",
            ".cursor/skills/engineering-doctrine/decision/evidence.md",
        ):
            handle_track_read(
                {
                    "tool_name": "Read",
                    "tool_input": {"path": path},
                    "conversation_id": session,
                    "workspace_root": self.target,
                },
                self.target,
            )
        allow = handle_gate_write(write_payload, self.target)
        self.assertEqual(allow["permission"], "allow")

    def test_unclassified_write_allowed(self) -> None:
        self._install()
        with open(os.path.join(self.target, ".cursor", "doctrine", "components.json"), "w", encoding="utf-8") as f:
            json.dump(
                {
                    "components": [
                        {
                            "id": "core",
                            "patterns": ["src/core/**"],
                            "required_project_files": [".cursor/doctrine/objectives.md"],
                            "required_doctrine_refs": [],
                        }
                    ]
                },
                f,
            )
        out = handle_gate_write(
            {
                "tool_name": "Write",
                "tool_input": {"path": "README.md"},
                "conversation_id": "s",
                "workspace_root": self.target,
            },
            self.target,
        )
        self.assertEqual(out["permission"], "allow")

    def test_session_isolation_when_conversation_id_differs(self) -> None:
        self._install()
        with open(os.path.join(self.target, ".cursor", "doctrine", "components.json"), "w", encoding="utf-8") as f:
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
        handle_track_read(
            {
                "tool_name": "Read",
                "tool_input": {"path": ".cursor/doctrine/objectives.md"},
                "conversation_id": "session-a",
                "workspace_root": self.target,
            },
            self.target,
        )
        deny = handle_gate_write(
            {
                "tool_name": "Write",
                "tool_input": {"path": "src/x.rs"},
                "conversation_id": "session-b",
                "workspace_root": self.target,
            },
            self.target,
        )
        self.assertEqual(deny["permission"], "deny")

    def test_invalid_components_json_blocks_substantive_writes(self) -> None:
        self._install()
        with open(os.path.join(self.target, ".cursor", "doctrine", "components.json"), "w", encoding="utf-8") as f:
            f.write("{ not json")
        out = handle_gate_write(
            {
                "tool_name": "Write",
                "tool_input": {"path": "src/a.rs"},
                "conversation_id": "s",
                "workspace_root": self.target,
            },
            self.target,
        )
        self.assertEqual(out["permission"], "deny")
        self.assertIn("invalid", out["agent_message"].lower())
        readme = handle_gate_write(
            {
                "tool_name": "Write",
                "tool_input": {"path": "README.md"},
                "conversation_id": "s",
                "workspace_root": self.target,
            },
            self.target,
        )
        self.assertEqual(readme["permission"], "deny")

        with open(os.path.join(self.target, ".cursor", "doctrine", "components.json"), "w", encoding="utf-8") as f:
            json.dump(
                {
                    "components": [
                        {
                            "id": "x",
                            "patterns": ["src/**"],
                            "required_project_files": [".cursor/doctrine/objectives.md"],
                            "required_doctrine_refs": [],
                        }
                    ]
                },
                f,
            )
        out2 = handle_gate_write(
            {
                "tool_name": "Write",
                "tool_input": {"path": "src/a.rs"},
                "conversation_id": "s",
                "workspace_root": self.target,
            },
            self.target,
        )
        self.assertEqual(out2["permission"], "deny")
        self.assertIn("objectives.md", out2["agent_message"])

    def test_context_invalidated_when_doctrine_file_changes(self) -> None:
        self._install()
        session = "sess-hash"
        comp_path = os.path.join(self.target, ".cursor", "doctrine", "components.json")
        with open(comp_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "components": [
                        {
                            "id": "core",
                            "patterns": ["src/**"],
                            "required_project_files": [".cursor/doctrine/invariants.md"],
                            "required_doctrine_refs": [],
                        }
                    ]
                },
                f,
            )
        inv = os.path.join(self.target, ".cursor", "doctrine", "invariants.md")
        handle_track_read(
            {
                "tool_name": "Read",
                "tool_input": {"path": inv},
                "conversation_id": session,
                "workspace_root": self.target,
            },
            self.target,
        )
        write_payload = {
            "tool_name": "Write",
            "tool_input": {"path": "src/x.rs"},
            "conversation_id": session,
            "workspace_root": self.target,
        }
        self.assertEqual(handle_gate_write(write_payload, self.target)["permission"], "allow")
        with open(inv, "a", encoding="utf-8") as f:
            f.write("\n# changed invariant\n")
        denied = handle_gate_write(write_payload, self.target)
        self.assertEqual(denied["permission"], "deny")
        handle_track_read(
            {
                "tool_name": "Read",
                "tool_input": {"path": inv},
                "conversation_id": session,
                "workspace_root": self.target,
            },
            self.target,
        )
        self.assertEqual(handle_gate_write(write_payload, self.target)["permission"], "allow")

    def test_explicit_session_does_not_leak_into_missing_conversation_id(self) -> None:
        self._install()
        with open(os.path.join(self.target, ".cursor", "doctrine", "components.json"), "w", encoding="utf-8") as f:
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
        handle_track_read(
            {
                "tool_name": "Read",
                "tool_input": {"path": ".cursor/doctrine/objectives.md"},
                "conversation_id": "chat-a",
                "workspace_root": self.target,
            },
            self.target,
        )
        deny = handle_gate_write(
            {
                "tool_name": "Write",
                "tool_input": {"path": "src/x.rs"},
                "workspace_root": self.target,
            },
            self.target,
        )
        self.assertEqual(deny["permission"], "deny")


class HooksMergeUnitTests(unittest.TestCase):
    def test_dedupe(self) -> None:
        frag = {"hooks": {"preToolUse": [{"command": "a", "matcher": "Write"}]}}
        merged = merge_hooks_json(frag, frag)
        self.assertEqual(len(merged["hooks"]["preToolUse"]), 1)


if __name__ == "__main__":
    unittest.main()
