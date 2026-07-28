"""step17_finish.py — Fertig-State + write_state_file (.wizard_state.sh)."""
from __future__ import annotations

import logging
from typing import Any

from .. import state

log = logging.getLogger(__name__)


def run(ctx: Any, ui: Any, actions: Any) -> None:
    log.info("Step 17: Abschluss + State-Datei")
    state.write_state_file(ctx, actions)
    log.info("Wizard abgeschlossen; State: %s", ctx.state_file)
