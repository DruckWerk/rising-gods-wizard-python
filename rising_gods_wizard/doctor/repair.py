"""repair.py — behebt gefundene Probleme (Doctor repair).

- realmlist: write_realmlist (Backup vorher)
- Community-Tools: fetch_community_tools (frisch von Upstream)
Jede Aktion mit ui.ask_yes_no bestätigen.
"""
from __future__ import annotations

from typing import Any

from .. import config
from ..addons.community_fetch import fetch_community_tools
from ..context import WizardContext
from ..game.realmlist import (
    detect_realmlist_path,
    needs_correction,
    write_realmlist,
)


def repair(ctx: WizardContext, ui: Any, actions: Any) -> list[str]:
    """Führt Reparaturen aus. Liefert Liste der erledigten Aktionen."""
    done: list[str] = []

    # Realmlist korrigieren (falls nötig)
    rpath = detect_realmlist_path(ctx)
    if needs_correction(rpath) and ui.ask_yes_no(
        f"Realmlist korrigieren auf {config.REALMLIST_HOST}?", default=True
    ):
        p = write_realmlist(ctx, actions, rpath)
        done.append(f"realmlist geschrieben: {p}")

    # Community-Tools neu fetchen
    ctx.community_tools_selected = ctx.community_tools_selected or list(
        config.COMMUNITY_SOURCES
    )
    if ui.ask_yes_no("Community-Tools neu herunterladen?", default=True):
        fetched = fetch_community_tools(ctx, ui, actions)
        done.append(f"{len(fetched)} Community-Tools gefetcht")

    return done
