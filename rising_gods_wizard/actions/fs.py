"""fs.py — FSAction: mkdir/write/copy/chmod (dry-run-sicher).

Im Dry-Run werden keine echten FS-Seiteneffekte erzeugt.
"""
from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from .interface import ActionProtocol


class FSAction(ActionProtocol):
    def __init__(self, ctx: Any):
        self.ctx = ctx

    def describe(self) -> str:
        return "FSAction: mkdir/write/copy/chmod — dry-run-sicher."

    def dry_run_plan(self, op: str, target: str) -> str:
        return f"[dry-run] würde FS-Op '{op}' auf: {target}"

    def mkdir(self, path: Path | str, mode: int = 0o755) -> None:
        p = Path(path)
        if self.ctx.dry_run:
            return
        p.mkdir(parents=True, exist_ok=True)
        p.chmod(mode)

    def write(self, path: Path | str, content: str) -> None:
        p = Path(path)
        if self.ctx.dry_run:
            return
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

    def copy(self, src: Path | str, dst: Path | str) -> None:
        if self.ctx.dry_run:
            return
        d = Path(dst)
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    def chmod(self, path: Path | str, mode: int) -> None:
        if self.ctx.dry_run:
            return
        Path(path).chmod(mode)

    def run(self, op: str, *args: Any) -> None:
        """Generischer Dispatch; konkrete Methoden (write/mkdir/...) vorziehen."""
        getattr(self, op)(*args)
