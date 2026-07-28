"""audio.py — Wine-Audio-Konfiguration (PURE Gen, <60 Zeilen).

Bestimmt den WINEDRIVER (alsa/pulse) und liefert das Env-Dict, das der
Launcher exportiert. Reine Datentransformation, keine Side-Effects.
"""
from __future__ import annotations

from ..context import WizardContext


def choose_driver(session_type: str, prefer_pulse: bool = False) -> str:
    """Wählt den Wine-Audio-Treiber.

    wayland → pulse (PipeWire/pulse); ansonsten alsa, sofern nicht
    explizit pulse bevorzugt wird.
    """
    if session_type == "wayland" or prefer_pulse:
        return "pulse"
    return "alsa"


def compute_audio_env(ctx: WizardContext) -> dict[str, str]:
    """PURE: liefert WINEDRIVER-Env für den Launcher."""
    driver = choose_driver(ctx.hw.session_type)
    return {"WINEDRIVER": driver}
