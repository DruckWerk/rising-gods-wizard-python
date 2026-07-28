"""prefix.py — Wine-Prefix-Anlage (Side-Effecting via actions).

Legt das WINEPREFIX-Verzeichnis an und initialisiert es (wineboot),
falls noch nicht geschehen. Respektiert ctx.dry_run (nur Protokoll).
"""
from __future__ import annotations

import logging

from ..actions import Actions
from ..context import WizardContext

log = logging.getLogger(__name__)


def create_prefix(ctx: WizardContext, actions: Actions) -> None:
    """Erstellt das Wine-Prefix und initialisiert es via wineboot.

    Setzt WINEPREFIX/WINEARCH und nutzt ausschließlich die actions-
    Schnittstelle, damit ein Dry-Run keine echten Nebenwirkungen erzeugt.
    """
    prefix = ctx.prefix
    log.info("Wine-Prefix sicherstellen: %s", prefix)

    # Verzeichnis anlegen (mkdir via actions.fs)
    actions.fs.mkdir(prefix, mode=0o755)

    # wineboot initialisiert das Prefix (winecfg wäre interaktiv → hier nur boot)
    # Env via `env` übergeben (in der Shell-Action-Allowlist erlaubt), damit
    # kein raw-Env-Prefix die Allowlist verletzt.
    cmd = (
        f"env WINEPREFIX={prefix} WINEARCH=win64 "
        f"{ctx.wine_cmd} wineboot -i"
    )
    log.info("Initialisiere Prefix via wineboot")
    actions.shell.run(cmd)
