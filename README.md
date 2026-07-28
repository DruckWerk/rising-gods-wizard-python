# Rising Gods Linux Wizard (Python)

Vollständiger Python-Rewrite des bash-Install-Wizards für **World of Warcraft 3.3.5a**
unter Linux/Wine. Installiert Client, Wine-Prefix, DXVK/Vulkan, GPU-optimierte
Tweaks, FPS-Boost, Community-Tools und einen startbereiten Launcher — headless
steuerbar per Whiptail-, Rich- oder Null-UI.

Das bash-Original dient als Referenz: `/home/jarvis/projects/rising-gods-linux-wizard/`.

## Features

- **17-Step-Install** (Steps 1–17, siehe `steps/registry.py`): Pre-Flight, System,
  Wine-Prefix, DXVK, Client-Download, Registry-Tweaks, GPU-Detection, System-Tweaks,
  Shader-Caches, Audio, Launcher, GameMode, Feintuning, FPS-Boost, Community-Tools,
  MangoHud, Abschluss+State.
- **Bug A — ntsync-Fix**: bei plain Wine wird korrekt `WINENTSYNC=1` gesetzt
  (nicht der bei plain wine wirkungslose `PROTON_USE_NTSYNC`). Hard-Gate: `/dev/ntsync`.
- **Feature 4 — Community-Tools Live-Fetch**: `wow_optimize`, `luaboost`, `zonefarclip`
  werden immer frisch von Upstream geladen. Kein stale lokaler Fallback. Checksum nur
  bei Versions-Pin (`config.COMMUNITY_SOURCES`).
- **Feature 5 — Realmlist-Verifikation**: prüft bei vorhandener Installation die
  `realmlist.wtf` gegen `config.REALMLIST_HOST` (`login.rising-gods.de`); schreibt bei
  Zustimmung ein Backup + korrekte Zeile.
- **Doctor-Modus**: `audit` (read-only), `repair`, `tune`, `hd`, `uninstall`.
- **Dry-Run**: `--dry-run` führt keine echten FS/Shell-Writes aus; Aktionen werden nur
  protokolliert (State-File-Inhalt wird ausgegeben, nicht geschrieben).
- **Drei UI-Backends**: `whiptail` (Default, TTY-Dialoge), `rich` (Terminal-Display),
  `null` (no-op, für CI/dry-run/Headless).
- **V2-UI/Theming (optional)**: `ice`/`classic`/`mono`-Theme via `--theme`, farblose
  ASCII-Assets, Layout-Helfer, Cancel/Back-Protokoll. Siehe Abschnitt unten.

## V2 — UI/Theming (optional)

Reine UI/Asset-Erweiterung (kein Step-Rewrite), gekapselt hinter `UIProtocol`
(Dependency Inversion). Steps rufen nur das Protokoll; Backends rendern Assets.

- **AssetRenderer + Theme** (`ui/assets.py`, `ui/theme.py`): farblose Plaintext-ASCII
  (`assets/*.txt`) als Quelle + Laufzeit-Theming (Farbe, Box-Decoration). Drei Themes:
  `ice` (Lich-King Eisblau, Default), `classic` (Gold/Rot), `mono` (reinweiß).
  `render()` ist rein/deterministisch; `paint()` schreibt auf die Console (Typewriter-
  Sleep nur hier, zentral).
- **layout.py** (`ui/layout.py`): deklarative Markup-Helfer `panel`/`divider`/`columns`/
  `step_header` über Theme/AssetRenderer — ohne I/O.
- **`--theme` CLI-Flag**: `ice` | `classic` | `mono` (Default `ice`). Steuert Farbe der
  RichUI/Whiptail-Titel; NullUI ignoriert es (no-op).
- **Cancel/Back-Protokoll** (`ask_yes_no_c`): neue UI-Methode liefert
  `bool | "cancel"`. Whiptail bei ESC/RC!=0 → `"cancel"`; Rich bei ESC/Timeout →
  `"cancel"`; NullUI → `default` (headless = proceed). Steps rufen sie via
  `getattr(ui, "ask_yes_no_c", None)`; bei `"cancel"` bricht der Step sauber ab, State
  bleibt unverändert (Resume funktioniert, da State erst am Ende geschrieben wird).
- **Progress-Senke** (V2-03): optionale `start_progress`/`update_progress`/`stop_progress`
  im Protokoll (Default no-op). RichUI delegiert an `ui/progress`; Whiptail/NullUI no-op.
- **RichUI-Integration (V2-04, ABGESCHLOSSEN)**: RichUI instanziiert EINEN `AssetRenderer`
  (an dieselbe `rich.Console` gebunden) und nutzt ihn in `show_step` (via `layout.step_header`)
  und `render_banner` (via `AssetRenderer.paint`). Race-freie Progress/Asset-Koordination:
  `AssetRenderer.paint()` läuft NUR außerhalb eines aktiven Live-Kontextes (vor
  `Progress.start()` / nach `stop()`) — der Guard ist `self._progress is None`. So entsteht
  kein ANSI-Flicker-Race zwischen Console-Print und rich Live. `progress.py` selbst wurde
  NICHT verändert; nur die Senke (RichUI) ist verdrahtet.

