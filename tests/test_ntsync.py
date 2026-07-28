"""test_ntsync.py — compute_ntsync_env() 4+1 Zweige (Bug A)."""
from __future__ import annotations

import logging

from rising_gods_wizard import config
from rising_gods_wizard.wine.launcher import compute_ntsync_env


def test_enabled_dev_present_full_env():
    env = compute_ntsync_env(True, True, config.MIN_NTSYNC_KERNEL)
    assert env.get("WINENTSYNC") == "1"
    assert env.get("WINEFSYNC") == "1"
    assert env.get("WINEESYNC") == "1"
    # Bug A: PROTON_USE_NTSYNC darf NICHT gesetzt sein (Proton-only No-Op)
    assert "PROTON_USE_NTSYNC" not in env


def test_enabled_no_dev_empty():
    # Hard-Gate: kein /dev/ntsync → keine ntsync-Env
    env = compute_ntsync_env(True, False, config.MIN_NTSYNC_KERNEL)
    assert env == {}


def test_disabled_dev_present_empty():
    # User-Choice: abgewählt → keine ntsync-Env
    env = compute_ntsync_env(False, True, config.MIN_NTSYNC_KERNEL)
    assert env == {}


def test_disabled_no_dev_empty():
    env = compute_ntsync_env(False, False, config.MIN_NTSYNC_KERNEL)
    assert env == {}


def test_kernel_advisory_warns_but_activates(caplog):
    # enabled + dev da, aber Kernel advisory drunter → volle env + Warn-Log
    with caplog.at_level(logging.WARNING):
        env = compute_ntsync_env(True, True, (6, 13, 0))
    assert env.get("WINENTSYNC") == "1"
    assert any("ntsync" in r.message for r in caplog.records)
