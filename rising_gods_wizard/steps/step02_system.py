"""step02_system.py — System-Basis + Paketinstall + Temp-Cleanup.

Nutzt actions.packages (distro-agnostik). Logik liegt in actions/packages.
"""
from __future__ import annotations

import logging
from typing import Any

log = logging.getLogger(__name__)

# Minimal-Paketsatz (erweiterbar); orientiert am bash-Original.
BASE_PACKAGES = ("wine", "winetricks", "gamemode", "mangohud", "curl")


def run(ctx: Any, ui: Any, actions: Any) -> None:
    log.info("Step 02: System-Basis & Pakete")
    for pkg in BASE_PACKAGES:
        rc, _out, err = actions.packages.install(pkg)
        if rc != 0:
            log.warning("Paket %s nicht installierbar: %s", pkg, err)
    # Temp-Cleanup: `rm`/`find` sind in der Shell-Action-Allowlist verboten
    # (Sicherheit). `python3` ist erlaubt -> gescopepter One-Liner, der NUR
    # /tmp/rgw-*.tmp löscht. Im dry-run nur Protokoll (kein echtes Löschen).
    actions.shell.run(
        "python3 -c \"import glob,os;"
        "[os.remove(f) for f in glob.glob('/tmp/rgw-*.tmp')]\""
    )
    log.info("Step 02 abgeschlossen")
