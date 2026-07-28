"""templates — Vorlagen für vom Wizard erzeugte Artefakte.

Die Vorlagen liegen als reine Textdateien unter ``templates/`` (farblose
ASCII-Quelle). Das Package lädt sie zur Laufzeit via ``importlib.resources``,
damit es auch als Wheel funktioniert (kein relativer Dateisystem-Pfad).

Für den State-File-Inhalt wird bewusst KEINE Jinja-Abhängigkeit eingeführt:
``state.render(ctx)`` liefert bereits den bash-sourceable Inhalt. Die
``wizard_state.sh.j2``-Vorlage dient als menschenlesbare Referenz / als
Quelle für externe Tooling (z.B. ``tools/parity_diff.py``) und wird hier
nur als statischer Text geladen.
"""
from __future__ import annotations

from importlib import resources

from .. import state
from ..context import WizardContext

TEMPLATE_NAMES = ("wizard_state.sh.j2",)


def render_state_template(ctx: WizardContext) -> str:
    """Liefert den State-File-Inhalt (delegiert an ``state.render``).

    Bewusst keine Jinja-Abhängigkeit — der Inhalt ist identisch zur Vorlage
    ``wizard_state.sh.j2``, nur mit den aktuellen ctx-Werten gefüllt.
    """
    return state.render(ctx)


def read_template(name: str) -> str:
    """Liest eine Vorlagendatei aus dem ``templates``-Package (importlib)."""
    if name not in TEMPLATE_NAMES:
        raise ValueError(f"Unbekannte Vorlage: {name!r} (bekannt: {TEMPLATE_NAMES})")
    try:
        return resources.files(__package__).joinpath(name).read_text(encoding="utf-8")
    except (FileNotFoundError, ModuleNotFoundError, TypeError):  # pragma: no cover
        # Fallback für ältere importlib.resources ohne Package-Kontext
        import pathlib

        p = pathlib.Path(__file__).with_name(name)
        return p.read_text(encoding="utf-8")


__all__ = ["TEMPLATE_NAMES", "render_state_template", "read_template"]
