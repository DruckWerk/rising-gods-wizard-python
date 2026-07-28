"""config.py — dxvk.conf Generierung (GPU-spezifisch, PURE + Action).

PURE: build_dxvk_conf(ctx) -> str
Action: write_dxvk_conf(ctx, actions) schreibt via actions.fs.
"""
from __future__ import annotations

from typing import Any

from ..context import WizardContext


def build_dxvk_conf(ctx: WizardContext) -> str:
    """PURE: erzeugt dxvk.conf-Inhalt abhängig von GPU-Vendor/Perf-Class."""
    vendor = ctx.hw.gpu_vendor
    cls = ctx.hw.perf_class
    lines = [
        "# dxvk.conf — auto-generiert durch Rising Gods Wizard",
        "dxvk.hud = version",
    ]
    # GPU-spezifische Tweaks (nvapi nur bei NVIDIA sinnvoll)
    if vendor == "nvidia":
        lines.append("dxvk.nvapi = True")
        lines.append("dxvk.nvapiHud = False")
    else:
        lines.append("dxvk.nvapi = False")
    # Perf-Class -> zulässiger Video-Speicher-Hint
    if cls in ("high", "ultra"):
        lines.append("dxvk.maxMemory = 16384")
    elif cls in ("mid", "low"):
        lines.append("dxvk.maxMemory = 8192")
    else:
        lines.append("dxvk.maxMemory = 4096")
    lines.append("")  # trailing newline
    return "\n".join(lines) + "\n"


def write_dxvk_conf(ctx: WizardContext, actions: Any) -> None:
    """Schreibt dxvk.conf via actions.fs (dry-run-sicher)."""
    content = build_dxvk_conf(ctx)
    actions.fs.write(ctx.dxvk_conf_path, content)
