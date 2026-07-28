"""lutris_export.py — rising-gods-lutris.yaml Generator (PURE GEN).

Erzeugt eine Lutris-Import-YAML mit Game-Eintrag (exe = start-wow.sh) und
Dual-Source-of-Truth-Schutz: `wizard_managed: true` + Prefix "nothing/disabled",
damit Lutris den Wizard-Prefix NICHT selbst verwaltet/überschreibt.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ..context import WizardContext

LUTRIS_FILENAME = "rising-gods-lutris.yaml"


def build_lutris_yaml(ctx: WizardContext) -> str:
    """PURE: erzeugt die vollständige Lutris-Import-YAML als String."""
    exe = ctx.launcher_path
    prefix = ctx.prefix
    return (
        "# ============================================================\n"
        "# Rising Gods •Linux• InstallWizard — Lutris-Import\n"
        "# wizard_managed: true  (NICHT manuell bearbeiten — Wizard-owned)\n"
        "# Prefix-Handling: nothing/disabled (Lutris verwaltet den\n"
        "#   Wizard-Prefix nicht selbst, um Überschreibungen zu vermeiden).\n"
        "# ============================================================\n"
        f"wizard_managed: true\n"
        "game:\n"
        f"  name: Rising Gods •Linux• InstallWizard\n"
        f"  exe: {exe}\n"
        f"  prefix: {prefix}\n"
        "  runner: wine\n"
        "  working_dir: ''\n"
        "wine:\n"
        "  version: lutris-ge-latest\n"
        "  prefix_command: ''\n"
        "system:\n"
        "  game_mode: true\n"
        "  dxvk: true\n"
        "  fsync: true\n"
        "  # wizard_managed-Schutz: Prefix NICHT von Lutris verwalten\n"
        "  prefix:\n"
        "    nothing: true\n"
        "    disabled: true\n"
    )


def write_lutris_yaml(ctx: WizardContext, actions: Any) -> Path:
    """Schreibt rising-gods-lutris.yaml neben den Launcher (dry-run-sicher)."""
    target = ctx.wow_dir / LUTRIS_FILENAME
    actions.fs.write(target, build_lutris_yaml(ctx))
    return target
