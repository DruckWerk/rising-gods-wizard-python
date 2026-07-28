"""download — WoW-Client-Beschaffung: lokal -> Torrent -> HTTP-Fallback.

Exportiert die Orchestrierung (client.fetch_client) sowie die beiden
Beschaffungs-Backends (torrent/start_torrent, direct/download_http).
Alle Funktionen respektieren ctx.dry_run via actions.shell.
"""
from __future__ import annotations

from .client import fetch_client
from .direct import download_http
from .torrent import start_torrent, verify_torrent

__all__ = ["download_http", "fetch_client", "start_torrent", "verify_torrent"]
