"""install.py — DXVK Download + Entpacken in Wine-Prefix (dry-run-sicher).

Nutzt actions.shell (curl/tar/cp) + actions.fs. Im dry-run wird nur
protokolliert, keine echte Netzwerk-/FS-Seiteneffekt.

HINWEIS (Allowlist): actions/shell.py erlaubt aktuell nur eine Präfix-Allowlist
(echo, mkdir, cp, wine, ...). curl/wget/tar MÜSSEN dort freigeschaltet werden,
sonst lehnt ShellAction den Aufruf zur Laufzeit ab. Gehört in den actions-Chunk.
"""
from __future__ import annotations

import logging
from typing import Any

from ..context import WizardContext

log = logging.getLogger(__name__)

# DXVK-Upstream-Releases (GitHub). Version-Pinning empfohlen.
# (Coder-Vermutung: DXVK-Tarballs folgen dxvk-<version>.tar.gz — zu bestätigen
#  gegen github.com/doitsujin/dxvk/releases.)
DXVK_VERSION = "2.4"
DXVK_RELEASE_URL = (
    f"https://github.com/doitsujin/dxvk/releases/download/v{DXVK_VERSION}"
    f"/dxvk-{DXVK_VERSION}.tar.gz"
)


def build_dxvk_url(version: str = DXVK_VERSION) -> str:
    """PURE: liefert die DXVK-Download-URL für eine Version."""
    return (
        f"https://github.com/doitsujin/dxvk/releases/download/v{version}"
        f"/dxvk-{version}.tar.gz"
    )


def install_dxvk(ctx: WizardContext, actions: Any) -> None:
    """Lädt DXVK und entpackt die DLLs in das Wine-Prefix.

    dry-run: nur protokollieren. Real: curl + tar + cp via actions.shell.
    """
    if ctx.dry_run:
        log.info(
            "[dry-run] DXVK-Install: würde %s laden + nach %s entpacken",
            DXVK_RELEASE_URL, ctx.prefix,
        )
        return
    actions.shell.run(f"curl -fL -o /tmp/dxvk.tar.gz {DXVK_RELEASE_URL}")
    actions.shell.run("tar -xzf /tmp/dxvk.tar.gz -C /tmp")
    src = f"/tmp/dxvk-{DXVK_VERSION}"
    actions.shell.run(
        f"cp -r {src}/x64/* {ctx.prefix}/drive_c/windows/system32/"
    )
    actions.shell.run(
        f"cp -r {src}/x32/* {ctx.prefix}/drive_c/windows/syswow64/"
    )
    log.info("DXVK %s installiert in %s", DXVK_VERSION, ctx.prefix)
