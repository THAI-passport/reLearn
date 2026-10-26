#!/usr/bin/env python3
"""Check the reverse engineering toolchain on this machine and print the platform route.

Usage: python3 tools/check_env.py
Exit code is 0 when all REQUIRED tools are present and an x86_64 test program builds and runs.

Supported routes: macOS Intel, macOS Apple Silicon (x86_64 via Rosetta 2), Linux x86_64,
Linux ARM64 (x86_64 cross compiler + qemu-user, or RELAB_NATIVE=1), and Windows via WSL2.
"""
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import relab  # noqa: E402

SYSTEM = platform.system()

REQUIRED = {
    "C compiler": ["clang", "gcc", "cc"],
    "File type": ["file"],
    "Strings": ["strings"],
    "Hex dump": ["xxd"],
    "Symbols": ["nm"],
    "Disassembler (CLI)": ["objdump", "llvm-objdump"],
    "Strip": ["strip"],
    "Make": ["make"],
    "Python 3": ["python3"],
}
if SYSTEM == "Darwin":
    REQUIRED["Mach-O inspector"] = ["otool"]
    REQUIRED["Debugger"] = ["lldb"]
else:
    REQUIRED["ELF inspector"] = ["readelf"]
    REQUIRED["Debugger"] = ["gdb", "lldb"]

OPTIONAL = {
    "Ghidra (module 04)": ["ghidraRun", "ghidra"],
    "radare2 / Cutter (module 12)": ["r2", "radare2", "cutter"],
    "Frida (module 15)": ["frida"],
    "ImHex (module 17)": ["imhex"],
}
if SYSTEM == "Linux":
    OPTIONAL.update({"strace (module 14)": ["strace"], "ltrace (module 14)": ["ltrace"],
                     "qemu-x86_64 (ARM64 hosts)": ["qemu-x86_64"],
                     "x86_64 cross gcc (ARM64 hosts)": ["x86_64-linux-gnu-gcc"]})
OPTIONAL_PY = {"z3 (module 19, track S1)": "z3", "lief (module 08)": "lief", "unicorn (module 16)": "unicorn"}


def find(names):
    for name in names:
        path = shutil.which(name)
        if path:
            return path
    return None


def report(group, required):
    missing = 0
    for label, names in group.items():
        path = find(names)
        if path:
            print(f"  [ok]       {label:<32} {path}")
        else:
            print(f"  [{'MISSING' if required else 'optional'}] {' ' if required else ''}{label:<32} (looked for: {', '.join(names)})")
            missing += required
    return missing


def is_wsl():
    try:
        return "microsoft" in Path("/proc/version").read_text().lower()
    except OSError:
        return False


def route(h):
    if SYSTEM == "Darwin":
        if h["machine"] == "arm64" or h["rosetta"]:
            return ("macOS Apple Silicon: labs build with `clang -arch x86_64` and run under Rosetta 2.\n"
                    "  If x86_64 programs fail to start: softwareupdate --install-rosetta --agree-to-license")
        return "macOS Intel: labs build and run natively for x86_64."
    if SYSTEM == "Linux":
        prefix = "Windows via WSL2 (Linux track). Use a separate Windows VM for PE work (module 24).\n  " if is_wsl() else ""
        if h["machine"] in ("aarch64", "arm64"):
            return (prefix + "Linux ARM64: install gcc-x86-64-linux-gnu and qemu-user, or set RELAB_NATIVE=1\n"
                    "  for native ARM64 labs (lesson listings will not match).")
        return prefix + "Linux x86_64: labs build and run natively."
    if SYSTEM == "Windows":
        return "Native Windows is not supported. Install WSL2 (wsl --install) and run the course inside it."
    return f"Unrecognized OS {SYSTEM}; try the Linux route."


def shadowed():
    """On macOS, warn when PATH tools differ from Apple's (for example Anaconda cctools)."""
    notes = []
    if SYSTEM != "Darwin":
        return notes
    for name in ("nm", "otool", "strip", "strings"):
        on_path = shutil.which(name)
        apple = relab.apple_tool(name)
        if on_path and apple and os.path.realpath(on_path) != os.path.realpath(apple) \
                and not on_path.startswith("/usr/bin/"):
            notes.append(f"  `{name}` on PATH is {on_path}; Apple's is {apple} (use `xcrun {name}` if output differs)")
    return notes


def smoke_test():
    """Build and run a tiny x86_64 program the way the labs do."""
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "t.c"
        src.write_text('#include <stdio.h>\nint main(void){puts("ok");return 0;}\n')
        exe = Path(tmp) / "t"
        try:
            relab.compile_c(src, exe)
        except (subprocess.CalledProcessError, SystemExit) as e:
            return f"build failed ({e})"
        runner = []
        if SYSTEM == "Linux" and platform.machine().lower() in ("aarch64", "arm64") and not relab.native_requested():
            runner = [shutil.which("qemu-x86_64") or "qemu-x86_64", "-L", "/usr/x86_64-linux-gnu"]
        try:
            out = subprocess.run(runner + [str(exe)], capture_output=True, text=True, timeout=20)
        except (OSError, subprocess.TimeoutExpired) as e:
            return f"run failed ({e})"
        return None if out.stdout.strip() == "ok" else f"run failed (exit {out.returncode}) {out.stderr.strip()}"


def java_version():
    java = shutil.which("java")
    if not java:
        return None
    out = subprocess.run([java, "-version"], capture_output=True, text=True)
    text = out.stderr or out.stdout
    return text.splitlines()[0] if text else "unknown"


def main():
    h = relab.host()
    print("Host")
    print(f"  OS:            {SYSTEM} {platform.release()}")
    print(f"  CPU arch:      {h['machine']}" + (" (this Python runs under Rosetta)" if h["rosetta"] else ""))
    print(f"  Python:        {platform.python_version()}")
    print(f"  Java:          {java_version() or 'not found (Ghidra needs JDK 21+)'}")
    print(f"  Route:         {route(h)}")
    print()
    print("Required tools")
    missing = report(REQUIRED, True)
    print()
    print("Optional tools (installed when a module needs them)")
    report(OPTIONAL, False)
    for label, mod in OPTIONAL_PY.items():
        try:
            __import__(mod)
            print(f"  [ok]       {label:<32} python module {mod}")
        except ImportError:
            print(f"  [optional] {label:<32} (pip install {'z3-solver' if mod == 'z3' else mod})")
    notes = shadowed()
    if notes:
        print()
        print("PATH notes")
        print("\n".join(notes))
    print()
    problem = smoke_test() if not missing else "skipped (required tools missing)"
    print(f"x86_64 build-and-run test: {'ok' if problem is None else problem}")
    print(f"Compiler command used by labs: {' '.join(relab.compiler())}")
    print()
    if missing or problem:
        print("Fix the items above (see README.md, 'Platform routes'), then re-run this script.")
        return 1
    print("All required tools found and an x86_64 program built and ran.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
