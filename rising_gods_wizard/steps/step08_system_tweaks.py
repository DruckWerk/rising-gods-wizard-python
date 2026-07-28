"""step08_system_tweaks.py — System-Tweaks (ntsync-Gate, vm-tune).

ntsync-Gate (Bug A): nur aktivieren, wenn /dev/ntsync vorhanden.
ctx.ntsync_enabled wird hier persistiert (für Step11 Launcher-Env).
"""
from __future__ import annotations

import logging
from typing import Any

from ..hardware import kernel

log = logging.getLogger(__name__)


def run(ctx: Any, ui: Any, actions: Any) -> None:
    log.info("Step 08: System-Tweaks (ntsync-Gate)")
    dev = kernel.ntsync_device_present()
    ctx.ntsync_enabled = bool(dev)
    if ctx.ntsync_enabled:
        log.info("ntsync-Gerät vorhanden -> ntsync aktiviert")
        actions.shell.run("modprobe ntsync")
    else:
        log.info("Kein /dev/ntsync -> ntsync deaktiviert")
    if ctx.vmtune_enabled:
        actions.shell.run("sysctl -w vm.swappiness=10")
