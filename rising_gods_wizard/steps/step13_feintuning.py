"""step13_feintuning.py — Feintuning (Config.wtf Patch + Desktop-Entry)."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from ..game import config_wtf

log = logging.getLogger(__name__)


def run(ctx: Any, ui: Any, actions: Any) -> None:
    log.info("Step 13: Feintuning (Config.wtf Patch)")
    config_wtf.write_config_wtf(ctx, actions)
    desktop = (
        Path.home() / ".local" / "share" / "applications" / "rising-gods.desktop"
    )
    actions.fs.write(
        desktop,
        f"[Desktop Entry]\nName=Rising Gods WoW\nExec={ctx.launcher_path}\n"
        "Type=Application\n",
    )
    log.info("Feintuning abgeschlossen")
