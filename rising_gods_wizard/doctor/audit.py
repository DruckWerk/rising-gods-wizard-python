"""audit.py — read-only System-Prüfung (Doctor audit).

Sammelt Befunde zu Prefix, GPU, Kernel/ntsync, realmlist (read-only!) und
Community-Tools-Integrität. KEINE Side-Effects: realmlist wird nur über die
read-only Helfer (detect_realmlist_path/needs_correction) geprüft.

Liefert ein dict: {"ok": bool, "findings": [ {component,status,detail}, ... ]}.
"""
from __future__ import annotations

import os
from typing import Any

from .. import config
from ..context import WizardContext
from ..game.realmlist import detect_realmlist_path, needs_correction
from ..hardware.kernel import ntsync_device_present, parse_kernel


def _finding(component: str, status: str, detail: str) -> dict[Any, Any]:
    return {"component": component, "status": status, "detail": detail}


def audit(ctx: WizardContext, actions: Any = None) -> dict[Any, Any]:
    """Read-only Audit. `actions` wird NICHT geschrieben (nur gelesen/ignoriert)."""
    findings: list[dict[Any, Any]] = []

    # Prefix
    if ctx.prefix.exists():
        findings.append(_finding("prefix", "ok", str(ctx.prefix)))
    else:
        findings.append(_finding("prefix", "missing", str(ctx.prefix)))

    # GPU (Snapshot aus ctx.hw; unverändert)
    findings.append(_finding(
        "gpu", "ok" if ctx.hw.gpu_vendor != "unknown" else "warning",
        f"{ctx.hw.gpu_vendor} ({ctx.hw.perf_class})",
    ))

    # Kernel + ntsync
    kt = parse_kernel(os.uname().release)
    dev = ntsync_device_present()
    if kt >= config.MIN_NTSYNC_KERNEL:
        findings.append(_finding("kernel", "ok", f"{kt} >= {config.MIN_NTSYNC_KERNEL}"))
    else:
        findings.append(_finding(
            "kernel", "warning",
            f"{kt} < advisory {config.MIN_NTSYNC_KERNEL}",
        ))
    if dev:
        findings.append(_finding("ntsync", "ok", f"{config.NTSYNC_DEVICE} present"))
    else:
        findings.append(_finding("ntsync", "missing", f"{config.NTSYNC_DEVICE} absent"))

    # Realmlist (READ-ONLY: keine Korrektur hier!)
    rpath = detect_realmlist_path(ctx)
    if needs_correction(rpath):
        findings.append(_finding("realmlist", "error",
                                 "falsch/fehlend (repair empfohlen)"))
    else:
        findings.append(_finding("realmlist", "ok", str(rpath)))

    # Community-Tools-Integrität (Dateien vorhanden?)
    for tool in config.COMMUNITY_SOURCES:
        dest = ctx.addons_dir / config.COMMUNITY_SOURCES[tool].get("dest_subdir", "")
        present = dest.exists()
        findings.append(_finding(
            "community", "ok" if present else "missing", f"{tool}: {dest}",
        ))

    ok = all(f["status"] in ("ok", "warning") for f in findings)
    return {"ok": ok, "findings": findings}
