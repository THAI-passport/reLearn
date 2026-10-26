#!/usr/bin/env python3
"""Build module 02 targets.

build/bits, build/floats, build/layout   lab programs with symbols
build/stamp                              writes a demo record with known values (symbols)
challenge/stamp                          writes a seeded record (stripped)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
import relab  # noqa: E402

MODULE = "02"
FIELDS = ("version", "flags", "delta", "id", "ratio")

DEMO = {"version": 2, "flags": [0, 2, 8], "delta": -2, "id": 0x1122334455667788,
        "ratio": 1.5, "pad": 0xAA}


def expected() -> dict:
    """Field values of the seeded record, in the form check.py compares."""
    order = sorted(range(16), key=lambda b: relab.derive(MODULE, f"flagbit{b}"))
    count = relab.derive_int(MODULE, "flagcount", 3, 6)
    k = relab.derive_int(MODULE, "ratio", -4000, 4000)
    if k % 8 == 0:
        k += 3                                   # keep a fractional part; k/8 stays exact in a float
    return {
        "version": relab.derive_int(MODULE, "version", 1, 9),
        "flags": sorted(order[:count]),
        "delta": -relab.derive_int(MODULE, "delta", 1000, 2_000_000),
        "id": relab.derive_int(MODULE, "id", 2**40, 2**63 - 1),
        "ratio": k / 8,
        "pad": relab.derive_int(MODULE, "pad", 0x80, 0xFE),
    }


def defines(v: dict) -> dict:
    return {
        "VERSION": v["version"],
        "FLAGS": hex(sum(1 << b for b in v["flags"])),
        "DELTA": f"({v['delta']})",
        "ID": f"{v['id']}ULL",
        "RATIO": f"({v['ratio']!r}f)",
        "PAD": hex(v["pad"]),
    }


def main() -> int:
    src = HERE / "src"
    build = HERE / "build"
    for name in ("bits", "floats", "layout"):
        relab.compile_c(src / f"{name}.c", build / name, debug=True)
    relab.compile_c(src / "stamp.c", build / "stamp", defines=defines(DEMO), debug=True)
    stamp = relab.compile_c(src / "stamp.c", HERE / "challenge" / "stamp", defines=defines(expected()))
    relab.strip(stamp)
    print("Built build/{bits,floats,layout,stamp} and challenge/stamp (stripped).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
