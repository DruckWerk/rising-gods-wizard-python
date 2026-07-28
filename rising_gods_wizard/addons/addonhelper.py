"""addonhelper.py — Reguläre Online-Addons (opt-in, default OFF).

install_addons(ctx, ui, actions) installiert reguläre Addons von
config.ADDON_BASE_URL. Per Spec §11.6 standardmässig AUS (ctx.addons_enabled).
Bei deaktiviertem Flag wird sauber returned (kein Netz-Zugriff).
"""
from __future__ import annotations

from typing import Any

from .. import config
from .ui import resolve_ui


def install_addons(ctx: Any, ui: Any = None, actions: Any = None) -> list[str]:
    """Installiert reguläre Addons, falls ctx.addons_enabled (Opt-in §11.6).

    Default OFF -> bei deaktiviert kein Netz, leere Liste. Liefert Liste
    installierter Addon-Namen.
    """
    ui = resolve_ui(ui)
    if not getattr(ctx, "addons_enabled", config.ADDONS_DEFAULT_ENABLED):
        ui.note("Reguläre Addons deaktiviert (Opt-in, §11.6) — übersprungen.")
        return []

    if actions is None:
        raise RuntimeError("actions erforderlich für Addon-Install.")
    selected = getattr(ctx, "addons_selected", []) or []
    installed: list[str] = []
    for name in selected:
        url = f"{config.ADDON_BASE_URL}/{name}.zip"
        dest = ctx.addons_dir / name
        if hasattr(actions, "fs"):
            actions.fs.mkdir(dest, mode=0o755)
        else:
            dest.mkdir(parents=True, exist_ok=True)
        ui.note(f"Installiere Addon '{name}' -> {url}")
        rc, _, err = actions.shell.run(f"curl -fL -o {dest / (name + '.zip')} {url}")
        if rc != 0:
            raise RuntimeError(f"Addon '{name}' fehlgeschlagen ({rc}): {err}")
        installed.append(name)
    return installed
