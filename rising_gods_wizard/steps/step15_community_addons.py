"""step15_community_addons.py — Community-Tools Live-Fetch (Feature 4) + Addons.

Community-Tools werden IMMER live gefetcht (fetch_community_tools).
Reguläre Addons nur bei ctx.addons_enabled (opt-in).
"""
from __future__ import annotations

import logging
from typing import Any

from ..addons import addonhelper, community_fetch

log = logging.getLogger(__name__)


def run(ctx: Any, ui: Any, actions: Any) -> None:
    log.info("Step 15: Community-Tools + Addons")
    community_fetch.fetch_community_tools(ctx, ui, actions)
    addonhelper.install_addons(ctx, ui, actions)
    log.info("Step 15 abgeschlossen")
