"""test_download_order.py — client.fetch_client wählt lokal->torrent->http.

OHNE echtes Netz: actions.shell.run per monkeypatch ersetzt, damit wir nur
die Reihenfolge-Logik prüfen.
"""
from __future__ import annotations

from pathlib import Path

from rising_gods_wizard.context import WizardContext
from rising_gods_wizard.download import client
from rising_gods_wizard.addons.ui import NoopUI


class _MockActions:
    """Shell-Run, das Reihenfolge erzwingt: curl/torrent rc=0."""

    def __init__(self):
        self.calls = []

    class _Shell:
        def __init__(self, parent):
            self._p = parent

        def run(self, command):
            self._p.calls.append(command)
            return (0, "ok", "")

    def __init__(self):
        self.calls = []
        self.shell = self._Shell(self)


def _ctx() -> WizardContext:
    return WizardContext()


def test_local_preferred(tmp_path):
    ctx = _ctx()
    local = tmp_path / "wow_local"
    local.mkdir()
    ctx.local_client_path = str(local)
    acts = _MockActions()
    src = client.fetch_client(ctx, acts, NoopUI())
    assert src == "local"
    assert ctx.client_source == "local"
    assert acts.calls == [], "Bei lokal darf kein shell.run erfolgen"


def test_torrent_before_http(tmp_path):
    ctx = _ctx()
    ctx.torrent_url = "magnet:?xt=urn:btih:abc"
    ctx.http_url = "http://example.com/wow.zip"
    acts = _MockActions()
    src = client.fetch_client(ctx, acts, NoopUI())
    assert src == "torrent"
    assert any("transmission-cli" in c for c in acts.calls)
    assert not any("curl" in c for c in acts.calls)


def test_http_fallback_only(tmp_path):
    ctx = _ctx()
    ctx.http_url = "http://example.com/wow.zip"
    acts = _MockActions()
    src = client.fetch_client(ctx, acts, NoopUI())
    assert src == "http"
    assert any("curl" in c for c in acts.calls)


def test_no_source_raises(tmp_path):
    ctx = _ctx()
    acts = _MockActions()
    import pytest
    with pytest.raises(RuntimeError):
        client.fetch_client(ctx, acts, NoopUI())
