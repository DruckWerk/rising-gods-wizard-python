"""addons — Community-Tools Live-Fetch (Feature 4) + reguläre Addons.

Exportiert community_fetch.fetch_community_tools und addonhelper.install_addons.
Für die statischen Bundles siehe config.BUNDLES_DIR (pv/unrar).
"""
from __future__ import annotations

from .addonhelper import install_addons
from .community_fetch import fetch_community_tools

__all__ = ["fetch_community_tools", "install_addons"]
