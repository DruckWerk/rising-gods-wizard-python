"""test_ui.py — NullUI-Default + UIProtocol + guarded Imports + V2-03 Protokoll.

- NullUI.ask_yes_no -> Default
- interface.UIProtocol erfüllt (ABC)
- WhiptailUI/RichUI Import crashen nicht (whiptail/rich evtl. fehlschlagend)
- V2-03: ask_yes_no_c Cancel-Status + Progress-Senke no-op
"""
from rising_gods_wizard.ui.interface import UIProtocol, NullUI, NoopUI, Cancel
from rising_gods_wizard.ui import null_ui, whiptail_ui, rich_ui, progress
from rising_gods_wizard.ui.theme import get_theme


def test_nullui_ask_yes_no_default():
    ui = NullUI()
    assert ui.ask_yes_no("?", default=True) is True
    assert ui.ask_yes_no("?", default=False) is False
    assert ui.ask_choice("?", ["a", "b"], default="a") == "a"
    assert ui.prompt("?", default="x") == "x"
    # keine Ausgabe, kein Crash
    ui.note("n"); ui.warn("w"); ui.error("e")


def test_interface_is_abc():
    assert issubclass(UIProtocol, object)
    # NullUI implementiert UIProtocol
    assert isinstance(NullUI(), UIProtocol)


def test_noop_alias_works():
    assert null_ui.NullUI is NullUI


def test_whiptail_import_no_crash():
    # Import + Instanzierung + Prompt dürfen nicht crashen. Liefert immer bool,
    # egal ob whiptail installiert (echtes TTY) oder fehlend (Fallback-Default).
    w = whiptail_ui.WhiptailUI()
    assert isinstance(w.ask_yes_no("?", default=True), bool)
    assert isinstance(w.ask_choice("?", ["a", "b"], default="a"), str)
    assert w.prompt("?", default="x") == "x"  # ohne TTY: Default-String


def test_rich_import_no_crash():
    # Import + Instanzierung ohne rich installiert -> plain fallback
    r = rich_ui.RichUI()
    r.note("test"); r.warn("w"); r.error("e")
    assert r.ask_yes_no("?", default=False) is False


def test_progress_import_and_fallback():
    p = progress.make_progress(backend="auto")
    p.update(0.5, "label")
    p.close()


# ── V2-03: Cancel/Progress-Protokoll ──────────────────────────────────
def test_nullui_ask_yes_no_c_default_no_cancel():
    # Headless: kein Cancel — immer default (proceed)
    ui = NullUI()
    assert ui.ask_yes_no_c("?", default=True) is True
    assert ui.ask_yes_no_c("?", default=False) is False


def test_nullui_progress_sink_is_noop():
    # Progress-Methoden dürfen nicht crashen (kein Attribut-Fehler).
    ui = NullUI()
    ui.start_progress(100)
    ui.update_progress(0.5, "lbl")
    ui.stop_progress()


def test_whiptail_ask_yes_no_c_no_tty_returns_bool():
    # whiptail ist installiert, aber kein TTY -> RC=1 (Nein), kein Cancel.
    # Wichtig: ask_yes_no_c liefert hier bool (nicht "cancel"), da RC!=ESC-Code.
    w = whiptail_ui.WhiptailUI()
    assert isinstance(w.ask_yes_no_c("?", default=True), bool)


def test_richui_ask_yes_no_c_default_headless():
    # Ohne rich-Console (display=False) -> kein Cancel, liefert default.
    r = rich_ui.RichUI(display=False)
    assert r.ask_yes_no_c("?", default=True) is True


def test_richui_progress_sink_noop_without_console():
    # display=False: Progress-Instanz wird nicht angelegt, Calls no-op.
    r = rich_ui.RichUI(display=False)
    r.start_progress(100)
    r.update_progress(0.5, "lbl")
    r.stop_progress()


def test_whiptail_theme_param_accepted():
    theme = get_theme("classic")
    w = whiptail_ui.WhiptailUI(theme=theme)
    assert w._theme is theme


def test_richui_theme_param_accepted():
    theme = get_theme("mono")
    r = rich_ui.RichUI(theme=theme)
    assert r._theme is theme
