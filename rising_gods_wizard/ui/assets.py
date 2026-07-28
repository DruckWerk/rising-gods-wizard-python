"""assets.py — AssetRenderer: farblose ASCII-Quelle + Laufzeit-Theming (V2a).

Spiegelt das kanonische ``templates/__init__.py``-Pattern (importlib.resources,
Wheel-sicher, Fallback via Path). ``render`` ist rein/deterministisch; der
einzige Seiteneffekt (Typewriter-Sleep + Print) liegt zentral in ``paint``.
"""
from __future__ import annotations

from importlib import resources
from pathlib import Path
from time import sleep
from typing import TYPE_CHECKING, Any

from .theme import Theme

if TYPE_CHECKING:  # rich ist optional (nur extra), zur Laufzeit ggf. nicht da
    from rich.console import Console

ASSET_NAMES = frozenset(
    {
        "banner_header",
        "banner_main",
        "frost_complete",
        "snow_spinner",
        "arthas_quote",
        "arthas_quote_2",
        "arthas_quote_3",
        "arthas_quote_4",
    }
)


def _style(text: str, style: str) -> str:
    return f"[{style}]{text}[/{style}]"


class AssetRenderer:
    def __init__(self, theme: Theme, console: Console | None = None) -> None:
        self._theme = theme
        self._console: Console | None = console

    def load_source(self, name: str) -> str:
        """Liest die farblose ASCII-Quelle. KeyError, wenn ``name`` unbekannt."""
        if name not in ASSET_NAMES:
            raise KeyError(name)
        fname = f"{name.replace('_', '-')}.txt"
        try:
            return (
                resources.files("rising_gods_wizard")
                .joinpath("assets")
                .joinpath(fname)
                .read_text(encoding="utf-8")
            )
        except (FileNotFoundError, ModuleNotFoundError, TypeError):  # pragma: no cover
            return (
                Path(__file__).with_name("..") / "assets" / fname
            ).read_text(encoding="utf-8")

    def render(
        self,
        name: str,
        *,
        box: bool = False,
        typewriter: bool = False,
        align: str = "left",
    ) -> str:
        """Liefert den vollständigen, themed-String (rein, deterministisch).

        ``typewriter`` steuert NUR ``paint()``, nie den Rückgabestring.
        """
        raw = self.load_source(name).splitlines()
        width = max((len(ln) for ln in raw), default=0)
        if align == "center":
            body = [ln.center(width) for ln in raw]
        elif align == "right":
            body = [ln.rjust(width) for ln in raw]
        else:
            body = list(raw)
        if not box:
            return "\n".join(_style(ln, self._theme.primary) for ln in body)
        bar = _style("═" * width, self._theme.box_style)
        top = _style("╔", self._theme.box_style) + bar + _style(
            "╗", self._theme.box_style
        )
        bot = _style("╚", self._theme.box_style) + bar + _style(
            "╝", self._theme.box_style
        )
        rows: list[str] = []
        side = _style("║", self._theme.box_style)
        for ln in body:
            pad = " " * (width - len(ln))
            rows.append(side + _style(ln, self._theme.primary) + pad + side)
        return "\n".join([top, *rows, bot])

    def paint(self, name: str, **kw: Any) -> None:
        """Rendert + schreibt auf ``self._console``. console=None → no-op.

        Typewriter-Sleep EXITIERT NUR HIER (zentrale Animationsstelle).
        """
        if self._console is None:
            return
        box = bool(kw.get("box", False))
        typewriter = bool(kw.get("typewriter", False))
        align = str(kw.get("align", "left"))
        text = self.render(name, box=box, typewriter=typewriter, align=align)
        if not typewriter:
            self._console.print(text)
            return
        for ch in text:
            self._console.print(ch, end="")
            sleep(0.004)
        self._console.print()
