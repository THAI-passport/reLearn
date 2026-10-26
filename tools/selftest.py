#!/usr/bin/env python3
"""Author self-test: build each module and prove its checker works.

    python3 tools/selftest.py            test every built module
    python3 tools/selftest.py 01 02      test selected modules (prefix match on folder name)

For each module and for two random seeds plus the learner's own seed:
  1. build.py builds the challenge,
  2. solutions/solve.py derives the answer from the built artifacts,
  3. check.py must PASS on that answer,
  4. check.py must FAIL on an obviously wrong answer,
  5. check.py must FAIL on the right answer for a different seed (proves answers are per learner).
The learner's own seed runs last, so the artifacts left on disk match their .seed.
The learner's my-answer.txt is never read or written.
"""
from __future__ import annotations

import os
import secrets
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULES = ROOT / "modules"


def py(script: Path, *args, env=None) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(script), *args], cwd=script.parent,
                          capture_output=True, text=True, env=env)


def testable(d: Path) -> bool:
    solver = d / "solutions" / "solve.py"
    return (d.is_dir() and not d.name.startswith("_") and (d / "build.py").exists()
            and (d / "check.py").exists() and solver.exists() and solver.stat().st_size > 200)


def check(mod: Path, answer: str, env) -> int:
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        f.write(answer)
    try:
        return py(mod / "check.py", "--answer-file", f.name, env=env).returncode
    finally:
        os.unlink(f.name)


def test_module(mod: Path) -> list[str]:
    failures = []
    seeds = [secrets.token_hex(16), secrets.token_hex(16), None]
    answers = {}
    for seed in seeds:
        label = "own seed" if seed is None else f"seed {seed[:6]}"
        env = dict(os.environ)
        env.pop("RELAB_SEED", None)
        if seed:
            env["RELAB_SEED"] = seed
        b = py(mod / "build.py", env=env)
        if b.returncode:
            failures.append(f"{label}: build failed\n{b.stdout}{b.stderr}")
            continue
        s = py(mod / "solutions" / "solve.py", env=env)
        if s.returncode or not s.stdout.strip():
            failures.append(f"{label}: solver failed\n{s.stdout}{s.stderr}")
            continue
        answer = s.stdout
        answers[seed] = answer
        right = check(mod, answer, env)
        wrong = check(mod, "definitely-not-the-answer\n", env)
        print(f"    {label:<14} right answer -> {'PASS' if right == 0 else 'FAIL'}, "
              f"wrong answer -> {'FAIL' if wrong else 'PASS'}")
        if right != 0:
            failures.append(f"{label}: checker rejected the solver's answer")
        if wrong == 0:
            failures.append(f"{label}: checker accepted a wrong answer")
    # Cross-seed: the answer for seed 1 must fail under the learner's own seed.
    if seeds[0] in answers and None in answers and answers[seeds[0]] != answers[None]:
        env = dict(os.environ)
        env.pop("RELAB_SEED", None)
        cross = check(mod, answers[seeds[0]], env)
        print(f"    cross-seed     other learner's answer -> {'FAIL' if cross else 'PASS'}")
        if cross == 0:
            failures.append("checker accepted another seed's answer")
    elif seeds[0] in answers and None in answers:
        failures.append("two seeds produced the same answer (challenge is not seeded)")
    return failures


def main() -> int:
    wanted = sys.argv[1:]
    mods = [d for d in sorted(MODULES.iterdir()) if testable(d)
            and (not wanted or any(d.name.startswith(w) for w in wanted))]
    if not mods:
        print("no testable modules matched")
        return 1
    total = 0
    for mod in mods:
        print(f"[{mod.name}]")
        fails = test_module(mod)
        for f in fails:
            print(f"    ERROR {f}")
        total += len(fails)
    print("selftest: OK" if not total else f"selftest: {total} problem(s)")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
