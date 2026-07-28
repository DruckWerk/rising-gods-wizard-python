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
└── ui/                # interface (Protokoll), whiptail_ui, rich_ui, null_ui, progress
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
