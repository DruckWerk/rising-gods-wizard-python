"""actions/__init__.py — Paket-Init + Aggregator.

Exportiert die 3 Aktions-Klassen. Zusätzlich `Actions` als Aggregator, weil
state.write_state_file(ctx, actions) ein Objekt mit .fs/.shell/.packages
erwartet (siehe state.py, Chunk 1).
"""
from __future__ import annotations

from dataclasses import dataclass

from ..context import WizardContext
from .fs import FSAction
from .packages import PackageAction
from .shell import ShellAction


@dataclass
class Actions:
    """Bündelt alle Aktionen für einen Kontext (eine Instanz pro Wizard-Lauf)."""

    shell: ShellAction
    fs: FSAction
    packages: PackageAction

    @classmethod
    def build(cls, ctx: WizardContext) -> Actions:
        return cls(
            shell=ShellAction(ctx),
            fs=FSAction(ctx),
            packages=PackageAction(ctx),
        )


__all__ = ["Actions", "FSAction", "PackageAction", "ShellAction"]
