"""test_actions_dryrun.py — Dry-Run erzeugt KEINE Seiteneffekte, liefert Plan."""
from __future__ import annotations

from pathlib import Path

from rising_gods_wizard.actions import ShellAction, FSAction, PackageAction
from rising_gods_wizard.context import WizardContext


def _ctx(tmp_path: Path) -> WizardContext:
    ctx = WizardContext()
    ctx.dry_run = True
    ctx.state_file = tmp_path / ".wizard_state.sh"
    return ctx


def test_shell_dryrun_no_exec(tmp_path):
    ctx = _ctx(tmp_path)
    s = ShellAction(ctx)
    rc, out, err = s.run("echo hi")
    assert rc == 0
    assert "würde ausführen" in out
    assert out == s.dry_run_plan("echo hi")


def test_fs_dryrun_no_write(tmp_path):
    ctx = _ctx(tmp_path)
    f = FSAction(ctx)
    target = tmp_path / "nope" / "out.txt"
    f.write(target, "geheim")
    assert not target.exists(), "Dry-Run darf kein File schreiben"


def test_packages_dryrun_no_install(tmp_path):
    ctx = _ctx(tmp_path)
    p = PackageAction(ctx)
    rc, out, err = p.install("wine")
    assert rc == 0
    assert "würde" in out and "wine" in out
    assert err == ""


def test_describe_readable(tmp_path):
    ctx = _ctx(tmp_path)
    for a in (ShellAction(ctx), FSAction(ctx), PackageAction(ctx)):
        assert a.describe().strip()
