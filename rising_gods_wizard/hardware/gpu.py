"""gpu.py — GPU Auto-Detection (PURE, testbar).

Liest lspci-Ausgabe, mappt auf GPU-Vendor + Perf-Klasse.
Konsistent mit context.HardwareSnapshot (gpu_vendor, perf_class):
  perf_class ∈ weak|old|low|mid|high|ultra
  (Chunk-Spec nennt WEAK/MID/HIGH/ULTRA als Hauptklassen — wir nutzen die im
   Projekt etablierte 6er-Skala für Konsistenz mit game/fps_boost + state.)
"""
from __future__ import annotations

import logging
import re
from typing import Any

from ..context import WizardContext

log = logging.getLogger(__name__)


def parse_vendor(lspci_output: str) -> str:
    """PURE: liefert 'nvidia' | 'amd' | 'intel' | 'unknown' aus lspci-Text."""
    low = lspci_output.lower()
    if "nvidia" in low:
        return "nvidia"
    if "amd" in low or "advanced micro devices" in low or "radeon" in low:
        return "amd"
    if "intel" in low:
        return "intel"
    return "unknown"


def detect_gpu_class(lspci_output: str) -> str:
    """PURE: mappt lspci-Text auf Perf-Klasse (weak..ultra).

    Heuristik (deterministisch, testbar):
      - kein/unknown Vendor           -> weak
      - Intel (iGPU)                  -> low
      - AMD diskret                   -> high
      - NVIDIA High-End (RTX40xx,
        3080/3090/4080/4090, Titan)   -> ultra
      - NVIDIA sonstige diskret       -> high
    """
    vendor = parse_vendor(lspci_output)
    if vendor == "unknown":
        return "weak"
    if vendor == "intel":
        return "low"
    if vendor == "amd":
        return "high"
    low = lspci_output.lower()
    high_end = re.search(r"(rtx\s*4\d{2}|3080|3090|4080|4090|titan)", low)
    return "ultra" if high_end else "high"


def detect_gpu(ctx: WizardContext, actions: Any, lspci_output: str | None = None) -> None:
    """Befüllt ctx.hw (gpu_vendor, perf_class) via lspci.

    dry-run: nur protokollieren, kein echter lspci-Aufruf.
    lspci_output kann injiziert werden (Tests/Headless).
    """
    if lspci_output is None:
        if ctx.dry_run:
            log.info("[dry-run] GPU-Detection: würde 'lspci' ausführen")
            return
        rc, out, _ = actions.shell.run("lspci")
        if rc != 0:
            log.warning("lspci lieferte rc=%s — GPU unbekannt", rc)
            lspci_output = ""
        else:
            lspci_output = out
    ctx.hw.gpu_vendor = parse_vendor(lspci_output)
    ctx.hw.perf_class = detect_gpu_class(lspci_output)
