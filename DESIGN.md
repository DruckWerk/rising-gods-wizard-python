# DESIGN.md — Rising Gods Linux Wizard (Python)

Architektur-Entscheidungen des Voll-Python-Rewrites (Build V1, Chunk 10/10).

## Warum Full-Python-Rewrite (§0.7)

Der bash-Original-Wizard (Commit `58856cc`) war gewachsen, vermischt Strings,
Netzwerk, FS- und Wine-Logik und nutzte `PROTON_USE_NTSYNC` (Bug A). Statt
weiterzuflicken galt die Regel **clean rebuild > flicken**: eine typsichere,
testbare, modularisierte Codebasis. Python bietet Dataclasses, `argparse`,
`importlib.resources` und einfacheres Testing (pytest/mypy) — Vorteile, die bash
nicht bietet.

## Modulare Paket-Struktur

Single-Responsibility je Modul; **< 130 Zeilen/Datei** als harte Grenze. Die
`WizardContext`-Dataclass (`context.py`) zieht seitenefekt-frei durch alle Steps;
Hardware-Snapshots werden PURE befüllt. Seiteneffekte sind hinter dem
`actions`-Objekt (`actions/shell.py`, `actions/fs.py`, `actions/packages.py`)
gekapselt — dieses ist die **Single-Source of Truth** für echte Writes.

Abhängigkeitsrichtung (kein Zyklus):
`__main__` → `steps` → `wine/game/dxvk/hardware/download/addons` → `actions` + `ui`.

## Bug A: ntsync bei plain Wine

`wine/launcher.py::compute_ntsync_env()` ist das autoritative Zentrum. Bei plain
Wine **muss** `WINENTSYNC=1` gesetzt werden; `PROTON_USE_NTSYNC=1` ist Proton-only
und bei plain wine ein No-Op (wurde im bash-Original fälschlich genutzt).

- User-Choice (`ctx.ntsync_enabled`) **UND** Hard-Gate (`/dev/ntsync` vorhanden,
  siehe `hardware/kernel.py`) müssen beide gelten.
- Advisory Kernel-Mindestversion: `config.MIN_NTSYNC_KERNEL = (6,14,0)`.
  Distro-Backports älterer Kernel werden toleriert (nur Warnung).
- Zusätzlich gesetzt: `WINEFSYNC=1`, `WINEESYNC=1` als Fallback.

## Feature 4: Community-Tools Live-Fetch

`addons/community_fetch.py` lädt `wow_optimize`, `luaboost`, `zonefarclip` IMMER frisch
von Upstream (Quellen in `config.COMMUNITY_SOURCES`).

- **Kein stale lokaler Fallback**: Offline/Netzfehler → harter `RuntimeError`.
- **Checksum nur bei Pin**: Default `version_pin=""` (latest) → KEINE Verifikation
  (sonst widerspräche sie dem "immer aktuellste Version"-Ziel). Bei gesetztem
  `version_pin` **und** `checksum` → SHA256-Verifikation via `download/direct.verify_file`,
  Abbruch bei Mismatch.
- Doctor `repair` nutzt dieselbe Funktion.

## Feature 5: Realmlist-Verifikation

`game/realmlist.py` prüft nur bei `ctx.existing_install == True` die locale-spezifische
`realmlist.wtf` (`Data/{enGB,enUS,deDE}/realmlist.wtf`) gegen `config.REALMLIST_HOST`.

- Reine Helfer (`detect_realmlist_path`, `parse_realmlist_host`, `needs_correction`)
  machen die Logik ohne FS-/UI-Side-Effects testbar.
- **Backup-Schreibung**: bei Korrektur wird das Original nach `*.wtf.bak` kopiert,
  bevor die korrekte Zeile geschrieben wird (`write_realmlist`).
- Entscheidung via `ui.ask_yes_no` (echte UI) bzw. Auto-Protokoll bei NullUI/dry-run.

## V1 / V2 / V3 Phasing

- **V1 (dieser Build)**: 17-Step-Install, Bug A, Feature 4+5, Doctor audit/repair/tune/hd/
  uninstall, Dry-Run, drei UI-Backends. Voll ruff- + pytest-konform.
- **V2 (geplant)**: Doctor-Politur, UI-Politur, erweiterte Resume-Logik,
  mehr Hardware-Profile.
- **V3 (optional)**: Textual-basiertes TUI als vollwertiges viertes UI-Backend.

## Dry-Run-Design

Das `actions`-Objekt ist die Single-Source für Side-Effects. Im Dry-Run
(`ctx.dry_run`) führen Shell/FS-Actions keine echten Writes aus, sondern nur Pläne/
Logs. Steps rufen `actions.shell.run` / `actions.fs.write` wie gewohnt — das
Verhalten wird am Actions-Layer umgeschaltet. State-File (`state.write_state_file`)
wird im Dry-Run nicht geschrieben; stattdessen wird `state.render(ctx)` ausgegeben.

## Build-Notiz: 9+1 Chunked-Build

Der Wizard wurde in 10 Chunks (1–9 Code, 10 Docs) mit Modell `tencent/hy3:free`
gebaut — eine bewusste Modell-Limit-Umgehung (kurze Kontextfenster pro Chunk).
Jeder Code-Chunk wurde einzeln mit `ruff check` + `pytest` verifiziert, bevor der
nächste folgte. Dadurch blieb der Build grün, ohne ein Riesen-Context-Fenster zu
benötigen.

## Konfiguration

`config.py` bündelt alle Konstanten zentral (keine hartkodierten Magic-Numbers in
Steps):

- `REALMLIST_HOST = "login.rising-gods.de"` — aus Server-/Community-Doku zu bestätigen.
- `COMMUNITY_SOURCES` — Dict der Live-Fetch-Quellen (URL, kind, dest_subdir,
  version_pin, checksum).
- Pfade: `DEFAULT_WOW_DIR = ~/Games/wow335`, `DEFAULT_PREFIX`, `DEFAULT_STATE_FILE`.
- `NTSYNC_DEVICE = "/dev/ntsync"`, `MIN_NTSYNC_KERNEL`.
- `PERF_CLASSES`, `CHECKLIST_ITEMS`, `ADDON_BASE_URL`, `GAMEMODE_INI`.

Steps/Module importieren aus `config`, statt Werte zu hartkodieren.
