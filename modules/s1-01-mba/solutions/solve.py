#!/usr/bin/env python3
"""Reference solver for track S1.1 (tutor use, behind the hint ladder). Needs z3-solver.

Does what the learner does, mechanically:
1. Disassemble the stripped gate binary and find `call <gate>` followed by `cmp eax, TARGET`.
2. Lift the gate function's x86_64 instructions into a Z3 bit-vector expression
   (input in edi, result in eax), tracking registers and stack slots.
3. Ask Z3 for an x with gate(x) == TARGET, and prove that it is the only one.
"""
import re
import subprocess
import sys
from pathlib import Path

try:
    import z3
except ImportError:
    sys.exit("z3 is missing: python3 -m pip install z3-solver (inside a virtual environment)")

HERE = Path(__file__).resolve().parent.parent
GATE = HERE / "challenge" / "gate"

listing = subprocess.run(["objdump", "-d", "-M", "intel", "--no-show-raw-insn", str(GATE)],
                         capture_output=True, text=True, check=True).stdout
lines = []
for raw in listing.splitlines():
    m = re.match(r"\s*([0-9a-f]+):\s+(\S+)\s*(.*)$", raw)
    if m:
        operands = re.sub(r"\s*(#|##|<).*$", "", m.group(3)).strip().lower()
        lines.append((int(m.group(1), 16), m.group(2).lower(), operands))

# 1. Find the call to gate and the target constant compared right after it.
gate_addr = target = None
for (a, mn, ops), (_, mn2, ops2) in zip(lines, lines[1:]):
    if mn.startswith("call") and mn2 == "cmp" and re.match(r"eax,\s*-?0x[0-9a-f]+$", ops2):
        gate_addr = int(re.match(r"(?:0x)?([0-9a-f]+)", ops).group(1), 16)
        target = int(ops2.split(",")[1].strip(), 16) & 0xFFFFFFFF
        break
if gate_addr is None:
    sys.exit("could not find `call gate; cmp eax, TARGET`")

# 2. Lift the gate function.
REG32 = {}
for names in (("rax", "eax"), ("rbx", "ebx"), ("rcx", "ecx"), ("rdx", "edx"), ("rsi", "esi"),
              ("rdi", "edi"), ("r8", "r8d"), ("r9", "r9d"), ("r10", "r10d"), ("r11", "r11d")):
    for n in names:
        REG32[n] = names[1]

x = z3.BitVec("x", 32)
regs = {"edi": x}
mem = {}


def slot(op: str) -> str:
    return re.sub(r"\s+", "", op.split("ptr", 1)[-1])


def read(op: str):
    op = op.strip()
    if "[" in op:
        return mem[slot(op)]
    if op in REG32:
        return regs[REG32[op]]
    return z3.BitVecVal(int(op, 16) & 0xFFFFFFFF, 32)


def write(op: str, val):
    op = op.strip()
    if "[" in op:
        mem[slot(op)] = val
    else:
        regs[REG32[op]] = val


def lea(op: str):
    total = z3.BitVecVal(0, 32)
    for sign, term in re.findall(r"([+-]?)\s*([^+-]+)", op.strip("[] ")):
        term = term.strip()
        if "*" in term:
            a, b = term.split("*")
            v = (read(a) * read(b)) if a in REG32 else (read(b) * int(a, 0))
        else:
            v = read(term)
        total = total - v if sign == "-" else total + v
    return total


body = [l for l in lines if l[0] >= gate_addr]
for addr, mn, ops in body:
    args = [o.strip() for o in ops.split(",")] if ops else []
    if mn in ("push", "pop", "nop", "endbr64"):
        continue
    if mn == "ret":
        break
    if mn == "mov":
        if args[1] in ("rsp", "rbp") or args[0] in ("rbp", "rsp"):
            continue
        write(args[0], read(args[1]))
    elif mn == "lea":
        write(args[0], lea(args[1]))
    elif mn in ("add", "sub", "and", "or", "xor"):
        a, b = read(args[0]), read(args[1])
        write(args[0], {"add": a + b, "sub": a - b, "and": a & b, "or": a | b, "xor": a ^ b}[mn])
    elif mn == "not":
        write(args[0], ~read(args[0]))
    elif mn == "neg":
        write(args[0], -read(args[0]))
    elif mn in ("shl", "sal", "shr", "sar"):
        n = read(args[1]) if len(args) > 1 else z3.BitVecVal(1, 32)
        v = read(args[0])
        write(args[0], v << n if mn in ("shl", "sal") else (z3.LShR(v, n) if mn == "shr" else v >> n))
    elif mn == "imul":
        if len(args) == 3:
            write(args[0], read(args[1]) * read(args[2]))
        else:
            write(args[0], read(args[0]) * read(args[1]))
    else:
        sys.exit(f"unsupported instruction at {addr:#x}: {mn} {ops}")

f = regs["eax"]

# 3. Solve, then prove uniqueness.
s = z3.Solver()
s.add(f == target)
if s.check() != z3.sat:
    sys.exit("no solution")
answer = s.model()[x].as_long()
s.add(x != answer)
if s.check() != z3.unsat:
    sys.exit("more than one input opens the gate")
print(answer)
