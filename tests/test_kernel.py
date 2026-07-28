"""test_kernel.py — parse_kernel / ntsync_supported / ntsync_device_present."""
import os

from rising_gods_wizard.hardware import kernel


def test_parse_kernel():
    assert kernel.parse_kernel("Linux 6.6.0-1-amd64") == (6, 6, 0)
    assert kernel.parse_kernel("Linux 5.15.0-generic") == (5, 15, 0)
    assert kernel.parse_kernel("6.14.1") == (6, 14, 1)
    assert kernel.parse_kernel("no version here") == (0, 0, 0)


def test_ntsync_supported():
    assert kernel.ntsync_supported((6, 6, 0)) is True
    assert kernel.ntsync_supported((6, 14, 0)) is True
    assert kernel.ntsync_supported((5, 15, 0)) is False


def test_ntsync_device_present(monkeypatch):
    monkeypatch.setattr(os.path, "exists", lambda p: p == "/dev/ntsync")
    assert kernel.ntsync_device_present() is True
    monkeypatch.setattr(os.path, "exists", lambda p: False)
    assert kernel.ntsync_device_present() is False
