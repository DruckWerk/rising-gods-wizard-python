"""rich_ui.py — RichUI: formatierte Ausgaben via `rich` (optional).

Import ist guarded: fehlt rich ODER display=False, fallen alle Methoden auf
stille/plain-Ausgabe zurück (kein Crash). Empfohlenes Display-Backend.

V2-04: RichUI nutzt AssetRenderer in show_step/render_banner (paint) und ist der
race-freie Display-Koordinator für Progress (§6). AssetRenderer.paint() läuft
AUSSERHALB eines aktiven Live-Kontextes (vor Progress.start() / nach stop()),
damit kein ANSI-Flicker-Race entsteht.
"""
from __future__ import annotations

from typing import Any, cast

from .assets import AssetRenderer
from .interface import Cancel, NoopUI
from .layout import step_header
from .progress import make_progress
from .theme import Theme, get_theme

# Optional: rich ist ein extra (nicht Pflicht). Zur Laufzeit ggf. nicht da.
Console: Any = None
Confirm: Any = None
_RICH = False

try:
    from rich.console import Console as _Console
    from rich.prompt import Confirm as _Confirm

    Console = _Console
    Confirm = _Confirm
    _RICH = True
except Exception:  # noqa: BLE001 - gewollt: rich ist optional
    pass


class RichUI(NoopUI):
    def __init__(self, display: bool = True, theme: Theme | None = None) -> None:
        self._theme = theme or get_theme("ice")
        self._display = display and _RICH
        self._console: Console | None = Console() if self._display else None
        # AssetRenderer an dieselbe Console gebunden (race-freie Senke).
        self._renderer = AssetRenderer(self._theme, console=self._console)
        # Progress-Senke (Display-Koordinator). _progress ist None, solange
        # kein Live-Kontext aktiv ist -> Guard gegen ANSI-Flicker-Race.
        self._progress: Any = None

    def note(self, msg: str) -> None:
        if self._console:
            self._console.print(f"[{self._theme.primary}]{msg}[/{self._theme.primary}]")
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

    def show_step(self, n: int, total: int, title: str) -> str:
        """Step-Header via layout.step_header; race-frei (kein aktiver Live).

        Liefert den themed-String zurück (deterministisch, auch bei
        console=None), und paintet ihn nur bei console present.
        """
        markup = step_header(n, total, title, self._theme)
        self._safe_paint_text(markup)
        return markup

    def render_banner(
        self, asset_name: str, *, box: bool = False, typewriter: bool = False
    ) -> str:
        """Liefert den themed-String (render) und paintet ihn race-frei.

        - Bei console present: paint() NUR, wenn KEIN aktiver Live-Kontext
          (Progress nicht gestartet) -> kein ANSI-Flicker-Race.
        - Bei dry_run/headless (console=None): kein paint (no-op), Rückgabe
          des reinen themed-Strings trotzdem (deterministisch, testbar).
        - typewriter steuert NUR paint(), nie den Rückgabestring.
        """
        text = self._renderer.render(asset_name, box=box, typewriter=typewriter)
        if self._console is not None and self._progress is None:
            # Race-frei: außerhalb aktivem Live-Kontext.
            self._renderer.paint(asset_name, box=box, typewriter=typewriter)
        return text

    def _safe_paint_text(self, markup: str) -> None:
        """Schreibt fertiges rich-Markup race-frei (kein Live-Kontext aktiv)."""
        if self._console is not None and self._progress is None:
            self._console.print(markup)

    def ask_yes_no_c(self, q: str, default: bool = True) -> bool | Cancel:
        # Ohne Console (headless/plain fallback) kein Cancel -> Proceed default.
        if not self._console or Confirm is None:
            return default
        try:
            return cast("bool | Cancel", Confirm.ask(q, default=default, console=self._console))
        except (KeyboardInterrupt, EOFError):  # ESC / Cancel
            return "cancel"

    # ── Progress-Senke (race-freier Display-Koordinator, §6) ──────────
    def start_progress(self, total: int = 100) -> None:
        if self._console is None:
            return
        # paint() ist erst wieder erlaubt, nachdem stop_progress() läuft.
        self._progress = make_progress(backend="rich")
        self._progress.update(0.0, "")

    def update_progress(self, fraction: float, label: str = "") -> None:
        if self._progress is not None:
            self._progress.update(fraction, label)

    def stop_progress(self) -> None:
        if self._progress is not None:
            self._progress.close()
            self._progress = None
