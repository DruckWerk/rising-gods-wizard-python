"""ui.py — Minimales UI-Protokoll für Module ohne echtes UI.

Die Module (download/addons) erwarten ein `ui`-Objekt mit note/warn/error.
Ohne echtes UI genügt ein Noop-Logger (dry-run/Tests). Echtes UI (Textual/
RichUI) implementiert dieselben Methoden.
"""
from __future__ import annotations

from typing import Any


class NoopUI:
    """Stille UI-Implementierung (Default für Module/Tests)."""

    def note(self, msg: str) -> None:
        pass

    def warn(self, msg: str) -> None:
        pass

    def error(self, msg: str) -> None:
        pass


def resolve_ui(ui: Any) -> object:
    """Liefert ui oder NoopUI, wenn ui None/fehlt."""
    return ui if ui is not None else NoopUI()
