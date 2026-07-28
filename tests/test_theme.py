"""Tests für ui/theme.py (V2a, siehe architect-spec-v2 §2)."""
from dataclasses import FrozenInstanceError, is_dataclass

import pytest

from rising_gods_wizard.ui.theme import THEMES, Theme, get_theme


def test_get_theme_ice_returns_ice() -> None:
    assert get_theme("ice") is THEMES["ice"]


def test_get_theme_unknown_falls_back_to_ice() -> None:
    assert get_theme("???") is THEMES["ice"]
    assert get_theme("") is THEMES["ice"]


def test_theme_is_frozen_dataclass() -> None:
    assert is_dataclass(Theme)
    ice = THEMES["ice"]
    with pytest.raises(FrozenInstanceError):
        setattr(ice, "primary", "red")
