#!/usr/bin/env python3
"""Reference solver for module 00 (tutor use, behind the hint ladder).

Does what `strings challenge/mystery | grep RE-` does: scans the stripped binary
for printable runs and prints the one that looks like a token.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
data = (HERE / "challenge" / "mystery").read_bytes()
found = re.findall(rb"RE-[0-9a-f]{8}", data)
if not found:
    sys.exit("no token found; run `make` first")
print(found[0].decode())
