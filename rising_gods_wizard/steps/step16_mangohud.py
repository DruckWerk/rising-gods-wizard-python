"""step16_mangohud.py — MangoHud optional."""
from __future__ import annotations

import logging
from typing import Any

from ..game import mangohud

log = logging.getLogger(__name__)


def run(ctx: Any, ui: Any, actions: Any) -> None:
    log.info("Step 16: MangoHud")
    path = mangohud.write_mangohud(ctx, actions)
    log.info("MangoHud: %s", path if path else "deaktiviert")
