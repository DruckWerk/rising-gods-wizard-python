"""uninstall.py — entfernt Prefix + State + Addons (Doctor uninstall).

Nutzt shutil.rmtree (sicher; `rm` ist in der Shell-Action-Allowlist nicht
erlaubt -> direkter, kontrollierter Aufruf). Bestätigung via ui.ask_yes_no.
"""
from __future__ import annotations

import shutil
from typing import Any

from ..context import WizardContext


def uninstall(ctx: WizardContext, ui: Any, actions: Any) -> list[str]:
    """Entfernt Prefix, Addons, State. Liefert Liste gelöschter Pfade."""
    targets = [ctx.prefix, ctx.addons_dir, ctx.state_file]
    if not ui.ask_yes_no(
        "WIRKLICH Prefix + Addons + State entfernen? (irreversibel)",
        default=False,
    ):
        return ["abgebrochen"]

    done: list[str] = []
    for t in targets:
        p = ctx.prefix if t is ctx.prefix else t  # explizit für Klarheit
        if p.exists():
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()
            done.append(str(p))
    return done
