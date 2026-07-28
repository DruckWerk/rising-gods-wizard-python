"""test_session.py — detect_session (PURE, via injiziertem environ)."""
from rising_gods_wizard.hardware.session import detect_session


def test_x11():
    assert detect_session({"XDG_SESSION_TYPE": "x11"}) == "x11"


def test_wayland():
    assert detect_session({"XDG_SESSION_TYPE": "wayland"}) == "wayland"


def test_tty():
    assert detect_session({"XDG_SESSION_TYPE": "tty"}) == "tty"


def test_wayland_via_display():
    assert detect_session({"WAYLAND_DISPLAY": "wayland-0"}) == "wayland"


def test_none_unknown():
    assert detect_session({}) == "unknown"
