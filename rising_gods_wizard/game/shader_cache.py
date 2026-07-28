"""shader_cache.py — Shader-Cache-Verzeichnisse anlegen.

Legt mesa_shader_cache und dxvk_shader_cache im Wine-Prefix an (actions.fs.mkdir).
Diese Verzeichnisse beschleunigen nachfolgende Starts (kein Recompile).
"""
from __future__ import annotations

from typing import Any

from ..context import WizardContext


def ensure_shader_cache_dirs(ctx: WizardContext, actions: Any) -> list[str]:
    """Legt beide Shader-Cache-Verzeichnisse an (dry-run-sicher)."""
    done: list[str] = []
    for p in (ctx.mesa_cache_path, ctx.dxvk_cache_path):
        actions.fs.mkdir(p, mode=0o755)
        done.append(str(p))
    return done
