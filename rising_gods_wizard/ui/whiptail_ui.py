"""whiptail_ui.py — WhiptailUI: interaktive Prompts via `whiptail` (newt).

Hinweis: whiptail ist ein TTY-basiertes UI-Frontend. Es wird DAHER direkt
via subprocess gerufen (nicht über actions.shell.run — jenes erzwingt
capture_output, wodurch whiptail kein Terminal bekäme und nichts anzeigen
könnte). Ist whiptail nicht installiert, fallen alle Prompts auf das
NoopUI-Verhalten (Default-Rückgabe) zurück — kein Crash.

V2-03: optionales ``theme``-Argument (steuert primär den Titel-Stil; newt ist
farblich limitiert). ``ask_yes_no_c`` liefert "cancel" bei ESC/RC!=0.
Progress-Methoden sind no-op (whiptail hat eigene Fortschrittsanzeige).
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from typing import Any

from .interface import Cancel, NoopUI
from .theme import Theme, get_theme


class WhiptailUI(NoopUI):
    def __init__(
        self,
        prompts: dict[Any, Any] | None = None,
        actions: Any = None,
        title: str = "Rising Gods Wizard",
        theme: Theme | None = None,
    ) -> None:
        self._prompts = prompts or {}
        self._actions = actions
        self._title = title
        self._theme = theme or get_theme("ice")
        self._have = shutil.which("whiptail") is not None

    # ── Display (whiptail kann kein Banner/Log; plain stdout/stderr) ────
    def note(self, msg: str) -> None:
        print(msg)

    def warn(self, msg: str) -> None:
        print(f"WARN: {msg}", file=sys.stderr)

    def error(self, msg: str) -> None:
        print(f"ERROR: {msg}", file=sys.stderr)

    # ── Prompts ────────────────────────────────────────────────────────
    def ask_yes_no(self, q: str, default: bool = True) -> bool:
        if not self._have:
            return default
        args = ["whiptail", "--title", self._title, "--yesno", q, "10", "60"]
        if not default:
            args.insert(3, "--defaultno")
        rc = subprocess.run(
            args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False
        ).returncode
        return rc == 0

    def ask_yes_no_c(self, q: str, default: bool = True) -> bool | Cancel:
        # Ohne whiptail-Binary kein Cancel möglich -> Proceed mit default.
        if not self._have:
            return default
        args = ["whiptail", "--title", self._title, "--yesno", q, "10", "60"]
        if not default:
            args.insert(3, "--defaultno")
        rc = subprocess.run(
            args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False
        ).returncode
        # RC==0 -> Ja, RC==1 -> Nein, RC!=0/ESC -> cancel
        if rc == 0:
            return True
        if rc == 1:
            return False
        return "cancel"

    def ask_choice(self, q: str, options: list[str], default: str = "") -> str:
        if not self._have or not options:
            return default
        items: list[str] = []
        for opt in options:
            items += [opt, ""]
        sel = subprocess.run(
            ["whiptail", "--title", self._title, "--menu", q,
             "15", "60", "5", *items],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True,
            check=False,
        )
        return sel.stdout.strip() if sel.returncode == 0 else default

    def prompt(self, q: str, default: str = "") -> str:
        if not self._have:
            return default
        r = subprocess.run(
            ["whiptail", "--title", self._title, "--inputbox", q,
             "10", "60", default],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True,
            check=False,
        )
        return r.stdout.strip() if r.returncode == 0 else default
