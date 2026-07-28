"""step09_shader_cache.py — Shader-Cache-Verzeichnisse anlegen."""
from __future__ import annotations

import logging
from typing import Any

from ..game import shader_cache

log = logging.getLogger(__name__)


def run(ctx: Any, ui: Any, actions: Any) -> None:
    log.info("Step 09: Shader-Cache-Verzeichnisse")
    created = shader_cache.ensure_shader_cache_dirs(ctx, actions)
    log.info("Shader-Caches: %s", created)
