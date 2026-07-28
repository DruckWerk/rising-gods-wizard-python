"""direct.py — HTTP-Direct-Download mit Progress + Verify.

Refactor von torrenthelper-Fallback. Nutzt curl (mit -L, -o, -#-Progress).
Im Dry-Run nur Plan; kein echtes Netz.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


def download_http(url: str, dest: Path, actions: Any) -> Path:
    """Lädt url via curl nach dest herunter (HTTP-Fallback).

    Liefert dest zurück. Fehler bei rc != 0 (inkl. Offline -> curl rc != 0).
    """
    dest = Path(dest)
    cmd = f"curl -fL -o {dest} --retry 2 {url}"
    rc, out, err = actions.shell.run(cmd)
    if rc != 0:
        raise RuntimeError(f"HTTP-Download fehlgeschlagen ({rc}): {err or out}")
    return dest


def verify_file(path: Path, expected_sha256: str | None = None) -> bool:
    """Verifiziert path. Bei expected_sha256 -> SHA256-Vergleich, sonst Größe>0.

    Eine leere Datei (0 Byte) gilt ohne erwarteten Hash als nicht verifiziert
    (False); mit erwartetem Hash als kaputter Download -> ValueError (ein
    0-Byte-Artefakt kann niemals ein gültiger Hash sein).
    """
    path = Path(path)
    if not path.exists():
        return False
    if path.stat().st_size == 0:
        if expected_sha256:
            raise ValueError(
                f"Download ist leer (0 Byte) — kaputter Download: {path}"
            )
        return False
    if expected_sha256:
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
        if h.hexdigest().lower() != expected_sha256.lower():
            raise ValueError(
                f"HTTP-Hash-Mismatch: erwartet {expected_sha256}, "
                f"erhalten {h.hexdigest()}"
            )
    return True
