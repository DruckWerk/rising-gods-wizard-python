"""game/ — WoW-spezifische Module (Config.wtf, FPS-Boost, Shader-Cache,
MangoHud, Lutris-Export, Realmlist-Verifikation / Feature 5).

Alle Module sind Dependency-Inversion-konform: reine Generierungsfunktionen
sind testbar ohne Side-Effects; Schreib-Aktionen laufen über injizierte
`actions` (FSAction), die --dry-run respektieren.
"""
from __future__ import annotations

from . import config_wtf, fps_boost, lutris_export, mangohud, realmlist, shader_cache

__all__ = [
    "config_wtf",
    "fps_boost",
    "lutris_export",
    "mangohud",
    "realmlist",
    "shader_cache",
]
