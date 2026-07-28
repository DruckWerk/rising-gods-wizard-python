"""interface.py — Abstraktes UI-Protokoll + Noop/Null-Basen.

Definiert UIProtocol (Methoden, die Steps/Doctor erwarten) und zwei
no-op-Basisklassen (NoopUI, NullUI) für dry-run/CI/Headless.

V2-03-Erweiterung (architect-spec-v2 §3/§6):
  - ask_yes_no_c() -> bool | "cancel"  (distinkter Cancel-Status)
  - start_progress/update_progress/stop_progress  (Progress-Senke, no-op Default)
"""
from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from typing import Literal

# Distinkter Cancel-Rückgabewert der ask_*-Variante.
Cancel = Literal["cancel"]


class UIProtocol(ABC):
    """Minimales UI-Protokoll (Dependency Inversion).

    Steps/Doctor rufen NUR diese Methoden. Konkrete Backends
    (WhiptailUI/RichUI) implementieren sie; NullUI/NoopUI liefern no-op.
    """

    @abstractmethod
    def note(self, msg: str) -> None: ...

    @abstractmethod
    def warn(self, msg: str) -> None: ...

    @abstractmethod
    def error(self, msg: str) -> None: ...

    @abstractmethod
    def ask_yes_no(self, q: str, default: bool = True) -> bool: ...

    @abstractmethod
    def ask_choice(self, q: str, options: list[str], default: str = "") -> str: ...

    @abstractmethod
    def prompt(self, q: str, default: str = "") -> str: ...

    @abstractmethod
    def ask_yes_no_c(self, q: str, default: bool = True) -> bool | Cancel:
        """Ja/Nein mit distinktem Cancel-Status.

        Rückgabe: True/False bei Entscheidung, "cancel" bei Abbruch (ESC).
        Backends ohne Cancel-Semantik (NullUI) liefern ``default``.
        """

    # ── Optionale Progress-Senke (§6) ──────────────────────────────────
    # Default-Implementierung ist no-op; konkrete Backends (RichUI) delegieren
    # an ihre Progress-Instanz. WhiptailUI/NullUI erben den no-op.
    def start_progress(self, total: int = 100) -> None:  # noqa: B027
        """Optional: Progress starten (Default no-op)."""

    def update_progress(self, fraction: float, label: str = "") -> None:  # noqa: B027
        """Optional: Progress aktualisieren, fraction 0.0..1.0 (Default no-op)."""

    def stop_progress(self) -> None:  # noqa: B027
        """Optional: Progress beenden (Default no-op)."""


class NoopUI(UIProtocol):
    """Basis: alle Methoden no-op (keine Ausgabe)."""

    def note(self, msg: str) -> None:
        pass

    def warn(self, msg: str) -> None:
        pass

    def error(self, msg: str) -> None:
        pass

    def ask_yes_no(self, q: str, default: bool = True) -> bool:
        return default

    def ask_choice(self, q: str, options: list[str], default: str = "") -> str:
        return default

    def prompt(self, q: str, default: str = "") -> str:
        return default

    def ask_yes_no_c(self, q: str, default: bool = True) -> bool | Cancel:
        # Headless/Noop: kein Cancel — Proceed mit default.
        return default


class NullUI(NoopUI):
    """Für dry-run/CI: no-op (error zusätzlich nach stderr)."""

    def error(self, msg: str) -> None:
        print(f"ERROR: {msg}", file=sys.stderr)
