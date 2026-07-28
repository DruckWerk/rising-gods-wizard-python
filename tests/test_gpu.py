"""test_gpu.py — detect_gpu_class / parse_vendor (PURE)."""
from rising_gods_wizard.hardware.gpu import detect_gpu_class, parse_vendor


def test_parse_vendor():
    assert parse_vendor("NVIDIA Corporation GP106") == "nvidia"
    assert parse_vendor("Advanced Micro Devices Navi") == "amd"
    assert parse_vendor("Intel UHD Graphics") == "intel"
    assert parse_vendor("Foobar random controller") == "unknown"


def test_intel_low():
    out = "VGA compatible controller: Intel Corporation UHD Graphics 630"
    assert detect_gpu_class(out) == "low"


def test_amd_high():
    out = ("Advanced Micro Devices, Inc. [AMD/ATI] Navi 22 "
           "[Radeon RX 6700 XT]")
    assert detect_gpu_class(out) == "high"


def test_nvidia_high():
    out = "NVIDIA Corporation GP106 [GeForce GTX 1060]"
    assert detect_gpu_class(out) == "high"


def test_nvidia_ultra():
    out = "NVIDIA Corporation AD102 [GeForce RTX 4090]"
    assert detect_gpu_class(out) == "ultra"


def test_unknown_weak():
    assert detect_gpu_class("Some unrelated controller") == "weak"
