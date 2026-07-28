"""test_steps.py — Registry + Step-Dispatch (Chunk 7).

Prüft:
  - STEP_REGISTRY enthält exakt 17 Einträge (1..17)
  - run_step(5, ...) bei ctx.existing_install ruft realmlist-Logik
  - run_step(n) für ungültige n -> ValueError sauber
"""
from __future__ import annotations

from unittest.mock import patch

import pytest

from rising_gods_wizard.actions import Actions
from rising_gods_wizard.addons.ui import NoopUI
from rising_gods_wizard.context import WizardContext
from rising_gods_wizard.steps import STEP_REGISTRY, STEP_TITLES, run_step


def _ctx(existing_install: bool = False) -> WizardContext:
    ctx = WizardContext()
    ctx.existing_install = existing_install
    ctx.dry_run = True
    return ctx


def _fixtures(ctx):
    return ctx, NoopUI(), Actions.build(ctx)


# ── 1) Registry enthält 17 Einträge (1..17) ──────────────────────────────
def test_registry_has_17_steps():
    assert set(STEP_REGISTRY.keys()) == set(range(1, 18))
    assert len(STEP_REGISTRY) == 17
    assert len(STEP_TITLES) == 17


# ── 2) run_step(5) bei existing_install ruft verify_realmlist ────────────
def test_step05_existing_install_calls_realmlist():
    ctx = _ctx(existing_install=True)
    ui, actions = NoopUI(), Actions.build(ctx)
    with patch("rising_gods_wizard.download.client.fetch_client") as mock_fc, patch(
        "rising_gods_wizard.game.realmlist.verify_realmlist"
    ) as mock_vr:
        mock_fc.return_value = "local"
        mock_vr.return_value = "realmlist: OK"
        run_step(5, ctx, ui, actions)
        mock_fc.assert_called_once()
        mock_vr.assert_called_once()
        # erster Argument-Positions-Parameter muss der Context sein
        assert mock_vr.call_args.args[0] is ctx


def test_step05_fresh_install_skips_realmlist():
    ctx = _ctx(existing_install=False)
    ui, actions = NoopUI(), Actions.build(ctx)
    with patch("rising_gods_wizard.download.client.fetch_client") as mock_fc, patch(
        "rising_gods_wizard.game.realmlist.verify_realmlist"
    ) as mock_vr:
        mock_fc.return_value = "local"
        run_step(5, ctx, ui, actions)
        mock_fc.assert_called_once()
        mock_vr.assert_not_called()


# ── 3) ungültige Step-ID -> ValueError ──────────────────────────────────
@pytest.mark.parametrize("bad_n", [0, 18, -1, 99])
def test_run_step_invalid_id_raises(bad_n):
    ctx = _ctx()
    ui, actions = NoopUI(), Actions.build(ctx)
    with pytest.raises(ValueError):
        run_step(bad_n, ctx, ui, actions)
