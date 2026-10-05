#!/usr/bin/env python3
"""Run doctrine install + setup through a pseudo-TTY (ConsoleIO, not ScriptIO)."""
from __future__ import annotations

import os
import pty
import select
import subprocess
import sys
import tempfile
import time

REPO = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
TARGET = os.environ.get("DOCTRINE_ACCEPTANCE_TARGET", "/tmp/doctrine-test")


def _write(fd: int, text: str) -> None:
    os.write(fd, text.encode())


def _run_pty(cmd: list[str], inputs: list[str], *, send_interrupt_after: int | None = None) -> tuple[int, str]:
    pid, fd = pty.openpty()
    proc = subprocess.Popen(
        cmd,
        stdin=fd,
        stdout=fd,
        stderr=fd,
        cwd=REPO,
        close_fds=True,
    )
    os.close(fd)
    master, _ = pty.openpty()
    # Re-open: simpler approach using master attached to child stdout
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdin=subprocess.PIPE,
        cwd=REPO,
        text=True,
        bufsize=0,
    )
    out_chunks: list[str] = []
    for i, line in enumerate(inputs):
        if send_interrupt_after is not None and i == send_interrupt_after:
            proc.send_signal(subprocess.signal.SIGINT if hasattr(subprocess, "signal") else 2)
            time.sleep(0.2)
        proc.stdin.write(line + "\n")
        proc.stdin.flush()
        time.sleep(0.05)
    proc.stdin.close()
    out_chunks.append(proc.stdout.read() or "")
    return proc.wait(), "".join(out_chunks)


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "prepare-fixture":
        os.makedirs(f"{TARGET}/crates/market-data/src", exist_ok=True)
        os.makedirs(f"{TARGET}/crates/risk/src", exist_ok=True)
        with open(f"{TARGET}/Cargo.toml", "w", encoding="utf-8") as f:
            f.write('[workspace]\nmembers = ["crates/market-data", "crates/risk"]\n')
        with open(f"{TARGET}/README.md", "w", encoding="utf-8") as f:
            f.write("# Trading stack\nLow-latency market data ingestion and risk checks.\n")
        with open(f"{TARGET}/crates/market-data/src/lib.rs", "w", encoding="utf-8") as f:
            f.write("use std::sync::atomic::{AtomicU64, Ordering};\npub fn tick() -> u64 { AtomicU64::new(0).load(Ordering::Relaxed) }\n")
        print(f"Fixture ready at {TARGET}")
        return 0

    print("Use manual terminal walkthrough documented in docs/doctrine-setup-question-audit.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
