"""steps/ — 17 Step-Module + Registry (V1 Build, Chunk 7).

Jeder Step ist reine Orchestrierung: er ruft die Fach-Module
(hardware/*, wine/*, dxvk/*, game/*, download/*, addons/*, state)
auf. Logik liegt in den Fach-Modulen (PURE Gen + Actions).
"""
from __future__ import annotations

from .registry import STEP_REGISTRY, STEP_TITLES, run_step

__all__ = ["STEP_REGISTRY", "STEP_TITLES", "run_step"]
