"""context.py — WizardContext: zieht durch alle Steps.

Pure Dataclass (keine Seiteneffekte). Steps lesen/schreiben Felder;
Hardware-Snapshot wird bei CLI-Start via hardware/* PURE befüllt.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import config


@dataclass
class HardwareSnapshot:
    """Ergebnis der PURE Hardware-Erkennung (gpu/session/kernel)."""

    gpu_vendor: str = "unknown"  # nvidia | amd | intel | unknown
    vram_mb: int = 0
    cpu_cores: int = 0
    cpu_threads: int = 0
    mem_total_gb: int = 0
    perf_class: str = "high"  # weak|old|low|mid|high|ultra
    session_type: str = "unknown"  # x11|wayland|tty|unknown
    kernel_tuple: tuple[int, int, int] = (0, 0, 0)
    ntsync_device_present: bool = False
    dxvk_active: bool = False


@dataclass
class WizardContext:
    """Zentraler Kontext, der durch alle Steps/Doctor-Module getragen wird."""

    # ── Pfade ────────────────────────────────────────────────────────────
    wow_dir: Path = field(default_factory=lambda: config.DEFAULT_WOW_DIR)
    prefix: Path = field(default_factory=lambda: config.DEFAULT_PREFIX)
    state_file: Path = field(default_factory=lambda: config.DEFAULT_STATE_FILE)
    launcher_path: Path = field(
        default_factory=lambda: config.DEFAULT_WOW_DIR / config.LAUNCHER_NAME
    )

    # ── Modus ────────────────────────────────────────────────────────────
    dry_run: bool = False
    export_lutris: bool = False
    doctor_mode: str = ""  # audit|repair|tune|hd|uninstall|""

    # ── Installations-Quelle ────────────────────────────────────────────
    existing_install: bool = False  # Feature 5: vorh. Install gewählt
    client_source: str = ""  # lokaler Pfad | torrent | http
    local_client_path: str = ""
    http_url: str = ""  # Fallback-Download-URL (CLI/image)
    torrent_url: str = ""  # Torrent-Magnet/-URL

    # ── Hardware ─────────────────────────────────────────────────────────
    hw: HardwareSnapshot = field(default_factory=HardwareSnapshot)

    # ── Ausgewählte Optionen (Checklisten) ───────────────────────────────
    ntsync_enabled: bool = False  # Bug A / Step08
    vmtune_enabled: bool = False
    fps_boost_selected: list[str] = field(default_factory=list)
    community_tools_selected: list[str] = field(default_factory=list)
    addons_enabled: bool = config.ADDONS_DEFAULT_ENABLED
    mangohud_enabled: bool = False

    # ── Wine ─────────────────────────────────────────────────────────────
    wine_cmd: str = "wine"
    use_gamemode: bool = True

    # ── Resume ───────────────────────────────────────────────────────────
    completed_steps: set[str] = field(default_factory=set)

    # ── Frei verfügbarer Bag für Module-spezifische Daten ────────────────
    extra: dict[str, Any] = field(default_factory=dict)

    # ── Helpers ────────────────────────────────────────────────────────────
    def _derive_paths(self) -> None:
        """Leite prefix/state_file/launcher_path relativ zu self.wow_dir neu ab.

        Muss nach jeder Änderung von ``self.wow_dir`` aufgerufen werden, damit
        die abgeleiteten Pfade zum überschriebenen Wurzelverzeichnis zeigen
        (z.B. via ``--wow-dir``). Die ``default_factory``-Werte in den
        Feldern bleiben als Initialwerte erhalten; hier wird der Zustand nach
        einer wow_dir-Änderung konsistent neu abgeleitet.
        """
        self.prefix = self.wow_dir / "prefix"
        self.state_file = self.wow_dir / ".wizard_state.sh"
        self.launcher_path = self.wow_dir / config.LAUNCHER_NAME

    @property
    def data_dir(self) -> Path:
        return self.wow_dir / "Data"

    @property
    def wtf_dir(self) -> Path:
        return self.data_dir / "WTF"

    @property
    def config_wtf_path(self) -> Path:
        return self.wtf_dir / "Config.wtf"

    @property
    def addons_dir(self) -> Path:
        return self.wow_dir / "Interface" / "AddOns"

    @property
    def dxvk_conf_path(self) -> Path:
        return self.prefix / "dxvk.conf"

    @property
    def mesa_cache_path(self) -> Path:
        return self.prefix / config.MESA_SHADER_CACHE_SUBDIR

    @property
    def dxvk_cache_path(self) -> Path:
        return self.prefix / config.DXVK_SHADER_CACHE_SUBDIR
