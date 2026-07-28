"""step12_config_gamemode.py — Config.wtf + GameMode-Settings (38 Einträge)."""
from __future__ import annotations

import logging
from typing import Any

from ..game import config_wtf

log = logging.getLogger(__name__)


def run(ctx: Any, ui: Any, actions: Any) -> None:
    log.info("Step 12: Config.wtf + GameMode")
    config_wtf.write_config_wtf(ctx, actions)
    if ctx.use_gamemode:
        actions.fs.write(
            __import__("pathlib").Path.home() / ".config" / "gamemode.ini",
            "[general]\nwineserver-realtime=1\n",
        )
    log.info("Config.wtf geschrieben")
