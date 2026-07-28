"""test_realmlist.py — Feature 5: realmlist.wtf-Verifikation (4 Zweige)."""
from __future__ import annotations

from pathlib import Path

from rising_gods_wizard import config
from rising_gods_wizard.actions import Actions
from rising_gods_wizard.context import WizardContext
from rising_gods_wizard.game import realmlist


def _ctx(wow_dir: Path, dry_run: bool = False) -> WizardContext:
    ctx = WizardContext(wow_dir=wow_dir)
    ctx.existing_install = True
    ctx.dry_run = dry_run
    return ctx


def _write(tmp_path: Path, locale: str, content: str) -> Path:
    p = tmp_path / "wow" / "Data" / locale / "realmlist.wtf"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return p


# (1) korrekter realmlist -> keine Änderung
def test_correct_realmlist_no_change(tmp_path):
    p = _write(tmp_path, "deDE", f'set realmlist "{config.REALMLIST_HOST}"\n')
    ctx = _ctx(tmp_path / "wow")
    actions = Actions.build(ctx)
    before = p.read_text()
    msg = realmlist.verify_realmlist(ctx, None, actions)
    assert "OK" in msg
    assert p.read_text() == before
    assert not (tmp_path / "wow" / "Data" / "deDE" / "realmlist.wtf.bak").exists()


# (2) falscher host -> Korrektur MIT Backup geschrieben
def test_wrong_host_corrected_with_backup(tmp_path):
    p = _write(tmp_path, "enUS", 'set realmlist "wrong.example.com"\n')
    ctx = _ctx(tmp_path / "wow")
    actions = Actions.build(ctx)
    msg = realmlist.verify_realmlist(ctx, None, actions)
    assert "geschrieben" in msg
    assert p.read_text().strip() == f'set realmlist "{config.REALMLIST_HOST}"'
    assert (tmp_path / "wow" / "Data" / "enUS" / "realmlist.wtf.bak").exists()
    bak = (tmp_path / "wow" / "Data" / "enUS" / "realmlist.wtf.bak").read_text()
    assert "wrong.example.com" in bak


# (3) fehlend -> wird erzeugt (erste Locale enGB)
def test_missing_realmlist_created(tmp_path):
    ctx = _ctx(tmp_path / "wow")
    actions = Actions.build(ctx)
    msg = realmlist.verify_realmlist(ctx, None, actions)
    assert "erzeugt" in msg
    target = tmp_path / "wow" / "Data" / config.REALMLIST_LOCALES[0] / "realmlist.wtf"
    assert target.exists()
    assert target.read_text().strip() == f'set realmlist "{config.REALMLIST_HOST}"'


# (4) dry-run -> keine Dateiänderung, Aktion protokolliert
def test_dry_run_no_write(tmp_path):
    p = _write(tmp_path, "enGB", 'set realmlist "stale.host"\n')
    ctx = _ctx(tmp_path / "wow", dry_run=True)
    actions = Actions.build(ctx)
    before = p.read_text()
    msg = realmlist.verify_realmlist(ctx, None, actions)
    assert p.read_text() == before  # unverändert
    assert "dry-run" in msg.lower() or "protokolliert" in msg
