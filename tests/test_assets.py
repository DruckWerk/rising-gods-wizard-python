"""Tests für ui/assets.py (V2a, siehe architect-spec-v2 §2)."""
import re
from pathlib import Path

_TAG = re.compile(r"\[/?[^\]]*\]")


def _visible(text: str) -> list[str]:
    return _TAG.sub("", text).splitlines()

import pytest

import rising_gods_wizard
from rising_gods_wizard.ui.assets import ASSET_NAMES, AssetRenderer
from rising_gods_wizard.ui.theme import get_theme

ASSETS_DIR = Path(rising_gods_wizard.__file__).parent / "assets"


def _asset_text(name: str) -> str:
    return (ASSETS_DIR / f"{name.replace('_', '-')}.txt").read_text(encoding="utf-8")


def test_load_source_returns_expected_text() -> None:
    r = AssetRenderer(get_theme("ice"))
    assert r.load_source("banner_header") == _asset_text("banner_header")
    assert r.load_source("arthas_quote_2") == _asset_text("arthas_quote_2")


def test_load_source_unknown_raises_keyerror() -> None:
    r = AssetRenderer(get_theme("ice"))
    try:
        r.load_source("nope")
    except KeyError:
        return
    raise AssertionError("expected KeyError for unknown asset name")


def test_render_box_contains_frame_markup() -> None:
    theme = get_theme("ice")
    r = AssetRenderer(theme)
    out = r.render("banner_header", box=True)
    assert f"[{theme.box_style}]" in out
    assert "╔" in out and "╚" in out and "║" in out


def test_render_align_center_pads() -> None:
    r = AssetRenderer(get_theme("ice"))
    left = _visible(r.render("banner_header", align="left"))
    center = _visible(r.render("banner_header", align="center"))
    assert left != center
    width = max(len(l) for l in left)
    # center füllt jede sichtbare Zeile auf die volle Breite auf
    assert all(len(l) == width for l in center)
    # und unterscheidet sich von left (mindestens eine Zeile verschoben)
    assert any(cl != cc for cl, cc in zip(left, center))


def test_render_independent_of_typewriter() -> None:
    r = AssetRenderer(get_theme("ice"))
    a = r.render("banner_header", typewriter=True)
    b = r.render("banner_header", typewriter=False)
    assert a == b


def test_paint_no_console_is_noop(capsys: pytest.CaptureFixture[str]) -> None:
    r = AssetRenderer(get_theme("ice"), console=None)
    r.paint("banner_header", typewriter=True)
    assert capsys.readouterr().out == ""


def test_all_assets_load() -> None:
    r = AssetRenderer(get_theme("ice"))
    for name in ASSET_NAMES:
        assert r.load_source(name).strip()
