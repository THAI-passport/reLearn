#!/usr/bin/env python3
"""prove.py: ask Z3 whether two MBA forms equal x + y, at several bit widths.

Usage: python3 src/prove.py [timeout_seconds]   (needs: python3 -m pip install z3-solver)

For each form and width we ask: "is there any x, y where form(x, y) != x + y?"
unsat means no such inputs exist, so the identity holds at that width.
"""
import sys
import time

import z3

FORMS = {
    "mba1": lambda x, y: (x ^ y) + 2 * (x & y),
    "mba2": lambda x, y: (x | y) + (x & y) + 3 * (~(x | y) - ~x - ~y + ~(x & y) + 1) - 3,
}
timeout = int(sys.argv[1]) if len(sys.argv) > 1 else 60

for name, form in FORMS.items():
    for width in (1, 8, 16, 32):
        x, y = z3.BitVecs("x y", width)
        s = z3.Solver()
        s.set("timeout", timeout * 1000)
        s.add(form(x, y) != x + y)
        start = time.time()
        result = s.check()
        print(f"{name} width {width:2}: {str(result):7} {time.time() - start:6.2f} s")
