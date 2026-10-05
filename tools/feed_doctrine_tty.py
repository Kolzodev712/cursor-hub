#!/usr/bin/env python3
"""Feed answers to doctrine setup via PTY when prompts appear (ConsoleIO path)."""
from __future__ import annotations

import os
import pty
import select
import subprocess
import sys
import termios
import tty

REPO = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))


def run(cmd: list[str], answers: list[str], *, interrupt_after: int | None = None) -> int:
    master, slave = pty.openpty()
    proc = subprocess.Popen(
        cmd,
        stdin=slave,
        stdout=slave,
        stderr=slave,
        cwd=REPO,
        close_fds=True,
    )
    os.close(slave)
    old = termios.tcgetattr(master)
    try:
        tty.setraw(master)
        buf = b""
        ans_idx = 0
        while proc.poll() is None:
            r, _, _ = select.select([master], [], [], 0.05)
            if r:
                chunk = os.read(master, 4096)
                if not chunk:
                    break
                sys.stdout.buffer.write(chunk)
                sys.stdout.buffer.flush()
                buf += chunk
                if buf.endswith(b"> ") or buf.endswith(b"Objective:\n") or buf.endswith(b"Responsibility:\n"):
                    if interrupt_after is not None and ans_idx >= interrupt_after:
                        os.write(master, b"\x03")
                        interrupt_after = None
                        continue
                    if ans_idx < len(answers):
                        line = answers[ans_idx] + "\n"
                        ans_idx += 1
                        os.write(master, line.encode())
                        buf = b""
        while proc.poll() is None:
            proc.wait(timeout=0.1)
    finally:
        termios.tcsetattr(master, termios.TCSADRAIN, old)
        os.close(master)
    return proc.wait()


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "/tmp/doctrine-test"
    answers = sys.argv[2:] if len(sys.argv) > 2 else []
    cmd = [sys.executable, "-m", "cursor_hub", "doctrine", "setup", target]
    raise SystemExit(run(cmd, answers))
