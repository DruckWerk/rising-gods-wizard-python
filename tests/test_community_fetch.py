"""test_community_fetch.py — Feature 4: Mock-Download, Checksum-Claim, Offline.

OHNE echtes Netz: actions.shell.run wird per Mock ersetzt. Der Mock legt die
Zieldatei (aus dem curl -o Argument) an, damit verify_file real prüfen kann.
Prüft: (1) Erfolg + Ablage, (2) version_pin+checksum -> verify (match/ mismatch),
(3) Offline -> harte Exception, KEIN silently-continue.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

import pytest

from rising_gods_wizard.context import WizardContext
from rising_gods_wizard.addons import community_fetch
from rising_gods_wizard.addons.ui import NoopUI


# Der Mock schreibt dieses feste Payload; Hash wird im Test dynamisch erzeugt.
_MOCK_PAYLOAD = b"rising-gods-community-tool-bundle"


class _MockActions:
    """Simuliert actions: curl -o <pfad> legt _MOCK_PAYLOAD an; rc=0."""

    def __init__(self, fail=False):
        self.calls: list[str] = []
        self.fail = fail

    class _Shell:
        def __init__(self, parent):
            self._p = parent

        def run(self, command: str):
            self._p.calls.append(command)
            if self._p.fail:
                return (1, "", "curl: (6) Could not resolve host")
            m = re.search(r"-o\s+(\S+)", command)
            if m:
                p = Path(m.group(1))
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(_MOCK_PAYLOAD)
            return (0, "ok", "")

    @property
    def shell(self):
        return self._Shell(self)


def _ctx(tmp_path: Path, tools=None) -> WizardContext:
    ctx = WizardContext()
    ctx.wow_dir = tmp_path
    ctx.community_tools_selected = tools or ["luaboost"]
    return ctx


def test_fetch_success_mocks_download(tmp_path):
    ctx = _ctx(tmp_path, ["luaboost"])
    acts = _MockActions(fail=False)
    out = community_fetch.fetch_community_tools(ctx, NoopUI(), acts)
    assert out, "Erwartet mindestens einen abgelegten Pfad"
    assert Path(out[0]).name == "luaboost.dl"
    assert Path(out[0]).exists()


def test_checksum_claim_verifies(tmp_path):
    # version_pin + korrekter checksum -> verify_file bestätigt (Match).
    from rising_gods_wizard import config
    ctx = _ctx(tmp_path, ["luaboost"])
    good = hashlib.sha256(_MOCK_PAYLOAD).hexdigest()
    config.COMMUNITY_SOURCES["luaboost"]["version_pin"] = "test"
    config.COMMUNITY_SOURCES["luaboost"]["checksum"] = good
    acts = _MockActions(fail=False)
    out = community_fetch.fetch_community_tools(ctx, NoopUI(), acts)
    assert out
    config.COMMUNITY_SOURCES["luaboost"]["version_pin"] = ""
    config.COMMUNITY_SOURCES["luaboost"]["checksum"] = ""


def test_checksum_mismatch_raises(tmp_path):
    from rising_gods_wizard import config
    ctx = _ctx(tmp_path, ["luaboost"])
    config.COMMUNITY_SOURCES["luaboost"]["version_pin"] = "test"
    config.COMMUNITY_SOURCES["luaboost"]["checksum"] = "deadbeef" * 8
    acts = _MockActions(fail=False)
    with pytest.raises(ValueError):
        community_fetch.fetch_community_tools(ctx, NoopUI(), acts)
    config.COMMUNITY_SOURCES["luaboost"]["version_pin"] = ""
    config.COMMUNITY_SOURCES["luaboost"]["checksum"] = ""


def test_offline_is_hard_error(tmp_path):
    ctx = _ctx(tmp_path, ["luaboost"])
    acts = _MockActions(fail=True)  # curl rc=1 -> Offline
    with pytest.raises(RuntimeError):
        community_fetch.fetch_community_tools(ctx, NoopUI(), acts)
