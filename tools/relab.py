#!/usr/bin/env python3
"""Shared helpers for building seeded, non-googleable lab challenges.

Every module's build.py, check.py and solutions/solve.py import this file:

    import sys; from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
    import relab

Seeds
    Each learner gets a random 128-bit seed in `.seed` at the repo root (gitignored).
    Secrets are derived with HMAC-SHA256(seed, "<module>:<label>"), so every module and
    every label gets an independent value, and two learners never share answers.
    Set RELAB_SEED to override the seed (used by tools/selftest.py to test many seeds).

Toolchain
    Labs target x86_64. On macOS (Intel or Apple Silicon) we pass `-arch x86_64`; Apple
    Silicon runs the result under Rosetta 2. On Linux x86_64 the native compiler is used.
    On Linux aarch64 we look for an x86_64 cross compiler (see `compiler()`), or the
    learner sets RELAB_NATIVE=1 to build native ARM64 binaries (labs still work, but
    disassembly in the lessons will not match).
    CC overrides the compiler. On macOS, Apple's binutils are resolved with `xcrun` so a
    shadowing `strip`/`otool` from Anaconda or Homebrew does not change the result.

Command line (handy for authors):
    python3 tools/relab.py info            host, compiler, seed status
    python3 tools/relab.py token 00        print a module's default token (author use only)
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import os
import platform
import secrets
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED_FILE = ROOT / ".seed"


# --------------------------------------------------------------------------- seeds

def seed() -> str:
    """Return the learner's seed, creating `.seed` on first use."""
    env = os.environ.get("RELAB_SEED")
    if env:
        return env.strip()
    if not SEED_FILE.exists():
        SEED_FILE.write_text(secrets.token_hex(16) + "\n")
    return SEED_FILE.read_text().strip()


def derive(module: str, label: str = "token") -> bytes:
    """32 pseudorandom bytes, unique per (seed, module, label)."""
    return hmac.new(seed().encode(), f"{module}:{label}".encode(), hashlib.sha256).digest()


def token(module: str, label: str = "token", prefix: str = "RE-", length: int = 8) -> str:
    """A short printable token such as RE-3fa9c1d2."""
    return prefix + derive(module, label).hex()[:length]


def derive_int(module: str, label: str, lo: int, hi: int) -> int:
    """Integer in [lo, hi], derived from the seed."""
    n = int.from_bytes(derive(module, label), "big")
    return lo + n % (hi - lo + 1)


def derive_ident(module: str, label: str, prefix: str, length: int = 6) -> str:
    """A C identifier such as sink_7c2e01, for seeded symbol names."""
    return f"{prefix}{derive(module, label).hex()[:length]}"


# ----------------------------------------------------------------------- toolchain

def host() -> dict:
    system = platform.system()
    machine = platform.machine().lower()
    info = {"system": system, "machine": machine, "rosetta": False}
    if system == "Darwin" and machine == "x86_64":
        # A Python process translated by Rosetta reports x86_64 on Apple Silicon.
        out = subprocess.run(["sysctl", "-in", "sysctl.proc_translated"],
                             capture_output=True, text=True)
        info["rosetta"] = out.stdout.strip() == "1"
    return info


def native_requested() -> bool:
    return os.environ.get("RELAB_NATIVE") == "1"


def compiler() -> list[str]:
    """Compiler command plus the flags that select an x86_64 target."""
    h = host()
    if os.environ.get("CC"):
        cc = os.environ["CC"].split()
    else:
        name = next((n for n in ("clang", "gcc", "cc") if shutil.which(n)), None)
        if name is None:
            sys.exit("relab: no C compiler found (install clang or gcc, then run tools/check_env.py)")
        cc = [name]
    if native_requested():
        return cc
    if h["system"] == "Darwin":
        return cc + ["-arch", "x86_64"]
    if h["machine"] in ("x86_64", "amd64"):
        return cc
    if h["machine"] in ("aarch64", "arm64"):
        if os.environ.get("CC"):
            return cc
        cross = shutil.which("x86_64-linux-gnu-gcc")
        if cross:
            return [cross]
        sys.exit("relab: this is an ARM64 Linux host. Install an x86_64 cross compiler\n"
                 "  (Debian/Ubuntu: sudo apt install gcc-x86-64-linux-gnu qemu-user)\n"
                 "or set RELAB_NATIVE=1 to build native ARM64 labs.")
    return cc


