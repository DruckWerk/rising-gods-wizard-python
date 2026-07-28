"""realmlist.py — Feature 5: realmlist.wtf-Verifikation (vorh. Installation).

Prüft bei ctx.existing_install == True die Locale-spezifische realmlist.wtf
(Data/{enGB,enUS,deDE}/realmlist.wtf, erste Treffer-Datei) gegen
config.REALMLIST_HOST. Bei Abweichung/Fehlen: UI-Prompt zur Korrektur;
bei Zustimmung Backup + korrekter Write über actions.fs.

Design: verify_realmlist(ctx, ui, actions) nutzt reine Helfer
(detect_realmlist_path, parse_realmlist_host, needs_correction), damit die
Logik ohne echte FS-/UI-Side-Effects testbar ist.
"""
from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from .. import config
from ..context import WizardContext

REALMLIST_LINE = 'set realmlist "{host}"'


def detect_realmlist_path(ctx: WizardContext) -> Path | None:
    """Erste vorhandene realmlist.wtf eines der Locale-Verzeichnisse."""
    for locale in config.REALMLIST_LOCALES:
        p = ctx.data_dir / locale / "realmlist.wtf"
        if p.exists():
            return p
    return None


def parse_realmlist_host(path: Path) -> str | None:
    """Liest den Host aus der ersten `set realmlist`-Zeile (None wenn fehlt)."""
    if not path.exists():
        return None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line.startswith("set realmlist"):
            parts = line.split(None, 2)
            if len(parts) >= 3:
                return parts[2].strip().strip('"')
    return None


def needs_correction(path: Path | None, host: str = config.REALMLIST_HOST) -> bool:
    """True, wenn Datei fehlt oder falschen Host enthält."""
    if path is None:
        return True
    return parse_realmlist_host(path) != host


def write_realmlist(ctx: WizardContext, actions: Any, path: Path | None = None) -> Path:
    """Schreibt die korrekte realmlist-Zeile (Backup des Originals vorher)."""
    target = path or (ctx.data_dir / config.REALMLIST_LOCALES[0] / "realmlist.wtf")
    if not ctx.dry_run and target.exists():
        shutil.copy2(target, target.with_suffix(".wtf.bak"))
    actions.fs.write(target, REALMLIST_LINE.format(host=config.REALMLIST_HOST) + "\n")
    return target


def verify_realmlist(ctx: WizardContext, ui: Any, actions: Any) -> str:
    """Feature-5-Hauptfunktion. Liefert ein Status-Log (Meldung).

    Wird NUR bei ctx.existing_install aufgerufen (siehe Step05).
    dry-run / NullUI: nur protokollieren, kein Schreiben.
    """
    if not ctx.existing_install:
        return "realmlist: übersprungen (keine vorh. Installation)"

    path = detect_realmlist_path(ctx)
    if not needs_correction(path):
        return f"realmlist: OK ({path}) -> {config.REALMLIST_HOST}"

    # Abweichung oder fehlend
    if path is None:
        msg = "realmlist: fehlend -> wird erzeugt"
    else:
        msg = f"realmlist: falscher Host -> Korrektur auf {config.REALMLIST_HOST}"

    # Entscheidung: Prompt (echte UI) oder Auto-Protokoll (NullUI/dry-run)
    do_write = True
    if ui is not None and hasattr(ui, "ask_yes_no"):
        do_write = ui.ask_yes_no(f"{msg}. Korrigieren?", default=True)
    elif ctx.dry_run:
        do_write = False  # dry-run ohne UI: nur protokollieren

    if do_write:
        write_realmlist(ctx, actions, path)
        return f"{msg} (geschrieben)"
    return f"{msg} (vom Nutzer abgelehnt / dry-run protokolliert)"
