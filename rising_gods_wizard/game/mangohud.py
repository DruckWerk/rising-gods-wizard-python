"""mangohud.py — optionale MangoHud-Config schreiben.

Klein (< 60 Z): schreibt ~/.config/MangoHud/wow335.conf mit FPS-Overlay.
Nur wenn ctx.mangohud_enabled.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ..context import WizardContext


def build_mangohud_conf() -> str:
    """PURE: minimalistische MangoHud-Config (FPS + frametime)."""
    return "fps=1\nframetime=1\nno_display=0\n"


def write_mangohud(ctx: WizardContext, actions: Any) -> Path | None:
    """Schreibt MangoHud-Config, falls aktiviert. Liefert Pfad oder None."""
    if not ctx.mangohud_enabled:
        return None
    target = Path.home() / ".config" / "MangoHud" / "wow335.conf"
    actions.fs.write(target, build_mangohud_conf())
    return target
