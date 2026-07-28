"""hardware/ — GPU/Session/Kernel-Erkennung (PURE, testbar).

gpu.py   : detect_gpu_class(lspci) -> Perf-Klasse
session.py: detect_session(environ) -> x11|wayland|tty|unknown
kernel.py : parse_kernel / ntsync_supported / ntsync_device_present
"""
