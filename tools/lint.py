#!/usr/bin/env python3
"""Repository lint: cheap checks for the rules in AGENTS.md and CONTRIBUTING.md.

    python3 tools/lint.py

Checks (exit 1 if any fails):
  1. Python files compile.
  2. No emojis in tracked text files.
  3. No build outputs, learner answers, or seeds are tracked.
  4. Every built module has README.md, build.py, check.py, Makefile, challenge/CHALLENGE.md,
     solutions/WALKTHROUGH.md and solutions/solve.py.
  5. Every captured-output comment in a lesson names a command (`<!-- captured: ... -->`).
"""
from __future__ import annotations

import py_compile
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿⭐⭕️‍]")
MODULE_FILES = ("README.md", "build.py", "check.py", "Makefile", "challenge/CHALLENGE.md",
                "solutions/WALKTHROUGH.md", "solutions/solve.py")
FORBIDDEN = (re.compile(r"(^|/)\.seed$"), re.compile(r"(^|/)my-answer\.txt$"),
             re.compile(r"^modules/[^/]+/(build|work)/"),
             re.compile(r"^modules/[^/]+/challenge/(?!CHALLENGE\.md$)"))


def tracked() -> list[str]:
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True)
    return [p for p in out.stdout.splitlines() if (ROOT / p).is_file()]


def main() -> int:
    errors: list[str] = []
    files = tracked()

    with tempfile.TemporaryDirectory() as tmp:
        for p in files:
            if p.endswith(".py"):
                try:
                    py_compile.compile(str(ROOT / p), cfile=str(Path(tmp) / "x.pyc"), doraise=True)
                except py_compile.PyCompileError as e:
                    errors.append(f"{p}: does not compile: {e.msg.strip()}")

    for p in files:
        for pat in FORBIDDEN:
            if pat.search(p):
                errors.append(f"{p}: build output, seed, or learner answer must not be tracked")
        if p.endswith((".md", ".py", ".c", ".h", ".yml", ".json", ".txt")) or p in ("Makefile", "LICENSE"):
            text = (ROOT / p).read_text(encoding="utf-8", errors="replace")
            for n, line in enumerate(text.splitlines(), 1):
                if EMOJI.search(line):
                    errors.append(f"{p}:{n}: emoji")
            if p.startswith("modules/") and p.endswith("README.md"):
                for n, line in enumerate(text.splitlines(), 1):
                    if "<!-- captured" in line and not re.search(r"captured:\s*\S", line):
                        errors.append(f"{p}:{n}: captured-output label names no command")

    for d in sorted((ROOT / "modules").iterdir()):
        if d.is_dir() and not d.name.startswith("_") and (d / "build.py").exists():
            for rel in MODULE_FILES:
                if not (d / rel).exists():
                    errors.append(f"modules/{d.name}: missing {rel}")

    for e in errors:
        print(f"lint: {e}")
    print("lint: OK" if not errors else f"lint: {len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
