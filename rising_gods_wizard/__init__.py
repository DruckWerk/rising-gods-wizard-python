"""rising_gods_wizard — Rising Gods Linux Wizard (Voll-Python-Rewrite).

Haupt-Package. Erlaubt `import rising_gods_wizard` und `python -m
rising_gods_wizard`. Der Einstiegspunkt (CLI) liegt in `__main__.py`.

Version-Hinweis: Diese `__version__` ist die Version des Python-Pakets
(Release-Tracking). Der im erzeugten State-File verwendete
`config.WIZARD_VERSION`-String ("5.2-python") ist die kompatible
Wizard-Generation für Resume/Parity und bewusst anders (stammt aus dem
bash-Original-Stand).
"""
from __future__ import annotations

__version__ = "1.0.0"

__all__ = ["__version__"]
