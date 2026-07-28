"""session.py — Session-Type Detection (x11/wayland/tty/unknown), PURE.

Quelle in Priorität: XDG_SESSION_TYPE -> WAYLAND_DISPLAY.
(Priority laut Spec erweiterbar um loginctl/Compositor-Suche — hier auf
 env-basierte Erkennung beschränkt, damit die Funktion PURE + testbar bleibt.)
"""
from __future__ import annotations

import os
from typing import Any


def detect_session_type(environ: dict[Any, Any] | None = None) -> str:
    """PURE: liefert 'x11'|'wayland'|'tty'|'unknown'.

    environ kann injiziert werden (Tests); default = os.environ.
    """
    env = environ if environ is not None else dict(os.environ)
    st = env.get("XDG_SESSION_TYPE", "").lower()
    if st in ("x11", "wayland", "tty"):
        return st
    if env.get("WAYLAND_DISPLAY"):
        return "wayland"
    return "unknown"


def detect_session(environ: dict[Any, Any] | None = None) -> str:
    """Alias/Entry-Point: liefert Session-Type (PURE, testbar via environ)."""
    return detect_session_type(environ)
