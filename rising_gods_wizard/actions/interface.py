"""interface.py — ActionProtocol ABC (trockenlauf-/ausführungsfähige Aktionen).

Jede Aktion kennt ihren Kontext (ctx) und respektiert ctx.dry_run:
im Dry-Run wird nichts ausgeführt, sondern nur ein Plan protokolliert.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ActionProtocol(ABC):
    """Vertrag für alle Wizard-Aktionen (Bash-Parity-Herzstück)."""

    @abstractmethod
    def describe(self) -> str:
        """Menschenlesbare Beschreibung dieser Aktion (Logs/Pläne)."""

    @abstractmethod
    def dry_run_plan(self, *args: Any, **kwargs: Any) -> str:
        """Liefert den Plan-Text, der im Dry-Run ausgegeben würde."""

    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Führt die Aktion aus (real) oder protokolliert (dry-run)."""
