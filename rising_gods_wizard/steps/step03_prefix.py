"""step03_prefix.py — Wine-Prefix + Verzeichnis-Setup."""
from __future__ import annotations

import logging
from typing import Any

from ..wine import prefix

log = logging.getLogger(__name__)


def run(ctx: Any, ui: Any, actions: Any) -> None:
    log.info("Step 03: Wine-Prefix anlegen")
    prefix.create_prefix(ctx, actions)
    log.info("Prefix bereit: %s", ctx.prefix)
