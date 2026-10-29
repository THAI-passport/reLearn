#!/usr/bin/env python3
"""Build module 04 targets.

build/{pointers,cstrings,nested}            module 03 programs with symbols (lab reference)
build/{pointers,cstrings,nested}-stripped   the same programs, stripped
build/gate                                  demo password checker with a known password (symbols)
challenge/gate                              seeded password checker (stripped)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
import relab  # noqa: E402

MODULE = "04"
LAB_SOURCES = HERE.parent / "03-c-memory" / "src"
DEMO_PASSWORD = "open-sesame"
DEMO_SPLIT = 4


def expected() -> str:
    """The exact password a correct my-answer.txt must contain."""
    return relab.token(MODULE, length=12)


def defines(password: str, split: int, swap: bool) -> dict:
    left, right = password[:split], password[split:]
    # PIECE_A holds whichever half comes second when swap is set, so declaration order and use order differ.
    a, b = (right, left) if swap else (left, right)
    first, second = ("piece_b", "piece_a") if swap else ("piece_a", "piece_b")
    return {"PIECE_A": relab.c_string(a), "PIECE_B": relab.c_string(b), "FIRST": first, "SECOND": second}


def main() -> int:
    build = HERE / "build"
    for name in ("pointers", "cstrings", "nested"):
        relab.compile_c(LAB_SOURCES / f"{name}.c", build / name, debug=True)
        stripped = relab.compile_c(LAB_SOURCES / f"{name}.c", build / f"{name}-stripped")
        relab.strip(stripped)
    relab.compile_c(HERE / "src" / "gate.c", build / "gate", debug=True,
                    defines=defines(DEMO_PASSWORD, DEMO_SPLIT, swap=True))
    password = expected()
    split = relab.derive_int(MODULE, "split", 5, 9)
    swap = relab.derive_int(MODULE, "swap", 0, 1) == 1
    out = relab.compile_c(HERE / "src" / "gate.c", HERE / "challenge" / "gate",
                          defines=defines(password, split, swap))
    relab.strip(out)
    print("Built build/{pointers,cstrings,nested}[-stripped], build/gate, and challenge/gate (stripped).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
