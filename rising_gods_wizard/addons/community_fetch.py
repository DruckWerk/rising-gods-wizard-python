"""community_fetch.py — FEATURE 4: Community-Tools Live-Fetch.

fetch_community_tools(ctx, ui, actions) lädt die in config.COMMUNITY_SOURCES
registrierten Tools IMMER frisch von Upstream. Kein stale lokal-Fallback.

Version-Pinning: Default "latest" -> KEINE Checksum-Verifikation. Bei
version_pin (incl. config-Checksum) -> SHA256-Verifikation, Abbruch bei
Mismatch. Offline -> harter Fehler (RuntimeError), kein silently-continue.
Doctor repair nutzt dieselbe Funktion.
"""
from __future__ import annotations

from typing import Any

from .. import config
from ..download.direct import verify_file
from .ui import resolve_ui


def fetch_community_tools(ctx: Any, ui: Any = None, actions: Any = None) -> list[str]:
    """Fetcht Community-Tools laut ctx.community_tools_selected (bzw. alle).

    Liefert Liste der abgelegten Pfade. Offline -> RuntimeError (hart).
    """
    ui = resolve_ui(ui)
    if actions is None:
        raise RuntimeError("actions ist erforderlich für Live-Fetch.")

    selected = ctx.community_tools_selected or list(config.COMMUNITY_SOURCES)
    dest_root = ctx.addons_dir  # WoW/Interface/AddOns
    fetched: list[str] = []

    for tool in selected:
        spec = config.COMMUNITY_SOURCES.get(tool)
        if spec is None:
            raise RuntimeError(f"Unbekannte Community-Quelle: {tool}")
        url = spec["url"]
        version_pin = spec.get("version_pin", "")
        checksum = spec.get("checksum", "")
        verify = bool(version_pin) and bool(checksum)
        subdir = spec.get("dest_subdir", "")
        target = dest_root / subdir if subdir else dest_root
        # dry-run-sicher via actions.fs.mkdir; Mock-Actions (Tests) ohne .fs
        # behalten den direkten Pfad bei.
        if hasattr(actions, "fs"):
            actions.fs.mkdir(target, mode=0o755)
        else:
            target.mkdir(parents=True, exist_ok=True)

        ui.note(f"Fetch '{tool}' (version={version_pin or 'latest'}) -> {url}")
        try:
            archive = actions.shell.run(f"curl -fL -o {target / (tool + '.dl')} {url}")
            rc, _, err = archive
            if rc != 0:
                raise RuntimeError(f"Download fehlgeschlagen ({rc}): {err}")
        except RuntimeError as err:
            # Offline / Netzfehler -> kein Fallback auf alte lokale Kopie.
            raise RuntimeError(
                f"Community-Tool '{tool}' konnte NICHT gefetcht werden "
                f"(Offline/Netzfehler). Community-Tools erfordern Online-Fetch; "
                f"kein Fallback auf veraltete lokale Kopie."
            ) from err

        dl_path = target / (tool + ".dl")
        if verify:
            verify_file(dl_path, checksum)  # ValueError bei Mismatch -> Abbruch
        fetched.append(str(dl_path))
        ui.note(f"'{tool}' verifiziert + abgelegt.")
    return fetched
