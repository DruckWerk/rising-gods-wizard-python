"""Tests für ui/layout.py (V2b, siehe architect-spec-v2 §3)."""
from rising_gods_wizard.ui.assets import AssetRenderer
from rising_gods_wizard.ui.layout import columns, divider, panel, step_header
from rising_gods_wizard.ui.theme import get_theme


def test_panel_contains_title_body_and_box_style() -> None:
    theme = get_theme("ice")
    out = panel(AssetRenderer(theme), "Titel", "Inhalt")
    assert "Titel" in out
    assert "Inhalt" in out
    assert f"[{theme.box_style}]" in out
    # Rahmen-Chars vorhanden
    assert "╔" in out and "╚" in out and "║" in out


def test_step_header_format() -> None:
    out = step_header(7, 17, "Foo", get_theme("ice"))
    assert "Schritt 7/17" in out
    assert "Foo" in out
    assert f"[{get_theme('ice').banner_style}]" in out


def test_columns_two_columns_with_align() -> None:
    out = columns(["a", "b"], [5, 5], ["left", "right"])
    parts = out.split("│")
    assert len(parts) == 2
    assert parts[0].startswith("a")
    assert parts[1].endswith("b")
    assert parts[0].strip() == "a"
    assert parts[1].strip() == "b"


def test_divider_not_empty() -> None:
    out = divider(AssetRenderer(get_theme("ice")))
    assert out.strip()
    assert f"[{get_theme('ice').box_style}]" in out
