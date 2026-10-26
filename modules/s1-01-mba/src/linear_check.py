#!/usr/bin/env python3
"""linear_check.py: decide a LINEAR MBA identity without a solver.

A linear MBA expression is a sum of constants times bitwise functions of the variables,
for example 2*(x & y) + 3*~(x | y) - 5. Every bit position of a bitwise function depends
only on the same bit position of the inputs, so such an expression is zero for all n-bit
inputs exactly when it is zero for the inputs where every variable is 0 or all ones.
With two variables that is 4 evaluations instead of 2^64.

Usage: python3 src/linear_check.py
"""
from itertools import product

MASK = 0xFFFFFFFF
CANDIDATES = {
    "x + y == (x ^ y) + 2*(x & y)": lambda x, y: ((x ^ y) + 2 * (x & y)) - (x + y),
    "x + y == (x | y) + (x & y) + 3*(~(x|y) - ~x - ~y + ~(x&y) + 1) - 3":
        lambda x, y: ((x | y) + (x & y) + 3 * (~(x | y) - ~x - ~y + ~(x & y) + 1) - 3) - (x + y),
    "x + y == (x ^ y) + (x & y)  (false)": lambda x, y: ((x ^ y) + (x & y)) - (x + y),
}

for text, diff in CANDIDATES.items():
    bad = [(x, y) for x, y in product((0, MASK), repeat=2) if diff(x, y) & MASK]
    verdict = "holds" if not bad else f"fails, e.g. x={bad[0][0]:#x}, y={bad[0][1]:#x}"
    print(f"{verdict:34} {text}")
