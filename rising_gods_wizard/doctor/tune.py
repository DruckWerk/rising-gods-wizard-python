"""tune.py — Performance-Tuning (Doctor tune).

Wendet FPS-Preset + Shader-Caches neu an (config-regen, dry-run-sicher).
"""
from __future__ import annotations

from typing import Any

from ..context import WizardContext
from ..game.config_wtf import write_config_wtf
from ..game.fps_boost import build_fps_config, selected_options
from ..game.shader_cache import ensure_shader_cache_dirs


def tune(ctx: WizardContext, ui: Any, actions: Any) -> list[str]:
    """Wendet Performance-Tuning an. Liefert Liste erledigter Schritte."""
    done: list[str] = []

    sel = ctx.fps_boost_selected or selected_options(ctx.hw.perf_class)
    fps_block = build_fps_config(sel)
    write_config_wtf(ctx, actions)  # Config.wtf (40 Einträge)
    # FPS-Block an Config.wtf anhängen (PURE gen + actions write)
    target = ctx.config_wtf_path
    if target.exists():
        actions.fs.write(target, _append_fps(target, fps_block))
    done.append(f"Config.wtf + FPS-Preset ({len(sel)} Optionen) angewendet")

    dirs = ensure_shader_cache_dirs(ctx, actions)
    done.append(f"Shader-Caches: {', '.join(dirs)}")
    return done


def _append_fps(path: Any, fps_block: str) -> str:
    """Liest bestehende Config.wtf (real) und hängt FPS-Block an."""
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    return existing.rstrip() + "\n" + fps_block
