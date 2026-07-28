"""step07_gpu.py — GPU Auto-Detection."""
from __future__ import annotations

import logging
from typing import Any

from ..hardware import gpu

log = logging.getLogger(__name__)


def run(ctx: Any, ui: Any, actions: Any) -> None:
    log.info("Step 07: GPU Auto-Detection")
    gpu.detect_gpu(ctx, actions)
    log.info("GPU erkannt: vendor=%s class=%s", ctx.hw.gpu_vendor, ctx.hw.perf_class)
