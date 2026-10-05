"""Interactive IO abstraction for doctrine setup wizard."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


class SetupIO(Protocol):
    def writeln(self, text: str = "") -> None: ...
    def readline(self, prompt: str = "") -> str: ...


@dataclass
class ConsoleIO:
    def writeln(self, text: str = "") -> None:
        print(text)

    def readline(self, prompt: str = "") -> str:
        try:
            return input(prompt)
        except EOFError:
            return ""


@dataclass
class ScriptIO:
    """Deterministic inputs for tests (FIFO queue)."""

    inputs: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    _idx: int = 0

    def writeln(self, text: str = "") -> None:
        self.outputs.append(text)

    def readline(self, prompt: str = "") -> str:
        if self._idx >= len(self.inputs):
            return ""
        val = self.inputs[self._idx]
        self._idx += 1
        self.outputs.append(f"{prompt}{val}")
        return val
