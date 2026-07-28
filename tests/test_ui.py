"""test_ui.py — NullUI-Default + UIProtocol + guarded Imports.

- NullUI.ask_yes_no -> Default
- interface.UIProtocol erfüllt (ABC)
- WhiptailUI/RichUI Import crashen nicht (whiptail/rich evtl. fehlschlagend)
"""
from rising_gods_wizard.ui.interface import UIProtocol, NullUI, NoopUI
from rising_gods_wizard.ui import null_ui, whiptail_ui, rich_ui, progress


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
