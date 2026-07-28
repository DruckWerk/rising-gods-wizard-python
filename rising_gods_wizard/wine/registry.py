"""registry.py — Wine-Registry-Tweaks (CSMT, Offscreen, DrawOrder, MSAA).

Generiert eine .reg-Datei mit Grafik-Stabilitäts-Tweaks, die der
Launcher per `wine regedit` importiert.
"""
from __future__ import annotations

from ..actions import Actions
from ..context import WizardContext

# Registry-Pfad für Wine-Grafik-Tweaks
D3D_KEY = r"HKEY_CURRENT_USER\Software\Wine\Direct3D"

# Tweak-Keys die geschrieben werden (Bug B Checklist-Audit-tauglich)
REG_TWEAKS: dict[str, str] = {
    "csmt": "y",
    "OffscreenRenderingMode": "fbo",
    "StrictDrawOrdering": "disabled",
    "Multisampling": "disabled",
}


def build_registry_content() -> str:
    """PURE: liefert den Inhalt der .reg-Datei (inkl. aller Tweak-Keys)."""
    lines = ["REGEDIT4", "", f"[{D3D_KEY}]"]
    for key, val in REG_TWEAKS.items():
        lines.append(f'"{key}"="{val}"')
    lines.append("")
    return "\n".join(lines)


def write_registry(ctx: WizardContext, actions: Actions) -> None:
    """Side-Effecting: schreibt die .reg-Datei ins Prefix via actions.fs."""
    content = build_registry_content()
    reg_path = ctx.prefix / "rgw-tweaks.reg"
    actions.fs.write(reg_path, content)
