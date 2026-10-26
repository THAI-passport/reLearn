#!/usr/bin/env python3
"""Build module 00 targets.

Creates build/hello (with symbols) and challenge/mystery (stripped).
The token is derived from the learner's local seed (tools/relab.py), so each
learner has a different answer.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
import relab  # noqa: E402

MODULE = "00"


def token() -> str:
    return relab.token(MODULE)


def main() -> int:
    src = HERE / "src" / "hello.c"
    defines = {"TOKEN": relab.c_string(token())}
    relab.compile_c(src, HERE / "build" / "hello", defines=defines, debug=True)
    mystery = relab.compile_c(src, HERE / "challenge" / "mystery", defines=defines)
    relab.strip(mystery)
    print("Built build/hello (symbols) and challenge/mystery (stripped).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
