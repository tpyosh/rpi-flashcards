from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SpiDisplayConfig:
    module_name: str = "unknown-2in13"
    width: int = 250
    height: int = 122
    rotation: int = 0


def build_bootstrap_notes(config: SpiDisplayConfig) -> list[str]:
    return [
        "Confirm the exact panel driver before enabling GPIO access.",
        f"Expected frame size: {config.width}x{config.height}.",
        "Keep terminal mode as the fallback during panel bring-up.",
    ]
