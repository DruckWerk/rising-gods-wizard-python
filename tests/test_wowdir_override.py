"""test_wowdir_override.py — Bug-Fix: --wow-dir Override (V1 DoD-Verstoß).

Prüft, dass ein gesetztes ``wow_dir`` die abgeleiteten Pfade
``prefix`` / ``state_file`` / ``launcher_path`` mitzieht.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from rising_gods_wizard.context import WizardContext
from rising_gods_wizard.__main__ import _build_context


def test_derive_paths_explicit_wow_dir() -> None:
    """WizardContext(wow_dir=...)._derive_paths() leitet relativ ab."""
    c = WizardContext(wow_dir=Path("/tmp/foo"))
    c._derive_paths()
    assert c.prefix == Path("/tmp/foo/prefix")
    assert c.state_file == Path("/tmp/foo/.wizard_state.sh")
    assert c.launcher_path == Path("/tmp/foo/start-wow.sh")


def test_cli_wow_dir_override() -> None:
    """CLI-Simulation via _build_context: alle Pfade unter dem Override."""
    args = argparse.Namespace(
        dry_run=True,
        wow_dir="/tmp/rg-x",
        locale="enUS",
        step=None,
        doctor=None,
        ui="null",
    )
    ctx = _build_context(args)
    assert ctx.wow_dir == Path("/tmp/rg-x").expanduser()
    # Alle drei abgeleiteten Pfade müssen unter dem Override liegen.
    assert ctx.prefix == Path("/tmp/rg-x/prefix")
    assert ctx.state_file == Path("/tmp/rg-x/.wizard_state.sh")
    assert ctx.launcher_path == Path("/tmp/rg-x/start-wow.sh")
    # Und NICHT mehr auf dem Default.
    assert "Games/wow335" not in str(ctx.prefix)
    assert "Games/wow335" not in str(ctx.state_file)
    assert "Games/wow335" not in str(ctx.launcher_path)


def test_cli_no_override_uses_default() -> None:
    """Ohne --wow-dir bleiben die Default-Pfade erhalten."""
    args = argparse.Namespace(
        dry_run=False,
        wow_dir=None,
        locale="enUS",
        step=None,
        doctor=None,
        ui=None,
    )
    ctx = _build_context(args)
    # Default-Default aus config.
    assert ctx.prefix == ctx.wow_dir / "prefix"
    assert ctx.state_file == ctx.wow_dir / ".wizard_state.sh"
    assert ctx.launcher_path == ctx.wow_dir / "start-wow.sh"


def test_step17_dry_run_writes_state_to_overridden_path() -> None:
    """Optional: run_step(17) im dry-run nutzt den überschriebenen state_file."""
    from rising_gods_wizard.actions import Actions
    from rising_gods_wizard.steps import registry as steps_registry
    from rising_gods_wizard.ui.null_ui import NullUI

    args = argparse.Namespace(
        dry_run=True,
        wow_dir="/tmp/rg-step17",
        locale="enUS",
        step=None,
        doctor=None,
        ui="null",
    )
    ctx = _build_context(args)
    ui = NullUI()
    actions = Actions.build(ctx)

    # Step 17 (Abschluss + State) darf im dry-run nicht crashen und muss
    # den überschriebenen state_file-Pfad verwenden.
    steps_registry.run_step(17, ctx, ui, actions)
    assert ctx.state_file == Path("/tmp/rg-step17/.wizard_state.sh")
