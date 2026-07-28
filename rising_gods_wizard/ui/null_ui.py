"""null_ui.py — NullUI-Re-Export (siehe interface.py).

Die eigentliche NullUI-Klasse lebt in interface.py; hier wird sie für
`from rising_gods_wizard.ui.null_ui import NullUI` re-exportiert, damit
das Backend-Bundle genau dem Chunk-8-File-Layout entspricht.
"""
from __future__ import annotations

from .interface import NullUI

__all__ = ["NullUI"]
