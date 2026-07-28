"""packages.py — PackageAction: distro-agnostik (apt/dnf/pacman).

Erkennung via `which`. Im Dry-Run nur Plan, keine echte Installation.
"""
from __future__ import annotations

import shutil
import subprocess
from typing import Any

from .interface import ActionProtocol


class PackageAction(ActionProtocol):
    def __init__(self, ctx: Any):
        self.ctx = ctx
        self.manager = self._detect()

    def _detect(self) -> str:
        for mgr, exe in (("apt", "apt-get"), ("dnf", "dnf"), ("pacman", "pacman")):
            if shutil.which(exe):
                return mgr
        return "unknown"

    def describe(self) -> str:
        return f"PackageAction: distro-agnostisch (erkannt: {self.manager})."

    def dry_run_plan(self, pkg: str) -> str:
        return f"[dry-run] würde via {self.manager} installieren: {pkg}"

    def _build_cmd(self, pkg: str) -> str:
        if self.manager == "apt":
            return f"apt-get install -y {pkg}"
        if self.manager == "dnf":
            return f"dnf install -y {pkg}"
        if self.manager == "pacman":
            return f"pacman -S --noconfirm {pkg}"
        raise RuntimeError("Kein unterstützter Paketmanager gefunden.")

    def install(self, pkg: str) -> tuple[int, str, str]:
        if self.ctx.dry_run:
            return (0, self.dry_run_plan(pkg), "")
        proc = subprocess.run(self._build_cmd(pkg), shell=True,
                              capture_output=True, text=True, check=False)
        return (proc.returncode, proc.stdout, proc.stderr)

    def run(self, pkg: str) -> tuple[int, str, str]:
        return self.install(pkg)
