"""Tests für RichUI V2-04 (architect-spec-v2 §6, Chunk 4).

- RichUI nutzt AssetRenderer in show_step/render_banner (paint).
- Display-Koordinator für Progress (race-frei: paint außerhalb Live-Kontext).
- NullUI/WhiptailUI bleiben no-op (kein Attribut-Fehler).
"""
from __future__ import annotations

import pytest

from rising_gods_wizard.ui import rich_ui
from rising_gods_wizard.ui.interface import NullUI
from rising_gods_wizard.ui.layout import step_header
from rising_gods_wizard.ui.theme import get_theme


def test_richui_progress_delegates_to_progress(monkeypatch: pytest.MonkeyPatch) -> None:
    """start/update/stop_progress delegieren an eine Progress-Instanz."""
    calls: list[object] = []

    class _FakeProgress:
        def __init__(self) -> None:
            calls.append("make")

        def update(self, fraction: float, label: str = "") -> None:
            calls.append(("update", fraction, label))

        def close(self) -> None:
            calls.append("close")

    monkeypatch.setattr(rich_ui, "make_progress", lambda backend: _FakeProgress())
    # display=True erzwingt eine echte Console (rich ist installiert).
    r = rich_ui.RichUI(display=True, theme=get_theme("ice"))
    assert r._console is not None
    r.start_progress(100)
    r.update_progress(0.5, "lbl")
    r.stop_progress()
    assert "make" in calls
    assert ("update", 0.5, "lbl") in calls
    assert "close" in calls
    # Nach stop ist die Senke zurückgesetzt (kein aktiver Live-Kontext).
    assert r._progress is None


def test_richui_render_banner_returns_themed_string_noop_paint() -> None:
    """render_banner liefert themed-String; paint ist no-op bei console=None."""
    r = rich_ui.RichUI(display=False, theme=get_theme("ice"))
    out = r.render_banner("banner_header")
    # themed-String (Asset-Inhalt + Theme-Markup) wird zurückgegeben.
    assert "▒▒▒" in out  # ASCII-Quelle aus assets/banner-header.txt
    assert f"[{r._theme.primary}]" in out  # Theme-Markup ist aufgebracht
    # Bei console=None (headless/dry-run) darf paint() NICHTS auf der Console tun.
    assert r._console is None


def test_richui_render_banner_paints_when_console_present(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Mit Console + keinem aktiven Live-Kontext ruft render_banner paint() auf."""
    painted: list[str] = []
    r = rich_ui.RichUI(display=True, theme=get_theme("classic"))
    monkeypatch.setattr(r._renderer, "paint", lambda name, **kw: painted.append(name))
    r.render_banner("banner_header", box=True)
    assert "banner_header" in painted


def test_richui_render_banner_no_paint_during_active_progress(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Race-frei: paint() wird NICHT aufgerufen, solange ein Live-Kontext aktiv ist."""
    painted: list[str] = []

    class _FakeProgress:
        def __init__(self) -> None:
            pass

        def update(self, fraction: float, label: str = "") -> None:
            pass

        def close(self) -> None:
            pass

    monkeypatch.setattr(rich_ui, "make_progress", lambda backend: _FakeProgress())
    # AssetRenderer.paint wird beobachtet (nicht ersetzt, damit der Guard greift).
    r = rich_ui.RichUI(display=True, theme=get_theme("ice"))
    monkeypatch.setattr(r._renderer, "paint", lambda name, **kw: painted.append(name))
    r.start_progress(100)
    # Während aktivem Progress darf kein Asset-Paint passieren.
    r.render_banner("banner_header")
    assert painted == []
    r.stop_progress()
    # Nach stop() (kein Live-Kontext) darf paint() wieder aufgerufen werden.
    r.render_banner("banner_header")
    assert painted == ["banner_header"]


def test_richui_show_step_contains_step_label() -> None:
    """show_step(7,17,'Foo') enthält 'Schritt 7/17' (layout.step_header)."""
    r = rich_ui.RichUI(display=False, theme=get_theme("ice"))
    out = r.show_step(7, 17, "Foo")
    assert "Schritt 7/17" in out
    assert "Foo" in out
    # identisch zur reinen layout-Funktion
    assert out == step_header(7, 17, "Foo", r._theme)


def test_nullui_start_progress_is_noop() -> None:
    """NullUI.start_progress ist no-op (kein Attribut-Fehler, keine Senke)."""
    ui = NullUI()
    ui.start_progress(100)
    ui.update_progress(0.5, "lbl")
    ui.stop_progress()
