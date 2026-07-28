"""rich_ui.py — RichUI: formatierte Ausgaben via `rich` (optional).

Import ist guarded: fehlt rich ODER display=False, fallen alle Methoden auf
stille/plain-Ausgabe zurück (kein Crash). Empfohlenes Display-Backend.
"""
from __future__ import annotations

from .interface import NoopUI

try:
    from rich.console import Console
    _RICH = True
except Exception:  # noqa: BLE001 - gewollt: rich ist optional
    Console = None
    _RICH = False


class RichUI(NoopUI):
    def __init__(self, display: bool = True):
        self._display = display and _RICH
        self._console = Console() if self._display else None

    def note(self, msg: str) -> None:
        if self._console:
            self._console.print(f"[cyan]{msg}[/cyan]")
        else:
            print(msg)

    def warn(self, msg: str) -> None:
        if self._console:
            self._console.print(f"[yellow]WARN: {msg}[/yellow]")
        else:
            print(f"WARN: {msg}")

    def error(self, msg: str) -> None:
        if self._console:
            self._console.print(f"[red]ERROR: {msg}[/red]")
        else:
            print(f"ERROR: {msg}")

    def show_step(self, n: int, total: int, title: str) -> None:
        if self._console:
            self._console.print(f"[bold blue]Schritt {n}/{total}:[/] {title}")

    def render_banner(self, text: str) -> None:
        if self._console:
            self._console.print(f"[bold white]{text}[/bold white]")
