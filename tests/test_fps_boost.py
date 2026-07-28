"""test_fps_boost.py — preset-Wahl für GPU-Klassen WEAK/MID/HIGH/ULTRA."""
from __future__ import annotations

from rising_gods_wizard.game import fps_boost


def test_weak_all_selected():
    sel = fps_boost.selected_options("weak")
    assert set(sel) == set(fps_boost.FPS_OPTIONS)


def test_mid_glow_and_maxfpsbk():
    sel = fps_boost.selected_options("mid")
    assert sel == ["ffxGlow", "maxFPSBk"]


def test_high_only_maxfpsbk():
    sel = fps_boost.selected_options("high")
    assert sel == ["maxFPSBk"]


def test_ultra_none():
    sel = fps_boost.selected_options("ultra")
    assert sel == []


def test_unknown_class_defaults_to_high():
    sel = fps_boost.selected_options("bogus")
    assert sel == ["maxFPSBk"]


def test_build_fps_config_values():
    cfg = fps_boost.build_fps_config(["Sound_EnableMusic", "maxFPSBk"])
    assert 'SET Sound_EnableMusic "0"' in cfg
    assert 'SET maxFPSBk "30"' in cfg
