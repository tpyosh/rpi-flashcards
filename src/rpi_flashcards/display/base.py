from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class PreparedCardFrame:
    width: int
    height: int
    title: str
    subtitle: str
    body_lines: tuple[str, ...]
    footer: str


class DisplayAdapter(Protocol):
    def show(self, frame: PreparedCardFrame) -> None:
        """Render one prepared frame on a concrete target."""

