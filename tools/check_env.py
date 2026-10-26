#!/usr/bin/env python3
"""Check the reverse engineering toolchain on this machine.

Usage: python3 tools/check_env.py
Exit code is 0 when all REQUIRED tools are present, 1 otherwise.
"""
import platform
import shutil
import subprocess
import sys

REQUIRED = {
    "Compiler": ["clang", "gcc"],
    "File type": ["file"],
    "Strings": ["strings"],
    "Hex dump": ["xxd"],
    "Symbols": ["nm"],
    "Disassembler (CLI)": ["objdump"],
    "Debugger": ["lldb", "gdb"],
    "Python 3": ["python3"],
}

OPTIONAL = {
    "Mach-O inspector (macOS)": ["otool"],
    "ELF inspector (Linux)": ["readelf"],
    "Ghidra": ["ghidraRun", "ghidra"],
    "Cutter / radare2": ["cutter", "r2", "radare2"],
    "Frida": ["frida"],
    "Make": ["make"],
}


def find(names):
    for name in names:
        path = shutil.which(name)
        if path:
            return name, path
    return None, None


def report(group, required):
    missing = 0
    for label, names in group.items():
        name, path = find(names)
        if name:
            print(f"  [ok]      {label:<26} {path}")
        else:
            tag = "MISSING " if required else "optional"
            print(f"  [{tag}] {label:<26} (looked for: {', '.join(names)})")
            if required:
                missing += 1
    return missing


def java_version():
    java = shutil.which("java")
    if not java:
        return None
    out = subprocess.run([java, "-version"], capture_output=True, text=True)
    return (out.stderr or out.stdout).splitlines()[0] if (out.stderr or out.stdout) else "unknown"


def main():
    print("Host")
    print(f"  OS:            {platform.system()} {platform.release()}")
    print(f"  CPU arch:      {platform.machine()}")
    print(f"  Python:        {platform.python_version()}")
    if platform.system() == "Darwin" and platform.machine() == "arm64":
        print("  Note: Apple Silicon. x86_64 labs are built with `clang -arch x86_64` and run under Rosetta.")
    print(f"  Java:          {java_version() or 'not found (needed for Ghidra)'}")
    print()
    print("Required tools")
    missing = report(REQUIRED, True)
    print()
    print("Optional tools")
    report(OPTIONAL, False)
    print()
    if missing:
        print(f"{missing} required tool group(s) missing. Install them, then re-run this script.")
        return 1
    print("All required tools found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
