"""hd.py — HD-Texturen-Option (Doctor hd).

Lädt HD-Textur-Paket herunter + installiert nach Data/. Der Quell-URL ist in
config.HD_TEXTURE_URL konfigurierbar (Default: leer -> klarer Fehler, kein
silent-Fallback). Bestätigung via ui.ask_yes_no.
"""
from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

from .. import config
from ..context import WizardContext


def _filename_from_url(url: str) -> str:
    path = urlparse(url).path
    return path.rsplit("/", 1)[-1] or "hd-textures.7z"


def install_hd_textures(ctx: WizardContext, ui: Any, actions: Any) -> str:
    """Lädt + installiert HD-Texturen. Liefert Zielpfad (oder Fehlermeldung)."""
    url = getattr(config, "HD_TEXTURE_URL", "") or ctx.extra.get(
        "hd_texture_url", ""
    )
    if not url:
        raise RuntimeError(
            "HD-Texturen: kein Quell-URL konfiguriert (config.HD_TEXTURE_URL). "
            "Bitte in config.py setzen; kein silent-Fallback."
        )
    dest = ctx.data_dir / _filename_from_url(url)
    dest.parent.mkdir(parents=True, exist_ok=True)

    if ui.ask_yes_no(f"HD-Texturen herunterladen ({url})?", default=True):
        rc, _, err = actions.shell.run(f"curl -fL -o {dest} {url}")
        if rc != 0:
            raise RuntimeError(f"HD-Download fehlgeschlagen ({rc}): {err}")
        ui.note(f"HD-Texturen abgelegt: {dest}")
        return str(dest)
    return "vom Nutzer abgelehnt"
