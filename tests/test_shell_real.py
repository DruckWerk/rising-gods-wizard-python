"""test_shell_real.py — ShellAction führt `echo hi` real aus."""
from __future__ import annotations

from rising_gods_wizard.actions import ShellAction
from rising_gods_wizard.context import WizardContext


def test_shell_echo_real():
    ctx = WizardContext()  # dry_run = False
    s = ShellAction(ctx)
    rc, out, err = s.run("echo hi")
    assert rc == 0
    assert out == "hi\n"
    assert err == ""


def test_shell_forbidden_rejected():
    ctx = WizardContext()
    s = ShellAction(ctx)
    try:
        s.run("rm -rf /")
    except ValueError:
        return
    raise AssertionError("Verbotenes Kommando wurde nicht abgelehnt")
