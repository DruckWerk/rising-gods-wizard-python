"""test_registry.py — registry.py schreibt valide .reg (Tweak-Keys)."""
from __future__ import annotations

from rising_gods_wizard.actions import Actions
from rising_gods_wizard.context import WizardContext
from rising_gods_wizard.wine.registry import (
    REG_TWEAKS,
    build_registry_content,
    write_registry,
)


def test_reg_content_contains_tweaks():
    content = build_registry_content()
    assert content.startswith("REGEDIT4")
    for key in REG_TWEAKS:
        assert f'"{key}"=' in content


def test_reg_content_parseable():
    content = build_registry_content()
    body = [l for l in content.splitlines() if l and not l.startswith("REGEDIT4")]
    kv = [l for l in body if l.startswith('"') and "=" in l]
    assert kv, "keine Key-Value-Zeilen gefunden"
    for line in kv:
        assert line.startswith('"') and line.endswith('"')


def test_write_registry_dry_run(tmp_path):
    ctx = WizardContext(prefix=tmp_path / "prefix")
    ctx.dry_run = True
    actions = Actions.build(ctx)
    write_registry(ctx, actions)
    # dry-run: keine Datei geschrieben
    assert not (ctx.prefix / "rgw-tweaks.reg").exists()


def test_write_registry_real(tmp_path):
    ctx = WizardContext(prefix=tmp_path / "prefix")
    ctx.dry_run = False
    actions = Actions.build(ctx)
    write_registry(ctx, actions)
    reg = ctx.prefix / "rgw-tweaks.reg"
    assert reg.exists()
    assert "csmt" in reg.read_text()
