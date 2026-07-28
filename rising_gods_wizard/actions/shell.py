"""shell.py — ShellAction: führt Kommandos aus (dry-run-sicher).

Sicherheit via Allowlist: nur erlaubte Präfixe werden ausgeführt, gefährliche
Muster sind immer verboten. Im Dry-Run wird nicht exec'd, nur protokolliert.
"""
from __future__ import annotations

import subprocess
from typing import Any

from .interface import ActionProtocol

# Nur diese Präfixe sind erlaubt. Erweiterbar für künftige Wizard-Schritte.
ALLOWED_PREFIXES = (
    "echo", "printf", "mkdir", "cp", "ln", "cat", "test", "ls",
    "wine", "gamemoderun", "env", "python", "python3", "chmod", "touch",
    "tee", "true", "false",
    # Download / Entpacken (Chunk 6: download/ + addons/)
    "curl", "wget", "transmission-cli", "transmission-remote",
    "7z", "unzip", "tar",
    # System-Tweaks / Hardware-Erkennung (Step02/08, hardware/*)
    "modprobe", "sysctl", "lspci", "sha256sum",
    # Env-Export (Step10 dxvk_audio u.a.) — nur Variable setzen, kein Exec-Risiko
    "export",
)
# Gefährliche Muster — immer verboten, unabhängig von der Allowlist.
FORBIDDEN_PATTERNS = (
    "rm -rf /", "mkfs", "dd if=", "dd of=", "shutdown", "reboot",
    ">: /dev/", "chmod -R 777 /",
)


class ShellAction(ActionProtocol):
    def __init__(self, ctx: Any):
        self.ctx = ctx

    def _check(self, command: str) -> None:
        cmd = command.strip()
        for pat in FORBIDDEN_PATTERNS:
            if pat in cmd:
                raise ValueError(f"Verbotenes Kommando abgelehnt: {command!r}")
        head = cmd.split(None, 1)[0] if cmd else ""
        if head not in ALLOWED_PREFIXES:
            raise ValueError(f"Nicht erlaubtes Kommando-Präfix: {head!r}")

    def describe(self) -> str:
        return "ShellAction: führt erlaubte Shell-Kommandos aus (dry-run-sicher)."

    def dry_run_plan(self, command: str) -> str:
        return f"[dry-run] würde ausführen: {command}"

    def run(self, command: str) -> tuple[int, str, str]:
        """Führt `command` aus. Dry-Run: nur Plan, rc=0, leere Ausgaben."""
        self._check(command)
        if self.ctx.dry_run:
            return (0, self.dry_run_plan(command), "")
        proc = subprocess.run(command, shell=True, capture_output=True,
                               text=True, check=False)
        return (proc.returncode, proc.stdout, proc.stderr)
