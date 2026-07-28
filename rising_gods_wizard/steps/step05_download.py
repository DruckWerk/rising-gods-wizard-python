"""step05_download.py — WoW-Client + Feature 5 Realmlist-Check.

Client-Beschaffung via download.client; bei ctx.existing_install wird
game.realmlist.verify_realmlist ausgeführt (Feature 5-Verzweigung).
"""
from __future__ import annotations

import logging
from typing import Any

from ..download import client
from ..game import realmlist

log = logging.getLogger(__name__)


def run(ctx: Any, ui: Any, actions: Any) -> None:
    log.info("Step 05: WoW-Client beschaffen")
    client.fetch_client(ctx, actions, ui)
    if ctx.existing_install:
        realmlist.verify_realmlist(ctx, ui, actions)
    else:
        log.info("Step 05: frischer Client — kein Realmlist-Check")
