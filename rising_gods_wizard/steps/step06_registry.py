"""step06_registry.py — Registry-Tweaks (CSMT, Offscreen, StrictDraw, MSAA)."""
from __future__ import annotations

import logging
from typing import Any

from ..wine import registry

log = logging.getLogger(__name__)


def run(ctx: Any, ui: Any, actions: Any) -> None:
    log.info("Step 06: Wine-Registry-Tweaks")
    registry.write_registry(ctx, actions)
    log.info("Registry-Tweaks geschrieben")
