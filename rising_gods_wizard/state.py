"""state.py — .wizard_state.sh lesen/schreiben (Bash-Parity).

Das Format ist bash-sourceable (export KEY="value"), damit der Wizard-Status
sowohl von Python als auch per `source .wizard_state.sh` von bash gelesen werden
kann. Ermöglicht Resume (Step-Checkpoints) und Parity zum bash-Original.

Hinweis: context.py definiert die Klasse als `WizardContext`; der Auftrag nennt
sie `InstallContext`. Wir exportieren beide Namen (Alias), damit bestehender
Code gegen `InstallContext` bindet, ohne context.py zu ändern.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from . import config
from .context import WizardContext as InstallContext  # Alias (siehe Docstring)


def render(ctx: InstallContext) -> str:
    """Erzeugt bash-sourceable Inhalt aus dem Kontext."""
    install_mode = (
        "existing" if ctx.existing_install else (ctx.client_source or "fresh")
    )
    fields: dict[str, str] = {
        "WOW_DIR": str(ctx.wow_dir),
        "INSTALL_MODE": install_mode,
        "NTSYNC_ENABLED": "true" if ctx.ntsync_enabled else "false",
        "GPU_CLASS": ctx.hw.gpu_vendor,
        "COMMUNITY_TOOLS": ",".join(ctx.community_tools_selected),
        "ADDONS": "true" if ctx.addons_enabled else "false",
        "FPS_PROFILE": ctx.hw.perf_class,
        "REALMLIST_HOST": config.REALMLIST_HOST,
    }
    lines = [
        "# Rising Gods Wizard — auto-generated state file",
        f"# version={config.WIZARD_VERSION}",
        "# Sourceable via: source .wizard_state.sh",
        "",
    ]
    for key, value in fields.items():
        lines.append(f'export {key}="{value}"')
    lines.append("")
    return "\n".join(lines)


def write_state_file(ctx: InstallContext, actions: Any, path: Path | None = None) -> None:
    """Schreibt den State über das Actions-Interface (dry-run-fähig).

    Default-Ziel: ctx.wow_dir / ".wizard_state.sh". `path` erlaubt im Test
    eine abweichende Zieldatei.
    """
    target = path or (ctx.wow_dir / ".wizard_state.sh")
    actions.fs.write(target, render(ctx))


def read_state_file(path: Path | str) -> dict[str, str]:
    """Parst eine bash-sourceable State-Datei zurück in ein dict (Resume)."""
    text = Path(path).read_text(encoding="utf-8")
    result: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        line = line.removeprefix("export ")
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        result[key] = value
    return result
