"""__main__.py — Entry-Point: `python -m rising_gods_wizard`.

CLI (argparse) -> InstallContext aufbauen -> UI wählen ->
Actions.build(ctx) -> entweder Doctor-Dispatch oder Step-Orchestration.

Hinweis zur Aufgabenbeschreibung: diese referenzierte
`actions.build(ctx, dry_run=...)` und `state.render_sourceable(ctx)`.
Die tatsächlich implementierte API lautet:
  - Actions.build(ctx)  (dry_run steckt im ctx, nicht im build-Aufruf)
  - state.render(ctx)   (bash-sourceable Inhalt; render_sourceable existiert
                         nicht — wir nutzen render + write_state_file)
Wir binden an die echte API, damit der Wizard läuft, statt an die in
der Chunk-Spec angenommene (veraltete) Signatur.
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from . import state
from .actions import Actions
from .context import WizardContext
from .steps import registry as steps_registry
from .ui import interface
from .ui.null_ui import NullUI
from .ui.rich_ui import RichUI
from .ui.theme import get_theme
from .ui.whiptail_ui import WhiptailUI

log = logging.getLogger("rising_gods_wizard")

LAST_STEP = 17

DOCTOR_MODES = ("audit", "repair", "tune", "hd", "uninstall")


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="rising-gods-wizard",
        description="Rising Gods Linux Wizard — WoW 3.3.5a Installer (Python).",
    )
    p.add_argument("--dry-run", action="store_true",
                   help="Keine echten FS/Shell-Writes; Aktionen nur protokollieren.")
    p.add_argument("--wow-dir", metavar="PATH", default=None,
                   help="Bestehende Installation -> ctx.existing_install=True.")
    p.add_argument("--locale", default="enUS",
                   help="Locale (Default enUS).")
    p.add_argument("--step", type=int, metavar="N", default=None,
                   help="Einzelner Step (1..17), sonst alle 1..17.")
    p.add_argument("--doctor", choices=DOCTOR_MODES, default=None,
                   help="Doctor-Modus: audit|repair|tune|hd|uninstall.")
    p.add_argument("--ui", choices=("whiptail", "rich", "null"), default=None,
                   help="UI-Backend (Default: null bei --dry-run, sonst whiptail).")
    p.add_argument("--theme", choices=("ice", "classic", "mono"), default="ice",
                   help="UI-Theme (Default: ice/Lich-King).")
    return p


def _build_context(args: argparse.Namespace) -> WizardContext:
    ctx = WizardContext()
    ctx.dry_run = bool(args.dry_run)

    if args.wow_dir:
        ctx.wow_dir = Path(args.wow_dir).expanduser()
        # Abgeleitete Pfade (prefix/state_file/launcher_path) neu relativ zum
        # überschriebenen wow_dir setzen — sonst zeigen sie auf den Default.
        ctx._derive_paths()
        # Bestehende Installation: nur, wenn wirklich eine Data/ mit
        # realmlist/wow.exe vorfinden — sonst trotzdem als Zielpfad nutzen,
        # aber existing_install nur setzen, wenn es Sinn ergibt.
        ctx.existing_install = ctx.wow_dir.exists()

    if args.locale:
        ctx.extra["locale"] = args.locale

    if args.doctor:
        ctx.doctor_mode = args.doctor

    # Dry-Run: sicherer HTTP-Platzhalter, damit die Step-Logik (insb.
    # Step05 fetch_client) ohne RuntimeError durchläuft. Im dry-run führt
    # die Shell-Action nur Pläne aus, kein echtes Netz. ctx.http_url wird
    # als dynamisches Attribut gesetzt (fetch_client liest ctx.http_url).
    if ctx.dry_run and not getattr(ctx, "http_url", ""):
        ctx.http_url = "http://dry-run.invalid/wow_client"

    return ctx


def _choose_ui(args: argparse.Namespace, ctx: WizardContext) -> interface.UIProtocol:
    choice = args.ui
    if choice is None:
        choice = "null" if ctx.dry_run else "whiptail"
    theme = get_theme(args.theme or "ice")
    if choice == "null":
        return NullUI()
    if choice == "rich":
        return RichUI(display=not ctx.dry_run, theme=theme)
    # whiptail
    return WhiptailUI(title="Rising Gods Wizard", theme=theme)


def _dispatch_doctor(args: argparse.Namespace, ctx: WizardContext,
                     ui: interface.UIProtocol, actions: Actions) -> int:
    from .doctor.audit import audit as doctor_audit
    from .doctor.hd import install_hd_textures as doctor_hd
    from .doctor.repair import repair as doctor_repair
    from .doctor.tune import tune as doctor_tune
    from .doctor.uninstall import uninstall as doctor_uninstall

    mode = ctx.doctor_mode
    ui.note(f"Doctor-Modus: {mode}")

    if mode == "audit":
        result = doctor_audit(ctx, actions)
        ok = result.get("ok", False)
        for f in result.get("findings", []):
            ui.note(f"  [{f['status']}] {f['component']}: {f['detail']}")
        ui.note("Audit " + ("OK" if ok else "mit Befunden"))
        return 0 if ok else 1

    done: list[str]
    if mode == "repair":
        done = doctor_repair(ctx, ui, actions)
    elif mode == "tune":
        done = doctor_tune(ctx, ui, actions)
    elif mode == "hd":
        done = [doctor_hd(ctx, ui, actions)]
    elif mode == "uninstall":
        done = doctor_uninstall(ctx, ui, actions)
    else:  # pragma: no cover - argparse choices verhindert das
        ui.error(f"Unbekannter Doctor-Modus: {mode}")
        return 2

    for line in done:
        ui.note(f"  - {line}")
    return 0


def _run_steps(args: argparse.Namespace, ctx: WizardContext,
               ui: interface.UIProtocol, actions: Actions) -> None:
    if args.step is not None:
        if not (1 <= args.step <= LAST_STEP):
            raise SystemExit(f"Ungültiger --step {args.step} (1..{LAST_STEP})")
        ui.note(f"Einzelner Step {args.step}: {steps_registry.STEP_TITLES[args.step]}")
        steps_registry.run_step(args.step, ctx, ui, actions)
        return

    for n in range(1, LAST_STEP + 1):
        title = steps_registry.STEP_TITLES[n]
        ui_note_step = getattr(ui, "show_step", None)
        if callable(ui_note_step):
            ui_note_step(n, LAST_STEP, title)
        else:
            ui.note(f"Schritt {n}/{LAST_STEP}: {title}")
        steps_registry.run_step(n, ctx, ui, actions)


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.INFO if not args.dry_run else logging.DEBUG,
        format="%(levelname)s %(name)s: %(message)s",
    )

    ctx = _build_context(args)
    ui = _choose_ui(args, ctx)
    actions = Actions.build(ctx)

    if ctx.doctor_mode:
        rc = _dispatch_doctor(args, ctx, ui, actions)
        # Bei audit kein State-Write; bei repair/tune/hd/uninstall ggf. State
        # aktualisieren (dry-run: nur render_sourceable protokollieren).
        if ctx.dry_run:
            ui.note(state.render(ctx))
        else:
            state.write_state_file(ctx, actions)
        return rc

    try:
        _run_steps(args, ctx, ui, actions)
    except Exception as exc:  # noqa: BLE001 - CLI-Top-Level: sauber melden
        ui.error(f"Wizard abgebrochen: {exc}")
        log.exception("Wizard-Fehler")
        return 1

    # Abschluss: State-Datei schreiben (dry-run: nur Inhalt protokollieren).
    if ctx.dry_run:
        ui.note("=== [dry-run] erzeugter State-File-Inhalt ===")
        ui.note(state.render(ctx))
        ui.note("=== dry-run beendet (keine echten Writes) ===")
    else:
        state.write_state_file(ctx, actions)
        ui.note(f"Wizard abgeschlossen. State: {ctx.state_file}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
