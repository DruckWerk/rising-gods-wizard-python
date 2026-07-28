"""step10_dxvk_audio.py — DXVK-Config + Audio-Fix (winealsa/PipeWire)."""
from __future__ import annotations

import logging
from typing import Any

from ..dxvk import config as dxvk_config
from ..wine import audio

log = logging.getLogger(__name__)


def run(ctx: Any, ui: Any, actions: Any) -> None:
    log.info("Step 10: DXVK-Config + Audio-Fix")
    dxvk_config.write_dxvk_conf(ctx, actions)
    env = audio.compute_audio_env(ctx)
    driver = env.get("WINEDRIVER", "alsa")
    actions.shell.run(f'export WINEDRIVER={driver}')
    log.info("Audio-Env: %s", env)
