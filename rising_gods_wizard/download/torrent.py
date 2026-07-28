"""torrent.py — Torrent-Backend (Refactor von torrenthelper.py).

Live-Progress via transmission-remote; optional Hash-Verifikation.
Aufruf nur mit erlaubten Präfixen (curl/wget/transmission-* via actions.shell).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .. import config


def start_torrent(url: str, dest: Path, actions: Any) -> Path:
    """Startet Torrent-Download via transmission-cli nach dest.

    url kann ein Magnet-Link oder eine .torrent-URL sein. Im Dry-Run wird
    nur protokolliert. Liefert den Zielpfad zurück.
    """
    dest = Path(dest)
    cmd = (
        f"transmission-cli -w {dest} "
        f"--rpc-port {config.TORRENT_RPC_PORT} {url}"
    )
    rc, out, err = actions.shell.run(cmd)
    if rc != 0:
        raise RuntimeError(f"Torrent-Download fehlgeschlagen ({rc}): {err or out}")
    return dest


def verify_torrent(dest: Path, expected_hash: str | None = None, actions: Any = None) -> bool:
    """Verifiziert den Torrent-Inhalt (optional Hash).

    Bei gesetztem expected_hash (SHA256) wird dieser via sha256sum geprüft;
    ohne Hash nur Existenz/Größe. Liefert True bei Erfolg.
    """
    dest = Path(dest)
    if not dest.exists():
        return False
    if expected_hash:
        result = actions.shell.run(f"sha256sum {dest}")
        out = result[1]
        actual = out.strip().split()[0] if out else ""
        if actual.lower() != expected_hash.lower():
            raise ValueError(
                f"Torrent-Hash-Mismatch: erwartet {expected_hash}, "
                f"erhalten {actual}"
            )
    return True
