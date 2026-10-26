#!/usr/bin/env python3
"""Build track S1.1 (MBA with Z3) targets.

build/identities     three versions of x + y (plain and two MBA forms) at -O0, with symbols
build/identities-O2  the same source at -O2, to see what the optimizer does to MBA
challenge/gate       stripped; accepts one number and prints "open" only for the right one.
                     Its check is a seeded affine function hidden behind seeded MBA rewrites.

The generated header with the expression is written to a temporary folder and deleted, so
the only place the expression exists is the binary.
"""
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
import relab  # noqa: E402

MODULE = "S1.1"
MASK = 0xFFFFFFFF


class Picker:
    """Deterministic choices from the learner's seed."""

    def __init__(self):
        self.n = 0

    def pick(self, k: int) -> int:
        self.n += 1
        return relab.derive_int(MODULE, f"choice{self.n}", 0, k - 1)

    def const(self, lo: int = 1, hi: int = MASK) -> int:
        self.n += 1
        return relab.derive_int(MODULE, f"const{self.n}", lo, hi)


# Expression trees: ("x",) ("c", v) ("not", a) (op, a, b) with op in xor or and add sub mul.

def ev(e, x: int) -> int:
    t = e[0]
    if t == "x":
        return x
    if t == "c":
        return e[1]
    if t == "not":
        return ~ev(e[1], x) & MASK
    a, b = ev(e[1], x), ev(e[2], x)
    return {"xor": a ^ b, "or": a | b, "and": a & b, "add": (a + b) & MASK,
            "sub": (a - b) & MASK, "mul": (a * b) & MASK}[t]


def emit(e) -> str:
    t = e[0]
    if t == "x":
        return "(x)"
    if t == "c":
        return f"0x{e[1]:08x}u"
    if t == "not":
        return f"(~{emit(e[1])})"
    sym = {"xor": "^", "or": "|", "and": "&", "add": "+", "sub": "-", "mul": "*"}[t]
    return f"({emit(e[1])} {sym} {emit(e[2])})"


def c(v):
    return ("c", v & MASK)


def rewrite(e, depth: int, p: Picker):
    """Replace + and ^ with equivalent MBA forms (identities valid modulo 2^n for every n)."""
    if e[0] in ("x", "c") or depth == 0:
        return e
    if e[0] == "not":
        return ("not", rewrite(e[1], depth - 1, p))
    a, b = rewrite(e[1], depth - 1, p), rewrite(e[2], depth - 1, p)
    if e[0] == "xor":
        return [
            ("sub", ("or", a, b), ("and", a, b)),                                  # a^b = (a|b) - (a&b)
            ("sub", ("add", a, b), ("mul", c(2), ("and", a, b))),                  # a^b = (a+b) - 2(a&b)
            ("or", ("and", ("not", a), b), ("and", a, ("not", b))),                # a^b = (~a&b) | (a&~b)
        ][p.pick(3)]
    if e[0] == "add":
        return [
            ("add", ("xor", a, b), ("mul", c(2), ("and", a, b))),                  # a+b = (a^b) + 2(a&b)
            ("add", ("or", a, b), ("and", a, b)),                                  # a+b = (a|b) + (a&b)
            ("sub", ("mul", c(2), ("or", a, b)), ("xor", a, b)),                   # a+b = 2(a|b) - (a^b)
        ][p.pick(3)]
    return (e[0], a, b)


def zero_term(p: Picker):
    """k * ((x|m) - (x&m) - (x^m)), which is always 0."""
    m = c(p.const())
    x = ("x",)
    return ("mul", c(p.const(2, 0xFFFF)), ("sub", ("sub", ("or", x, m), ("and", x, m)), ("xor", x, m)))


def challenge():
    """Return (expression tree, plain description, accepted input, target)."""
    p = Picker()
    k1, k2, k3 = p.const(), p.const(), p.const()
    plain = ("xor", ("add", ("xor", ("x",), c(k1)), c(k2)), c(k3))     # ((x ^ k1) + k2) ^ k3
    tree = rewrite(plain, 3, p)
    tree = ("add", tree, zero_term(p))
    tree = ("sub", tree, zero_term(p))
    secret = relab.derive_int(MODULE, "input", 0, MASK)
    return tree, plain, secret, ev(plain, secret)


def expected() -> int:
    return challenge()[2]


def main() -> int:
    tree, plain, secret, target = challenge()
    for i in range(2000):                                             # self-check the rewrites
        x = relab.derive_int(MODULE, f"probe{i}", 0, MASK)
        assert ev(tree, x) == ev(plain, x), "MBA rewrite is not equivalent"
    src = HERE / "src"
    relab.compile_c(src / "identities.c", HERE / "build" / "identities", debug=True)
    relab.compile_c(src / "identities.c", HERE / "build" / "identities-O2", opt="-O2", debug=True)
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "gate_expr.h").write_text(
            f"#define GATE_EXPR(x) {emit(tree)}\n#define TARGET 0x{target:08x}u\n")
        gate = relab.compile_c(src / "gate.c", HERE / "challenge" / "gate", extra=[f"-I{tmp}"])
    relab.strip(gate)
    print("Built build/identities, build/identities-O2, and challenge/gate (stripped).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
