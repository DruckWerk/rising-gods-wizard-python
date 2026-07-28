"""test_fs_write.py — FSAction.write schreibt echtes File (nicht dry-run)."""
from __future__ import annotations

from pathlib import Path

from rising_gods_wizard.actions import FSAction
from rising_gods_wizard.context import WizardContext


def test_fs_write_real(tmp_path):
    ctx = WizardContext()  # dry_run = False
    f = FSAction(ctx)
    target = tmp_path / "sub" / "Config.wtf"
    content = "SET gxResolution \"1920x1080\"\n"
    f.write(target, content)
    assert target.exists(), "File muss echterweise geschrieben sein"
    assert target.read_text(encoding="utf-8") == content


def test_fs_mkdir_real(tmp_path):
    ctx = WizardContext()
    f = FSAction(ctx)
    d = tmp_path / "prefix" / "drive_c"
    f.mkdir(d)
    assert d.is_dir()
