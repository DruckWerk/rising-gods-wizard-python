"""client.py — Orchestrierung der Client-Beschaffung.

Reihenfolge (Spec §11.7): lokal (falls vorhanden) -> Torrent (Port 9092)
-> HTTP-Fallback. Bricht bei Offline/Torrent-Fehler nicht still, sondern
gibt den gewählten Quell-Typ in ctx.client_source zurück.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .. import config
from .direct import download_http
from .torrent import start_torrent


def fetch_client(ctx: Any, actions: Any, ui: Any = None) -> str:
    """Beschafft den WoW-Client. Liefert den Quell-Typ zurück.

    Reihenfolge: lokal -> torrent -> http. Im Dry-Run werden alle Schritte
    nur protokolliert, aber die Reihenfolge-Logik bleibt erhalten.
    """
    # 1) lokal
    if ctx.local_client_path and Path(ctx.local_client_path).exists():
        ctx.client_source = "local"
        if ui:
            ui.note(f"Lokaler Client gefunden: {ctx.local_client_path}")
        return str(ctx.client_source)

    # 2) Torrent
    torrent_url = getattr(ctx, "torrent_url", "") or ""
    if torrent_url:
        try:
            start_torrent(torrent_url, ctx.wow_dir, actions)
            ctx.client_source = "torrent"
            if ui:
                ui.note("Torrent-Download gestartet (Port "
                        f"{config.TORRENT_RPC_PORT}).")
            return str(ctx.client_source)
        except RuntimeError as exc:
            if ui:
                ui.warn(f"Torrent fehlgeschlagen, HTTP-Fallback: {exc}")

    # 3) HTTP-Fallback (erfordert eine URL in ctx)
    http_url = getattr(ctx, "http_url", "") or ""
    if not http_url:
        raise RuntimeError(
            "Keine Client-Quelle verfügbar: weder lokal, noch Torrent-URL, "
            "noch HTTP-URL gesetzt (Offline?)."
        )
    download_http(http_url, ctx.wow_dir / "wow_client", actions)
    ctx.client_source = "http"
    if ui:
        ui.note("HTTP-Download abgeschlossen.")
    return str(ctx.client_source)
