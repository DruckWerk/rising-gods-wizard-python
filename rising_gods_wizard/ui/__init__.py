"""ui/ — UI-Abstraktion (Interface + Backends).

Steps/Doctor rufen NUR UIProtocol. Konkrete Backends (WhiptailUI/RichUI)
werden in cli.py injiziert; NullUI ist der Default für --dry-run/CI.
"""
from __future__ import annotations

__all__ = ["interface", "null_ui", "progress", "rich_ui", "whiptail_ui"]
