"""interface.py — Abstraktes UI-Protokoll + Noop/Null-Basen.

Definiert UIProtocol (Methoden, die Steps/Doctor erwarten) und zwei
no-op-Basisklassen (NoopUI, NullUI) für dry-run/CI/Headless.
"""
from __future__ import annotations

import sys
from abc import ABC, abstractmethod


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


class NullUI(NoopUI):
    """Für dry-run/CI: no-op (error zusätzlich nach stderr)."""
    def error(self, msg: str) -> None:
        print(f"ERROR: {msg}", file=sys.stderr)
