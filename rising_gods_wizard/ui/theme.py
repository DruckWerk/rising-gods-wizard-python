"""theme.py — Theming für AssetRenderer (V2a, siehe architect-spec-v2 §2)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    name: str
    primary: str  # rich-Style-Token, z.B. "bright_cyan"
    accent: str
    banner_style: str  # z.B. "bold bright_white"
    box_style: str  # z.B. "cyan"
    gradient: tuple[str, str]  # (start, end) für Gradient-Overlay


THEMES: dict[str, Theme] = {
    "ice": Theme(
        "ice",
        "bright_cyan",
        "bright_blue",
        "bold bright_white",
        "cyan",
        ("bright_cyan", "bright_blue"),
    ),
    "classic": Theme(
        "classic",
        "bright_yellow",
        "bright_red",
        "bold white",
        "yellow",
        ("yellow", "red"),
    ),
    "mono": Theme(
        "mono",
        "white",
        "white",
        "bold white",
        "white",
        ("white", "white"),
    ),
}


def get_theme(name: str) -> Theme:
    return THEMES.get(name, THEMES["ice"])
