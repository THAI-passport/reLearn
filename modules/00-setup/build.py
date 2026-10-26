#!/usr/bin/env python3
"""Build module 00 targets.

Creates build/hello (with symbols) and challenge/mystery (stripped).
The secret token is derived from a local, gitignored seed (.seed at repo root),
so each learner has a different answer.
"""
import hashlib
import platform
import secrets
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SEED_FILE = ROOT / ".seed"
MODULE_ID = "00"


def get_seed() -> str:
    if not SEED_FILE.exists():
        SEED_FILE.write_text(secrets.token_hex(16))
    return SEED_FILE.read_text().strip()


def token(seed: str = None) -> str:
    seed = seed or get_seed()
    return "RE-" + hashlib.sha256((seed + MODULE_ID).encode()).hexdigest()[:8]


def compile_target(out: Path, extra: list) -> None:
    out.parent.mkdir(exist_ok=True)
    cmd = ["clang", "-O0", f'-DTOKEN="{token()}"', str(HERE / "src" / "hello.c"), "-o", str(out)]
    if platform.system() == "Darwin":
        cmd[1:1] = ["-arch", "x86_64"]
    cmd += extra
    subprocess.run(cmd, check=True)


def main() -> int:
    compile_target(HERE / "build" / "hello", ["-g"])
    compile_target(HERE / "challenge" / "mystery", [])
    subprocess.run(["strip", str(HERE / "challenge" / "mystery")], check=True)
    print("Built build/hello (symbols) and challenge/mystery (stripped).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
