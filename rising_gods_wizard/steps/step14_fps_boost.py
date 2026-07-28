"""step14_fps_boost.py — FPS-Boost (7 Optionen, per-Class HW-Vorauswahl)."""
from __future__ import annotations

import logging
from typing import Any

from ..game import fps_boost

log = logging.getLogger(__name__)


def run(ctx: Any, ui: Any, actions: Any) -> None:
    log.info("Step 14: FPS-Boost")
    selected = ctx.fps_boost_selected or fps_boost.selected_options(ctx.hw.perf_class)
    content = fps_boost.build_fps_config(selected)
    actions.fs.write(ctx.config_wtf_path, content)
    log.info("FPS-Boost (%d Optionen) geschrieben", len(selected))
