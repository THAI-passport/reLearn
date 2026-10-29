#!/usr/bin/env python3
"""Reference solver for module 04 (tutor use, behind the hint ladder).

Takes the printable fragments that `strings` finds in the stripped gate program, tries every ordered
pair joined together as a password, and prints the pair the program accepts. The learner's route is
the decompiler: it shows which piece is copied first, and the order is the whole puzzle.
"""
import itertools
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
GATE = str(HERE / "challenge" / "gate")

data = Path(GATE).read_bytes()
fragments = sorted({m.decode() for m in re.findall(rb"[A-Za-z0-9-]{3,12}", data)})

for a, b in itertools.permutations(fragments, 2):
    candidate = a + b
    if len(candidate) != 15:
        continue
    run = subprocess.run([GATE, candidate], capture_output=True, text=True)
    if run.returncode == 0 and "granted" in run.stdout:
        print(candidate)
        sys.exit(0)
sys.exit("no pair of fragments was accepted")
