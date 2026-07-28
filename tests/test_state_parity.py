"""test_state_parity.py — Parity + Roundtrip + DryRun für state.py.

Da actions.py (eigenes Chunk) noch nicht existiert, nutzen wir leichtgewichtige
Fakes, die das im Auftrag geforderte Interface `actions.fs.write(path, content)`
sowie das DryRun-Verhalten (nur loggen, nicht schreiben) abbilden.
"""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from rising_gods_wizard import state
from rising_gods_wizard.context import HardwareSnapshot, WizardContext


class _FakeFs:
    """Minimaler fs-Write-Ersatz: real schreibend oder nur loggend (dry-run)."""

    def __init__(self, dry_run: bool = False) -> None:
        self.dry_run = dry_run
        self.written: dict[str, str] = {}
        self.log: list[tuple[str, str]] = []

    def write(self, path, content: str) -> None:
        if self.dry_run:
            self.log.append((str(path), content))
        else:
            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")


class _FakeActions:
    """Ersatz für Real/DryRun-Actions (nur fs.write relevant hier)."""

    def __init__(self, dry_run: bool = False) -> None:
        self.dry_run = dry_run
        self.fs = _FakeFs(dry_run)


def _make_ctx(tmp: Path) -> WizardContext:
    ctx = WizardContext()
    ctx.wow_dir = tmp / "wow"
    ctx.existing_install = False
    ctx.client_source = "torrent"
    ctx.ntsync_enabled = True
    ctx.community_tools_selected = ["wow_optimize", "luaboost"]
    ctx.addons_enabled = True
    ctx.hw = HardwareSnapshot(gpu_vendor="nvidia", perf_class="high")
    return ctx


def test_render_is_sourceable() -> None:
    ctx = _make_ctx(Path("/tmp"))
    content = state.render(ctx)
    with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False) as f:
        f.write(content)
        path = f.name
    keys = [
        "WOW_DIR",
        "INSTALL_MODE",
        "NTSYNC_ENABLED",
        "GPU_CLASS",
        "COMMUNITY_TOOLS",
        "ADDONS",
        "FPS_PROFILE",
        "REALMLIST_HOST",
    ]
    script = "source " + path + "\n"
    script += "for k in " + " ".join(keys) + "; do\n"
    script += 'printf "%s=%s\\n" "$k" "${!k}"\n'
    script += "done\n"
    out = subprocess.run(
        ["bash", "-s"], input=script, capture_output=True, text=True
    )
    assert out.returncode == 0, out.stderr
    for k in keys:
        assert any(
            line.startswith(k + "=") for line in out.stdout.splitlines()
        ), f"Key {k} not set after source"
    Path(path).unlink(missing_ok=True)


def test_roundtrip() -> None:
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        ctx = _make_ctx(tmp)
        path = tmp / "wow" / ".wizard_state.sh"
        state.write_state_file(ctx, _FakeActions(dry_run=False), path=path)
        assert path.exists()
        data = state.read_state_file(path)
        expected = {
            "WOW_DIR": str(ctx.wow_dir),
            "INSTALL_MODE": "torrent",
            "NTSYNC_ENABLED": "true",
            "GPU_CLASS": "nvidia",
            "COMMUNITY_TOOLS": "wow_optimize,luaboost",
            "ADDONS": "true",
            "FPS_PROFILE": "high",
            "REALMLIST_HOST": "login.rising-gods.de",
        }
        assert data == expected


def test_dryrun_no_write() -> None:
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        ctx = _make_ctx(tmp)
        path = tmp / "wow" / ".wizard_state.sh"
        actions = _FakeActions(dry_run=True)
        state.write_state_file(ctx, actions, path=path)
        assert not path.exists()
        assert len(actions.fs.log) == 1
        logged_path, logged_content = actions.fs.log[0]
        assert logged_path == str(path)
        assert "WOW_DIR" in logged_content
