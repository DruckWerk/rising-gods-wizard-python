"""step01_preflight.py — Pre-Flight Requirements-Check + Hardware-Snapshot.

Erfasst den Hardware-Snapshot (gpu/session/kernel/ntsync-Gate) via
hardware/* PURE-Module. Logik liegt in hardware/*.
"""
from __future__ import annotations

import logging
import os
from typing import Any

from ..hardware import gpu, kernel, session

log = logging.getLogger(__name__)


def run(ctx: Any, ui: Any, actions: Any) -> None:
    log.info("Step 01: Pre-Flight & Hardware-Erkennung")
    ctx.hw.session_type = session.detect_session_type(ctx.extra.get("environ"))
    ctx.hw.kernel_tuple = kernel.parse_kernel(os.uname().release)
    ctx.hw.ntsync_device_present = kernel.ntsync_device_present()
    gpu.detect_gpu(ctx, actions)
    log.info(
        "Pre-Flight OK: vendor=%s class=%s session=%s ntsync=%s",
        ctx.hw.gpu_vendor,
        ctx.hw.perf_class,
        ctx.hw.session_type,
        ctx.hw.ntsync_device_present,
    )
