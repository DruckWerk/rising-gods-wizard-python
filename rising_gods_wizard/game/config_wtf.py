"""config_wtf.py — WTF/Config.wtf (Stabilitäts-Einträge) generieren + schreiben.

Parity zum bash-Original (Commit 58856cc, Zeilen ~2402-2443): 40 SET-Einträge.
gxTextureCacheSize ist dynamisch (ultra/high -> 1024, sonst 256), analog bash.
"""
from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from ..context import WizardContext

# (key, value) — value=None => dynamisch (gxTextureCacheSize)
_CONFIG_ENTRIES: tuple[tuple[str, str | None], ...] = (
    ("gxApi", "d3d9"),
    ("gxWindow", "1"),
    ("gxMaximize", "1"),
    ("gxRefresh", "60"),
    ("gxCursor", "0"),
    ("gxTextureCacheSize", None),
    ("gxMultisample", "0"),
    ("gxTripleBuffer", "0"),
    ("gxFixLag", "1"),
    ("farclip", "800"),
    ("shadowLevel", "0"),
    ("weatherDensity", "0"),
    ("groundEffectDensity", "0"),
    ("groundEffectDist", "0"),
    ("M2UseThreads", "1"),
    ("maxAnimThreads", "3"),
    ("terrainMipLevel", "0"),
    ("environmentDetail", "0.5"),
    ("componentTextureLevel", "0"),
    ("textureFilteringMode", "0"),
    ("rippleDetail", "0"),
    ("projectedTextures", "0"),
    ("reflectionMode", "0"),
    ("M2BatchDoodads", "1"),
    ("M2BatchParticles", "1"),
    ("worldPreloadNonCriticalNodes", "0"),
    ("readTinyRaidData", "0"),
    ("readTinyPetData", "0"),
    ("readTinyGuildData", "0"),
    ("checkAddonVersion", "0"),
    ("synchronizeSettings", "0"),
    ("synchronizeConfig", "0"),
    ("synchronizeBindings", "0"),
    ("synchronizeMacros", "0"),
    ("SoundOutputSystem", "1"),
    ("SoundBufferSize", "150"),
    ("Sound_OutputQuality", "0"),
    ("Sound_NumChannels", "24"),
    ("maxFPS", "0"),
    ("processAffinityMask", "0"),
)


def build_config_wtf(cache_size: int = 256) -> str:
    """PURE: erzeugt den vollständigen Config.wtf-Inhalt (40 Einträge)."""
    lines = [
        f'SET {key} "{cache_size if value is None else value}"'
        for key, value in _CONFIG_ENTRIES
    ]
    return "\n".join(lines) + "\n"


def write_config_wtf(ctx: WizardContext, actions: Any, cache_size: int | None = None) -> Path:
    """Schreibt Config.wtf (mit Backup des Originals, falls vorhanden)."""
    if cache_size is None:
        cache_size = 1024 if ctx.hw.perf_class in ("ultra", "high") else 256
    content = build_config_wtf(cache_size)
    target = ctx.config_wtf_path
    if not ctx.dry_run and target.exists():
        shutil.copy2(target, target.with_suffix(".wtf.backup"))
    actions.fs.write(target, content)
    return target
