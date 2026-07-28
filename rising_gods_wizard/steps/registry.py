"""registry.py — STEP_REGISTRY: geordnete Step-IDs + Metadaten + Dispatch.

Jeder Step liefert eine Funktion run(ctx, ui, actions). run_step(n, ...)
dispatcht auf die entsprechende Funktion; ungültige IDs -> ValueError.
"""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from . import step01_preflight as s01
from . import step02_system as s02
from . import step03_prefix as s03
from . import step04_dxvk as s04
from . import step05_download as s05
from . import step06_registry as s06
from . import step07_gpu as s07
from . import step08_system_tweaks as s08
from . import step09_shader_cache as s09
from . import step10_dxvk_audio as s10
from . import step11_launcher as s11
from . import step12_config_gamemode as s12
from . import step13_feintuning as s13
from . import step14_fps_boost as s14
from . import step15_community_addons as s15
from . import step16_mangohud as s16
from . import step17_finish as s17

STEP_REGISTRY: dict[int, Callable[..., None]] = {
    1: s01.run,
    2: s02.run,
    3: s03.run,
    4: s04.run,
    5: s05.run,
    6: s06.run,
    7: s07.run,
    8: s08.run,
    9: s09.run,
    10: s10.run,
    11: s11.run,
    12: s12.run,
    13: s13.run,
    14: s14.run,
    15: s15.run,
    16: s16.run,
    17: s17.run,
}

STEP_TITLES: dict[int, str] = {
    1: "Pre-Flight & Hardware",
    2: "System & Pakete",
    3: "Wine-Prefix",
    4: "DXVK/Vulkan",
    5: "Client + Realmlist",
    6: "Registry-Tweaks",
    7: "GPU-Detection",
    8: "System-Tweaks (ntsync)",
    9: "Shader-Caches",
    10: "DXVK + Audio",
    11: "Launcher-Script",
    12: "Config.wtf + GameMode",
    13: "Feintuning",
    14: "FPS-Boost",
    15: "Community-Tools + Addons",
    16: "MangoHud",
    17: "Abschluss + State",
}


def run_step(n: int, ctx: Any, ui: Any, actions: Any) -> None:
    """Dispatcht Step n. Ungültige IDs -> ValueError."""
    fn = STEP_REGISTRY.get(n)
    if fn is None:
        raise ValueError(f"Unbekannte Step-ID: {n} (gültig 1..17)")
    fn(ctx, ui, actions)
