"""fps_boost.py — 7 FPS-Optionen, per-Class HW-Vorauswahl (WEAK..ULTRA).

Reine Logik (testbar ohne Side-Effects). Presets folgen dem bash-Original
(Zeilen 2525-2555), gemappt auf die 7 Optionen in Reihenfolge:
  Sound_EnableMusic, Sound_EnableAmbience, Sound_EnableReverb,
  ffxGlow, ffxDeath, ffxSpecial, maxFPSBk
"""
from __future__ import annotations

# Reihenfolge = bash FPS_ITEMS (Zeile 2560-2566)
FPS_OPTIONS: tuple[str, ...] = (
    "Sound_EnableMusic",
    "Sound_EnableAmbience",
    "Sound_EnableReverb",
    "ffxGlow",
    "ffxDeath",
    "ffxSpecial",
    "maxFPSBk",
)

# Preset pro Perf-Class (True=vorausgewählt ON). Index = FPS_OPTIONS-Index.
# weak=alle, old=Sound+Glow+Death+maxFPSBk, mid=Glow+maxFPSBk,
# high=maxFPSBk, low=alle (bash kennt kein low -> wie weak), ultra=keine.
_PRESETS: dict[str, tuple[bool, ...]] = {
    "weak": (True, True, True, True, True, True, True),
    "old": (True, True, True, True, True, False, True),
    "low": (True, True, True, True, True, True, True),
    "mid": (False, False, False, True, False, False, True),
    "high": (False, False, False, False, False, False, True),
    "ultra": (False, False, False, False, False, False, False),
}


def preset_for(perf_class: str) -> tuple[bool, ...]:
    """Liefert das Vorauswahl-Preset für eine Perf-Class (Default: high)."""
    if perf_class not in _PRESETS:
        perf_class = "high"
    return _PRESETS[perf_class]


def selected_options(perf_class: str) -> list[str]:
    """Liefert die vorausgewählten FPS-Optionen für eine Perf-Class."""
    return [opt for opt, on in zip(FPS_OPTIONS, preset_for(perf_class), strict=False) if on]


def build_fps_config(selected: list[str]) -> str:
    """PURE: erzeugt die SET-Zeilen für die gewählten Optionen."""
    lines = []
    for opt in selected:
        if opt == "maxFPSBk":
            lines.append('SET maxFPSBk "30"')
        else:
            lines.append(f'SET {opt} "0"')
    return "\n".join(lines) + "\n" if lines else ""
