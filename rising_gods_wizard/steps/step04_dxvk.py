"""step04_dxvk.py — DXVK + Vulkan-Install, GPU-Config, Shader-Caches."""
from __future__ import annotations

import logging
from typing import Any

from ..dxvk import config as dxvk_config
from ..dxvk import install as dxvk_install

log = logging.getLogger(__name__)


def run(ctx: Any, ui: Any, actions: Any) -> None:
    log.info("Step 04: DXVK/Vulkan installieren")
    dxvk_install.install_dxvk(ctx, actions)
    dxvk_config.write_dxvk_conf(ctx, actions)
    log.info("DXVK installiert + dxvk.conf geschrieben")
