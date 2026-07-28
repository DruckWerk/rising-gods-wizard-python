"""test_launcher.py — launcher.py baut Command/Skript mit WINENTSYNC-Logik."""
from __future__ import annotations

from rising_gods_wizard.context import HardwareSnapshot, WizardContext
from rising_gods_wizard.wine.launcher import (
    build_launch_command,
    build_launcher_script,
)


def _ctx(ntsync_enabled: bool, dev: bool, kernel=(6, 14, 0), session="x11"):
    return WizardContext(
        ntsync_enabled=ntsync_enabled,
        hw=HardwareSnapshot(
            ntsync_device_present=dev,
            kernel_tuple=kernel,
            session_type=session,
        ),
    )


def test_script_ntsync_enabled():
    ctx = _ctx(True, True)
    script = build_launcher_script(ctx)
    assert "export WINENTSYNC=1" in script
    assert "export WINEARCH=win64" in script
    assert "export WINEPREFIX=" in script
    # Bug A: kein Proton-Only No-Op
    assert "PROTON_USE_NTSYNC" not in script


def test_script_ntsync_disabled():
    ctx = _ctx(False, True)
    script = build_launcher_script(ctx)
    assert "WINENTSYNC" not in script


def test_command_list_has_env():
    ctx = _ctx(True, True)
    cmd = build_launch_command(ctx)
    assert cmd[0] == "env"
    assert any(c.startswith("WINENTSYNC=1") for c in cmd)


def test_script_pure_no_execution_at_build():
    # build_launcher_script ist PURE: kein wine-Aufruf zur Bauzeit
    ctx = _ctx(True, True)
    script = build_launcher_script(ctx)
    assert "exec" in script  # Launcher führt zur Laufzeit aus
    assert "wineboot" not in script  # kein Prefix-Init im Launcher
