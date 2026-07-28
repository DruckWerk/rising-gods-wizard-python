"""layout.py — reine Markup-Layout-Funktionen (V2b, siehe architect-spec-v2 §3).

Baut themed rich-Markup-Strings OHNE I/O. ``AssetRenderer.render`` wird
absichtlich NICHT aufgerufen — layout ist eine reine Markup-Schicht über
den bereits existierenden ``assets.py``/``theme.py``-Bausteinen.
"""
from __future__ import annotations

from .assets import AssetRenderer
from .theme import Theme, get_theme


def _style(text: str, style: str) -> str:
    return f"[{style}]{text}[/{style}]"


def panel(renderer: AssetRenderer, title: str, body: str) -> str:
    """Themed Kasten (theme.box_style) um die title- und body-Zeile."""
    theme = renderer._theme
    box = theme.box_style
    w = max(len(title), len(body)) + 2
    bar = "═" * w
    top = _style("╔" + bar + "╗", box)
    bot = _style("╚" + bar + "╝", box)

    def row(text: str) -> str:
        pad = " " * (w - len(text))
        return _style("║ " + text + pad + " ║", box)

    return "\n".join([top, row(title), row(body), bot])


def divider(renderer: AssetRenderer, char: str = "─") -> str:
    """Trennlinie in theme.box_style (default: ─)."""
    theme = renderer._theme
    return _style(char * 40, theme.box_style)


def columns(items: list[str], widths: list[int], align: list[str]) -> str:
    """Spaltenausrichtung left/center/right, durch │ getrennt."""
    cells: list[str] = []
    for item, width, a in zip(items, widths, align, strict=True):
        if a == "right":
            cells.append(item.rjust(width))
        elif a == "center":
            cells.append(item.center(width))
        else:
            cells.append(item.ljust(width))
    return " │ ".join(cells)


def step_header(n: int, total: int, title: str, theme: Theme) -> str:
    """Schritt-Header im theme.banner_style, z.B. 'Schritt 7/17: Foo'."""
    return _style(f"Schritt {n}/{total}: {title}", theme.banner_style)


__all__ = ["panel", "divider", "columns", "step_header", "get_theme"]
