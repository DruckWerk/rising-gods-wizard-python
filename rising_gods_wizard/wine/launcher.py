"""launcher.py — start-wow.sh Generierung + ntsync-Env (Bug A Fix).

PURE Gen: build_launcher_script(ctx) liefert den Shell-Skript-Inhalt.
compute_ntodusync_env() ist das autoritative Wahrheitszentrum für ntsync
(siehe Spec §5 Bug A): bei plain Wine MUSS WINENTSYNC=1 gesetzt werden,
PROTON_USE_NTSYNC=1 ist ein No-Op und wird NICHT verwendet.
"""
from __future__ import annotations

import logging

from .. import config
from ..context import WizardContext
from .audio import compute_audio_env

log = logging.getLogger(__name__)


def compute_ntsync_env(
    enabled: bool,
    dev_ntsync_exists: bool,
    kernel_tuple: tuple[int, int, int],
) -> dict[str, str]:
    """BUG A: korrekte ntsync-Env für plain Wine.

    User-Choice (enabled) UND Hard-Gate (dev_ntsync_exists) müssen beide
    gelten. Liefert {} wenn abgewählt oder kein /dev/ntsync-Device.
    Setzt WINENTSYNC=1 (moderne Wine ntsync) + Fallback WINEFSYNC/WINEESYNC.
    PROTON_USE_NTSYNC wird NICHT gesetzt (Proton-only, No-Op bei plain wine).
    """
    if not enabled or not dev_ntsync_exists:
        return {}
    if kernel_tuple < config.MIN_NTSYNC_KERNEL:
        log.warning(
            "ntsync: /dev/ntsync vorhanden, aber Kernel %s < advisory %s — "
            "ntsync dennoch aktiviert (Distro-Backport möglich)",
            kernel_tuple, config.MIN_NTSYNC_KERNEL,
        )
    env = {"WINENTSYNC": "1"}
    env["WINEFSYNC"] = "1"
    env["WINEESYNC"] = "1"
    return env


def build_launcher_env(ctx: WizardContext) -> dict[str, str]:
    """PURE: sammelt alle Env-Vars für den Launcher (WINEARCH, Prefix, ntsync, Audio, Game)."""
    env: dict[str, str] = {
        "WINEARCH": "win64",
        "WINEPREFIX": str(ctx.prefix),
        "WOW_DIR": str(ctx.wow_dir),
        "GAME": str(ctx.wow_dir / "Wow.exe"),
        "LUTRIS_GAME_PATH": str(ctx.wow_dir),
    }
    env.update(
        compute_ntsync_env(
            ctx.ntsync_enabled,
            ctx.hw.ntsync_device_present,
            ctx.hw.kernel_tuple,
        )
    )
    env.update(compute_audio_env(ctx))
    return env


def build_launcher_script(ctx: WizardContext) -> str:
    """PURE: baut den Inhalt von start-wow.sh (Shell-Skript)."""
    env = build_launcher_env(ctx)
    lines = [
        "#!/usr/bin/env bash",
        "# Rising Gods Wizard — WoW 3.3.5a Launcher (auto-generiert)",
        "set -euo pipefail",
        "",
    ]
    for k, v in env.items():
        lines.append(f"export {k}={v}")

    wine = ctx.wine_cmd
    if ctx.use_gamemode:
        wine = f"gamemoderun {wine}"
    lines += [
        "",
        f'exec env WINEPREFIX="$WINEPREFIX" {wine} "$GAME" "$@"',
        "",
    ]
    return "\n".join(lines)


def build_launch_command(ctx: WizardContext) -> list[str]:
    """PURE: liefert die Ausführungs-Command-Liste (env-Präfix + wine-Aufruf)."""
    env = build_launcher_env(ctx)
    cmd = ["env"]
    for k, v in env.items():
        cmd.append(f"{k}={v}")
    wine = ctx.wine_cmd
    if ctx.use_gamemode:
        wine = f"gamemoderun {wine}"
    cmd += [wine, str(ctx.wow_dir / "Wow.exe")]
    return cmd
