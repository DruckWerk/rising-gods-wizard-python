"""test_doctor_audit.py — audit liefert Befund-dict OHNE Side-Effects.

Monkeypatch: echte FSAction durch Stub ersetzen; realmlist read-only prüfen.
"""
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from rising_gods_wizard.context import WizardContext
from rising_gods_wizard.doctor import audit


class _NoopActions:
    """Stub: wirft bei jedem Schreib-Versuch (audit darf nicht schreiben)."""

    class _Fs:
        def write(self, *a, **k):
            raise AssertionError("audit hat geschrieben!")

        def mkdir(self, *a, **k):
            raise AssertionError("audit hat geschrieben!")

    fs = _Fs()


@pytest.fixture
def ctx(tmp_path):
    c = WizardContext(
        wow_dir=tmp_path / "wow",
        prefix=tmp_path / "wow" / "prefix",
        state_file=tmp_path / "wow" / ".wizard_state.sh",
        existing_install=True,
    )
    # Prefix anlegen (damit audit 'prefix ok' meldet)
    c.prefix.mkdir(parents=True, exist_ok=True)
    # realmlist korrekt anlegen (read-only Pfad)
    rl = c.data_dir / "enGB" / "realmlist.wtf"
    rl.parent.mkdir(parents=True, exist_ok=True)
    rl.write_text('set realmlist "login.rising-gods.de"\n')
    return c


def test_audit_returns_dict(ctx):
    result = audit.audit(ctx, _NoopActions())
    assert isinstance(result, dict)
    assert "ok" in result and "findings" in result
    assert isinstance(result["findings"], list)
    assert len(result["findings"]) > 0


def test_audit_no_side_effects(ctx):
    # darf nicht crashen und nichts schreiben
    result = audit.audit(ctx, _NoopActions())
    comps = {f["component"] for f in result["findings"]}
    assert {"prefix", "gpu", "kernel", "ntsync", "realmlist"}.issubset(comps)


def test_audit_realmlist_readonly_ok(ctx):
    result = audit.audit(ctx, _NoopActions())
    rl = [f for f in result["findings"] if f["component"] == "realmlist"][0]
    assert rl["status"] == "ok"
