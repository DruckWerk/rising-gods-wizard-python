"""doctor/ — Wartungs-Modus (audit/repair/tune/hd/uninstall).

Wiederverwendung der Fach-Module (realmlist, community_fetch, config_wtf,
shader_cache). Side-Effects nur über das Actions-Interface bzw. shutil.
"""
from __future__ import annotations

__all__ = ["audit", "hd", "repair", "tune", "uninstall"]
