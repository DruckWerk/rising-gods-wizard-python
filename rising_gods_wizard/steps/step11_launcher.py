"""step11_launcher.py — Launcher-Script-Generierung (start-wow.sh) [Bug A].

Nutzt wine/launcher.build_launcher_script() (PURE) -> actions.fs.write.
ntsync-Env kommt aus compute_ntsync_env (Bug A Fix).
"""
from __future__ import annotations

import logging
from typing import Any

from ..wine import launcher

log = logging.getLogger(__name__)


def run(ctx: Any, ui: Any, actions: Any) -> None:
    log.info("Step 11: Launcher-Script generieren")
    script = launcher.build_launcher_script(ctx)
    actions.fs.write(ctx.launcher_path, script)
    log.info("Launcher geschrieben: %s", ctx.launcher_path)