> **V2 ist vollständig.** Alle Teile (V2a AssetRenderer/Theme, V2b layout, V2c --theme Flag,
> V2e progress-Koordination + RichUI-Integration) sind implementiert und grün
> (ruff + mypy --strict + pytest). V2d (RichUI-eigene Prompts statt whiptail) ist bewusst
> NICHT gemacht → V3.

## Installation

> PEP 668: system-weites `pip install` ist auf Debian 13 verboten. Immer einen
> venv nutzen.

```bash
cd /home/jarvis/projects/rising-gods-wizard-python
python -m venv .venv
. .venv/bin/activate
pip install -e .
# optional: rich-Display-Backend
pip install -e ".[rich]"
```

Danach steht das Konsolen-Skript `rising-gods-wizard` (via `pyproject.toml`) sowie
`python -m rising_gods_wizard` zur Verfügung.

## Usage

```bash
# Trockenlauf (keine echten Writes), Null-UI
python -m rising_gods_wizard --dry-run

# Echte Installation in Standard-Ziel (~/Games/wow335)
python -m rising_gods_wizard

# Nur einen Step ausführen (hier Step 8: System-Tweaks/ntsync)
python -m rising_gods_wizard --step 8

# Bestehende Installation reparieren/verifizieren
python -m rising_gods_wizard --wow-dir ~/Games/wow335 --doctor repair

# Read-only Audit
python -m rising_gods_wizard --doctor audit

# Anderes UI-Backend erzwingen
python -m rising_gods_wizard --ui rich
python -m rising_gods_wizard --dry-run --ui null

# V2: UI-Theme wählen (ice=Lich-King, classic, mono)
python -m rising_gods_wizard --ui rich --theme classic
python -m rising_gods_wizard --dry-run --theme mono
```

### CLI-Flags (`__main__.py`)

| Flag | Default | Wirkung |
|------|---------|---------|
| `--dry-run` | aus | Keine echten FS/Shell-Writes |
| `--wow-dir PATH` | `~/Games/wow335` | Ziel; bei Existenz → `existing_install=True` |
| `--locale` | `enUS` | Locale (enGB/enUS/deDE) |
| `--step N` | alle (1..17) | Einzelner Step |
| `--doctor MODE` | — | `audit\|repair\|tune\|hd\|uninstall` |
| `--ui BACKEND` | `null` bei dry-run, sonst `whiptail` | `whiptail\|rich\|null` |
| `--theme NAME` | `ice` | `ice\|classic\|mono` (V2, UI-Theming) |

## Projektstruktur

```
rising_gods_wizard/
├── __main__.py        # CLI-Entry (argparse), Context, UI-Wahl, Dispatch
├── config.py          # Zentrale Konstanten (REALMLIST_HOST, COMMUNITY_SOURCES, Pfade)
├── context.py         # WizardContext + HardwareSnapshot (dataclass, side-effect-frei)
├── state.py           # .wizard_state.sh lesen/schreiben (bash-sourceable, Resume)
├── actions/           # Seiteneffekt-Layer: shell, fs, packages, interface (Single-Source)
├── wine/              # launcher (start-wow.sh, ntsync-env), prefix, audio
├── game/              # realmlist (Feature 5), fps_boost, shader_cache, config_wtf,
│                      #   lutris_export, mangohud
├── dxvk/              # install, config (dxvk.conf)
├── hardware/          # session (X11/Wayland), gpu (Vendor/VRAM), kernel (/dev/ntsync)
├── download/          # direct (curl), client, torrent (RPC)
├── addons/            # community_fetch (Feature 4), addonhelper, ui, bundles/
├── steps/             # registry + step01..step17 (17-Step-Install)
├── doctor/            # audit, repair, tune, hd, uninstall
└── ui/                # interface (Protokoll), whiptail_ui, rich_ui, null_ui, progress,
│                      #   theme (V2a), assets (V2a AssetRenderer), layout (V2b)
```

## Tests & Qualität

```bash
pytest tests/          # Unit-Tests (ruff/mypy-konform)
ruff check rising_gods_wizard/   # Lint (line-length 100, py310)
mypy --strict rising_gods_wizard/   # Typprüfung (strict)
```

## Hinweise

- Das bash-Original ist Referenz: `/home/jarvis/projects/rising-gods-linux-wizard/`.
- Laufzeit-Pflichtabhängigkeiten: keine. `whiptail` (System-Tool `newt`) und `rich`
  (optional) werden graceful degradiert, falls nicht installiert.
- `config.REALMLIST_HOST` ist aus der Server-/Community-Doku zu bestätigen (aktuell
  `login.rising-gods.de`).
