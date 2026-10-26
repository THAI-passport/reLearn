#!/usr/bin/env python3
"""Build module NN targets: build/<lab> (symbols) and challenge/<name> (stripped, seeded)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
import relab  # noqa: E402

MODULE = "NN"


def expected() -> str:
    """The exact content a correct my-answer.txt must have (after strip())."""
    return relab.token(MODULE)


def main() -> int:
    src = HERE / "src" / "lab.c"
    defines = {"TOKEN": relab.c_string(expected())}
    relab.compile_c(src, HERE / "build" / "lab", defines=defines, debug=True)
    out = relab.compile_c(src, HERE / "challenge" / "mystery", defines=defines)
    relab.strip(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