def apple_tool(name: str) -> str:
    """Resolve an Apple binutil through xcrun so PATH shadowing does not matter."""
    out = subprocess.run(["xcrun", "--find", name], capture_output=True, text=True)
    path = out.stdout.strip()
    if out.returncode == 0 and path:
        return path
    return shutil.which(name) or name


def tool(name: str) -> str:
    if host()["system"] == "Darwin":
        return apple_tool(name)
    if name == "strip" and not native_requested() and host()["machine"] in ("aarch64", "arm64"):
        cross = shutil.which("x86_64-linux-gnu-strip")
        if cross:
            return cross
    return shutil.which(name) or name


def run(cmd: list, **kw) -> subprocess.CompletedProcess:
    kw.setdefault("check", True)
    return subprocess.run([str(c) for c in cmd], **kw)


def compile_c(sources, out: Path, *, defines: dict | None = None, opt: str = "-O0",
              debug: bool = False, object_only: bool = False, extra: list | None = None) -> Path:
    """Compile C sources for the course target. Returns the output path."""
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = compiler() + [opt]
    if debug:
        cmd.append("-g")
    if object_only:
        cmd.append("-c")
    for key, value in (defines or {}).items():
        cmd.append(f"-D{key}" if value is None else f"-D{key}={value}")
    cmd += list(extra or [])
    cmd += [str(s) for s in ([sources] if isinstance(sources, (str, Path)) else sources)]
    cmd += ["-o", str(out)]
    run(cmd)
    return out


def strip(path: Path, *, local_only: bool = False) -> None:
    """Strip symbols. local_only keeps global symbols (needed for object files)."""
    run([tool("strip")] + (["-x"] if local_only else []) + [str(path)])


def c_string(value: str) -> str:
    """Quote a value for use in -DNAME=... on the command line."""
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def c_bytes(data: bytes) -> str:
    """Render bytes as a C initializer list: {0x12,0x34,...}."""
    return "{" + ",".join(f"0x{b:02x}" for b in data) + "}"


# ------------------------------------------------------------------------ checking

def answer_arg(module_dir: Path, default: str = "my-answer.txt") -> Path:
    """Parse --answer-file (used by selftest) and return the path to read."""
    p = argparse.ArgumentParser(add_help=True)
    p.add_argument("--answer-file", default=str(Path(module_dir) / default))
    return Path(p.parse_args().answer_file)


def read_answer(path: Path, hint: str) -> str | None:
    if not path.exists():
        print(f"FAIL: {hint}")
        return None
    return path.read_text().strip()


def verdict(ok: bool, pass_msg: str, fail_msg: str) -> int:
    print(("PASS: " + pass_msg) if ok else ("FAIL: " + fail_msg))
    return 0 if ok else 1


# ------------------------------------------------------------------------------ cli

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("info")
    t = sub.add_parser("token")
    t.add_argument("module")
    t.add_argument("label", nargs="?", default="token")
    a = p.parse_args()
    if a.cmd == "info":
        h = host()
        print(f"host:      {h['system']} {h['machine']}" + (" (Rosetta)" if h["rosetta"] else ""))
        print(f"compiler:  {' '.join(compiler())}")
        print(f"strip:     {tool('strip')}")
        print(f"seed file: {SEED_FILE} ({'present' if SEED_FILE.exists() else 'created on first build'})")
    else:
        print(token(a.module, a.label))
    return 0


if __name__ == "__main__":
    sys.exit(main())
