"""config.py — Konstanten und Defaults für den Rising Gods Linux Wizard.

Alle Magic-Numbers, Pfade und externen Quellen sind hier zentral gebündelt,
damit Steps/Module sie nicht hartkodieren. Werte stammen aus dem
bash-Original (Commit 58856cc) und der Architektur-Spec.
"""
from __future__ import annotations

from pathlib import Path

# ── Versions-/Pfad-Konstanten ──────────────────────────────────────────────
WIZARD_VERSION = "5.2-python"
DEFAULT_WOW_DIR = Path.home() / "Games" / "wow335"
DEFAULT_PREFIX = DEFAULT_WOW_DIR / "prefix"
DEFAULT_STATE_FILE = DEFAULT_WOW_DIR / ".wizard_state.sh"
LAUNCHER_NAME = "start-wow.sh"

# ── ntsync ─────────────────────────────────────────────────────────────────
# Advisory only: Distros backporten ntsync oft auch in ältere Kernel.
# Das maßgebliche Hard-Gate ist /dev/ntsync (siehe hardware/kernel.py).
MIN_NTSYNC_KERNEL: tuple[int, int, int] = (6, 14, 0)
NTSYNC_DEVICE = "/dev/ntsync"

# ── Realmlist (Feature 5) ──────────────────────────────────────────────────
# Default laut Spec. Vom Coder gegen Server-Doku zu bestätigen.
# Rising Gods nutzt laut README/Community den Login-Host "login.rising-gods.de".
REALMLIST_HOST = "login.rising-gods.de"
REALMLIST_LOCALES = ("enGB", "enUS", "deDE")

# ── Netzwerk / Torrent ─────────────────────────────────────────────────────
TORRENT_RPC_HOST = "127.0.0.1"
TORRENT_RPC_PORT = 9092  # isolation per Owner-Freigabe

# ── Community-Tools Live-Fetch (Feature 4) ─────────────────────────────────
# Quellen aus dem bash-Original (Proxyload-URLs). Coder-Ermittlung: diese
# URLs wurden aus dem Referenz-Repo übernommen. Bei "latest" (Default) findet
# KEINE Checksum-Verifikation statt (sonst widerspräche sie dem
# "immer aktuellste Version"-Ziel). Pinning via version+checksum möglich.
#
# WICHTIG: Kein silent Fallback auf veraltete lokale Kopie. Bei Offline →
# klarer Fehler (siehe addons/community_fetch.py).
COMMUNITY_SOURCES: dict[str, dict[str, str]] = {
    "wow_optimize": {
        "url": "https://github.com/suprepupre/wow-optimize/releases/download/"
        "v3.10.0/Release.7z",
        "kind": "archive",  # .7z → braucht 7z; DLL + version.dll extrahieren
        "dest_subdir": "",  # landet direkt in Wow.exe-Verzeichnis
        "version_pin": "v3.10.0",
        # checksum optional; bei version_pin hinterlegbar (SHA256 hex)
        "checksum": "",
    },
    "luaboost": {
        "url": "https://github.com/suprepupre/LuaBoost/archive/refs/heads/main.zip",
        "kind": "zip",
        "inner_dir": "LuaBoost-main",
        "dest_subdir": "!LuaBoost",
        "version_pin": "",  # latest
        "checksum": "",
    },
    "zonefarclip": {
        "url": "https://github.com/fajaman/ZoneFarclip/archive/refs/heads/master.zip",
        "kind": "zip",
        "inner_dir": "ZoneFarclip-master",
        "dest_subdir": "ZoneFarclip",
        "version_pin": "",  # latest
        "checksum": "",
    },
}

# ── Reguläre Online-Addons (addonhelper, default OFF) ──────────────────────
ADDON_BASE_URL = "https://addons.rising-gods.de"
ADDONS_DEFAULT_ENABLED = False  # Owner-Freigabe §11.6: opt-in

# ── DXVK/Shader-Cache ──────────────────────────────────────────────────────
MESA_SHADER_CACHE_SUBDIR = "mesa_shader_cache"
DXVK_SHADER_CACHE_SUBDIR = "dxvk_shader_cache"

# ── GameMode ───────────────────────────────────────────────────────────────
GAMEMODE_INI = Path.home() / ".config" / "gamemode.ini"

# ── Performance-Klassen ─────────────────────────────────────────────────────
PERF_CLASSES = ("weak", "old", "low", "mid", "high", "ultra")

# ── Checklist-Item IDs (Bug B Audit) ───────────────────────────────────────
# Zentrale Registry, damit test_checklist_audit.py jede id prüfen kann.
CHECKLIST_ITEMS: dict[str, list[str]] = {
    "system_tweaks": ["ntsync", "vmtune"],
    "fps_boost": [
        "Sound_EnableMusic",
        "Sound_EnableAmbience",
        "Sound_EnableReverb",
        "ffxGlow",
        "ffxDeath",
        "ffxSpecial",
        "maxFPSBk",
    ],
    "community_tools": ["wow_optimize", "luaboost", "zonefarclip"],
}

# ── Asset-Pfade (farblose ASCII) ───────────────────────────────────────────
ASSETS = {
    "banner_header": "banner-header.txt",
    "banner_main": "banner-main.txt",
    "frost_complete": "frost-complete.txt",
    "snow_spinner": "snow-spinner.txt",
    "arthas_quote": "arthas-quote.txt",
}

# ── Statische Binaries (Bundles) ────────────────────────────────────────
# pv/unrar liegen gebündelt unter rising_gods_wizard/bundles/ (offline nutzbar).
# Community-Tools werden NICHT gebündelt (siehe Feature 4), nur live gefetcht.
BUNDLES_DIR = Path(__file__).resolve().parent / "bundles"

# Style-Konvention: Das Package nutzt importlib.resources für assets/bundles,
# damit es auch als Wheel funktioniert.
