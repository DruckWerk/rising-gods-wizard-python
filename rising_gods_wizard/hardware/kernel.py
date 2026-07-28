"""kernel.py — Kernel-Version parsen + ntsync-Gate (PURE).

ntsync-Gate-Modell (Spec §5 Bug A):
  - Hard-Gate (autoritativ): /dev/ntsync existiert -> ntsync_device_present()
  - Kernel-Version ist NUR advisory für die Wine-Seite (config.MIN_NTSYNC_KERNEL)
  - Kernel-seitig landed der ntsync-Char-Treiber in Linux 6.6 (CONFIG_NTSYNC).
    Daher gilt hier das Kernel-Gate 6.6+ für ntsync_supported().
"""
from __future__ import annotations

import os
import re

from .. import config

# Kernel-seitige ntsync-Verfügbarkeit: ntsync-Treiber landed in Linux 6.6.
# (config.MIN_NTSYNC_KERNEL=(6,14,0) ist NUR advisory für die Wine-Userland-Seite.)
NTSYNC_KERNEL_MIN: tuple[int, int, int] = (6, 6, 0)


def parse_kernel(uname: str) -> tuple[int, int, int]:
    """PURE: parst 'Linux 6.6.0-1-amd64' -> (6, 6, 0)."""
    m = re.search(r"\b(\d+)\.(\d+)(?:\.(\d+))?", uname)
    if not m:
        return (0, 0, 0)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3) or 0))


def ntsync_supported(kernel_tuple: tuple[int, int, int]) -> bool:
    """PURE helper: Kernel-seitig ntsync verfügbar? (6.6+)."""
    return bool(kernel_tuple >= NTSYNC_KERNEL_MIN)


def ntsync_device_present() -> bool:
    """Hard-Gate: /dev/ntsync autoritativ (Side-Effect: FS-Stat)."""
    return os.path.exists(config.NTSYNC_DEVICE)
