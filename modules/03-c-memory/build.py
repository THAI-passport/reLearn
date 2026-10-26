#!/usr/bin/env python3
"""Build module 03 targets.

build/{memmap,pointers,cstrings,nested,lifetime}   lab programs with symbols
build/overflow                                     off-by-one heap bug, built with AddressSanitizer
build/vault                                        demo of the challenge program with a known token (symbols)
challenge/vault                                    seeded challenge program (stripped)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
import relab  # noqa: E402

MODULE = "03"
REGIONS = ("global", "heap", "stack")

DEMO_TOKEN = "RE-demo1234"
DEMO_SPLIT = (3, 4)                      # lengths of pieces 1 and 2; piece 3 gets the rest
DEMO_NUMBERS = {"global": 2, "heap": 3, "stack": 1}


def expected() -> str:
    """The exact token a correct my-answer.txt must contain."""
    return relab.token(MODULE)


def plan(token: str, split: tuple, numbers: dict) -> dict:
    """Pieces of the token by region."""
    cuts = (split[0], split[0] + split[1])
    pieces = {1: token[:cuts[0]], 2: token[cuts[0]:cuts[1]], 3: token[cuts[1]:]}
    return {r: pieces[numbers[r]] for r in REGIONS}


def seeded() -> tuple:
    token = expected()
    split = (relab.derive_int(MODULE, "len1", 2, 4), relab.derive_int(MODULE, "len2", 2, 4))
    order = sorted(range(3), key=lambda i: relab.derive(MODULE, f"region{i}"))
    numbers = {r: order[i] + 1 for i, r in enumerate(REGIONS)}
    return token, split, numbers


def defines(token: str, split: tuple, numbers: dict, decoys: list) -> dict:
    pieces = plan(token, split, numbers)
    d = {f"P_{r.upper()}": relab.c_string(pieces[r]) for r in REGIONS}
    d.update({f"N_{r.upper()}": numbers[r] for r in REGIONS})
    d.update({f"DECOY{i + 1}": relab.c_string(v) for i, v in enumerate(decoys)})
    return d


def main() -> int:
    src = HERE / "src"
    build = HERE / "build"
    for name in ("memmap", "pointers", "cstrings", "nested", "lifetime"):
        relab.compile_c(src / f"{name}.c", build / name, debug=True)
    relab.compile_c(src / "overflow.c", build / "overflow", debug=True,
                    extra=["-fsanitize=address", "-fno-omit-frame-pointer"])

    demo_decoys = ["demo-before-1", "demo-after-1", "demo-before-2", "demo-after-2", "demo-before-3", "demo-after-3"]
    relab.compile_c(src / "vault.c", build / "vault", debug=True,
                    defines=defines(DEMO_TOKEN, DEMO_SPLIT, DEMO_NUMBERS, demo_decoys))

    token, split, numbers = seeded()
    decoys = [relab.token(MODULE, f"decoy{i}", prefix="RE-", length=8) for i in range(6)]
    out = relab.compile_c(src / "vault.c", HERE / "challenge" / "vault",
                          defines=defines(token, split, numbers, decoys))
    relab.strip(out)
    print("Built build/{memmap,pointers,cstrings,nested,lifetime,overflow,vault} and challenge/vault (stripped).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
