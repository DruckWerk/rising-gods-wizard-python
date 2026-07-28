"""progress.py — Einheitlicher Progress-Helfer (TQDM/Rich, import-guarded).

LiveProgress kapselt ein Render-Objekt (rich Live oder tqdm). Alle
Progress-Quellen schreiben hier hinein -> kein Flackern, kein Race.
Fällt auf plain-print zurück, wenn weder rich noch tqdm vorhanden sind.
"""
from __future__ import annotations

import logging
from typing import Any

log = logging.getLogger(__name__)


class Progress:
    """Fraktions-basierter Progress (fraction 0.0..1.0)."""

    def __init__(self, use_rich: bool = True, use_tqdm: bool = True) -> None:
        self._live: Any = None
        self._rich: Any = None
        self._task: Any = None
        self._tqdm: Any = None
        self._init_backend(use_rich, use_tqdm)

    def _init_backend(self, use_rich: bool, use_tqdm: bool) -> None:
        if use_rich:
            try:
                from rich.live import Live
                from rich.progress import Progress as RichProgress
                self._rich = RichProgress()
                self._live = Live(self._rich, auto_refresh=False)
                self._task = self._rich.add_task("…", total=100)
                return
            except Exception:  # noqa: BLE001 - rich optional
                log.debug("rich nicht verfügbar; Fallback")
        if use_tqdm:
            try:
                from tqdm import tqdm
                self._tqdm = tqdm(total=100, unit="%")
                return
            except Exception:  # noqa: BLE001 - tqdm optional
                log.debug("tqdm nicht verfügbar; Fallback")
        self._tqdm = None  # plain fallback

    def update(self, fraction: float, label: str = "") -> None:
        pct = max(0, min(100, int(fraction * 100)))
        if self._live is not None:
            self._rich.update(self._task, completed=pct, description=label)
            self._live.refresh()
        elif self._tqdm is not None:
            self._tqdm.update(pct - self._tqdm.n)
        else:
            print(f"[{pct:3d}%] {label}")

    def close(self) -> None:
        if self._live is not None:
            self._live.stop()
        elif self._tqdm is not None:
            self._tqdm.close()


def make_progress(backend: str = "auto") -> Progress:
    if backend == "rich":
        return Progress(use_rich=True, use_tqdm=False)
    if backend == "tqdm":
        return Progress(use_rich=False, use_tqdm=True)
    return Progress(use_rich=True, use_tqdm=True)
