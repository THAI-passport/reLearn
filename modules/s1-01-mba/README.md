# Track S1.1: Mixed Boolean-Arithmetic (MBA) with Z3

Kind: specialist track S1 (obfuscation and deobfuscation), first module. Time: about 6 hours.
Prerequisites: modules 02 and 07 (the rest of track S1 also needs 15 and 19).

## Context
Obfuscation transforms a program so it computes the same thing but is harder to understand. Mixed Boolean-Arithmetic mixes arithmetic operators (`+`, `-`, `*`) with bitwise ones (`&`, `|`, `^`, `~`) on fixed-width integers. Zhou, Main, Gu, and Johnson introduced it for software protection in 2007. It works because the two families do not mix in ordinary algebra: there are no simple distributive laws between `+` and `&`, so algebraic simplifiers, decompilers, and humans struggle. It also works because MBA costs almost nothing at run time.

MBA is now common in commercial protectors, in LLVM-based obfuscators, and in malware. It is also a research field of its own, with simplifiers such as MBA-Blast, SiMBA, and GAMBA, and with synthesis-based attacks (track S1.6). This module covers the core idea, how MBA looks in a binary, what a compiler and an SMT solver can and cannot do with it, and how to break a small MBA-protected check.

## Objectives
After this module you can:
- Explain why identities such as `x + y == (x ^ y) + 2*(x & y)` hold modulo 2^n.
- Recognize MBA patterns in x86_64 disassembly (including `~a` compiled as `xor reg, -0x1`).
- Prove or refute an MBA identity with Z3, and explain why some proofs time out.
- Decide a linear MBA identity with 2^t evaluations (t = number of variables).
- Lift an obfuscated function from disassembly into a Z3 expression and solve for an accepted input.
- Describe what the optimizer did and did not undo at `-O2`.

## Prerequisites
You can already:
- Use AND, OR, XOR, NOT, shifts, and two's complement arithmetic on 32-bit values (module 02).
- Read `-O0` and `-O2` x86_64 functions and map them to C (module 07).

## Setup
Install Z3 into a virtual environment at the repo root (`.venv/` is gitignored):
```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install z3-solver
cd modules/s1-01-mba
make
```
Captured output below comes from macOS 26 on Intel, Apple clang 17.0.0, and Python's `z3-solver` package. Timings depend on your machine and Z3 version.

## Guided steps

### 1. Why the identity holds
Predict: is `x + y == (x ^ y) + 2*(x & y)` true for all 32-bit `x` and `y`, including when the sum overflows?

Reason it out bit by bit. `x ^ y` is the sum of each bit position without carries. `x & y` marks the positions that produce a carry, and the carry moves one position left, which is `2*(x & y)`. Overflow does not matter, because both sides are computed modulo 2^32 and drop the same carry out of bit 31.

Run the lab program (the default arguments overflow on purpose):
```bash
./build/identities
./build/identities 7 9
```
<!-- captured: the commands above -->
```
plain 4001234567
mba1  4001234567
mba2  4001234567
plain 16
mba1  16
mba2  16
```
Read `add_mba2` in `src/identities.c`. It hides `x + y` behind a sub-expression that is always 1. Before reading on, find that sub-expression and convince yourself it equals 1, using `~a == -a - 1`.

### 2. MBA in the binary
```bash
objdump -d -M intel --no-show-raw-insn build/identities | less
```
`add_mba1` and `add_mba2` at `-O0` (excerpt, lines cut, none changed):
<!-- captured: objdump -d -M intel --no-show-raw-insn build/identities -->
```
0000000100000490 <_add_mba1>:
10000049a:     	mov	eax, dword ptr [rbp - 0x4]
10000049d:     	xor	eax, dword ptr [rbp - 0x8]
1000004a0:     	mov	ecx, dword ptr [rbp - 0x4]
1000004a3:     	and	ecx, dword ptr [rbp - 0x8]
1000004a6:     	shl	ecx
1000004a8:     	add	eax, ecx

00000001000004b0 <_add_mba2>:
1000004ba:     	mov	eax, dword ptr [rbp - 0x4]
1000004bd:     	or	eax, dword ptr [rbp - 0x8]
1000004c0:     	mov	ecx, dword ptr [rbp - 0x4]
1000004c3:     	and	ecx, dword ptr [rbp - 0x8]
1000004c6:     	add	eax, ecx
1000004c8:     	mov	ecx, dword ptr [rbp - 0x4]
1000004cb:     	or	ecx, dword ptr [rbp - 0x8]
1000004ce:     	xor	ecx, -0x1
1000004d1:     	mov	edx, dword ptr [rbp - 0x4]
1000004d4:     	xor	edx, -0x1
1000004d7:     	sub	ecx, edx
1000004d9:     	mov	edx, dword ptr [rbp - 0x8]
1000004dc:     	xor	edx, -0x1
1000004df:     	sub	ecx, edx
1000004e1:     	mov	edx, dword ptr [rbp - 0x4]
1000004e4:     	and	edx, dword ptr [rbp - 0x8]
1000004e7:     	xor	edx, -0x1
1000004ea:     	add	ecx, edx
1000004ec:     	add	ecx, 0x1
1000004ef:     	imul	ecx, ecx, 0x3
1000004f2:     	add	eax, ecx
1000004f4:     	sub	eax, 0x3
```
Patterns to recognize: `~a` appears as `xor reg, -0x1` (XOR with all ones), `2*a` as `shl reg` (shift left by one), and constant multipliers as `imul reg, reg, imm`. A long, branch-free run that alternates arithmetic and bitwise operations on the same few values is the visual signature of MBA.

Checkpoint: map each instruction of `_add_mba2` back to the C expression in `src/identities.c`.

### 3. What the optimizer does to MBA
Predict: at `-O2`, will clang turn both MBA functions back into a single `add`?
```bash
objdump -d -M intel --no-show-raw-insn build/identities-O2 | less
```
<!-- captured: objdump -d -M intel --no-show-raw-insn build/identities-O2 (the three functions) -->
```
0000000100000470 <_add_plain>:
100000470:     	push	rbp
100000471:     	mov	rbp, rsp
100000474:     	lea	eax, [rdi + rsi]
100000477:     	pop	rbp
100000478:     	ret

0000000100000480 <_add_mba1>:
100000480:     	push	rbp
100000481:     	mov	rbp, rsp
100000484:     	mov	eax, esi
100000486:     	xor	eax, edi
100000488:     	and	esi, edi
10000048a:     	lea	eax, [rax + 2*rsi]
10000048d:     	pop	rbp
10000048e:     	ret

0000000100000490 <_add_mba2>:
100000490:     	push	rbp
100000491:     	mov	rbp, rsp
100000494:     	lea	eax, [rdi + rsi]
100000497:     	pop	rbp
100000498:     	ret
```
With this compiler, the longer `add_mba2` was simplified completely, because its rewrites cancel through algebraic rules the optimizer knows. The shorter `add_mba1` survived, because no rule maps `(x ^ y) + 2*(x & y)` back to `x + y`. Lessons:
- Expression length says little about difficulty. What matters is whether some rewrite system knows the identity.
- Real obfuscators protect their MBA from the optimizer (opaque constants, splitting across functions, or applying the obfuscation after optimization). The challenge here is built at `-O0` for the same reason.
- Another compiler or version may simplify differently. Check your own output.

### 4. Proving identities with Z3
Z3 is an SMT solver. To prove `A == B` for all inputs, ask it to find inputs where `A != B`. The answer `unsat` (no such inputs) is a proof. Read `src/prove.py`, predict which line will be slowest, then run it with a 60-second limit per query:
```bash
python3 src/prove.py 60
```
<!-- captured: python3 src/prove.py 60 (z3-solver in a virtual environment) -->
```
mba1 width  1: unsat     0.00 s
mba1 width  8: unsat     0.02 s
mba1 width 16: unsat     0.02 s
mba1 width 32: unsat     0.03 s
mba2 width  1: unsat     0.00 s
mba2 width  8: unsat     5.89 s
mba2 width 16: unsat    11.53 s
mba2 width 32: unknown  60.01 s
```
`unknown` means Z3 gave up within the limit: no proof either way. Bit-vector solvers reduce the problem to a Boolean circuit, and multiplications mixed with bitwise operations make that circuit hard. This is exactly the property MBA obfuscation exploits. Also note that a 1-bit proof is not enough on its own: arithmetic mod 2 hides terms like `2*(x & y)`, which are always 0 in one bit.

Checkpoint: why does an obfuscator want identities that are cheap to execute but expensive to prove?

### 5. Linear MBA without a solver
A **linear** MBA expression is a sum of constants times bitwise functions of the variables, such as `2*(x & y) + 3*~(x | y) - 5`. Bit j of a bitwise function depends only on bit j of the inputs, so the whole expression is a sum over bit positions of 2^j times one small integer formula. Therefore:

> A linear MBA expression is zero for every n-bit input exactly when it is zero for the 2^t inputs where each of its t variables is either 0 or all ones.

```bash
python3 src/linear_check.py
```
<!-- captured: python3 src/linear_check.py -->
```
holds                              x + y == (x ^ y) + 2*(x & y)
holds                              x + y == (x | y) + (x & y) + 3*(~(x|y) - ~x - ~y + ~(x&y) + 1) - 3
fails, e.g. x=0xffffffff, y=0xffffffff x + y == (x ^ y) + (x & y)  (false)
```
Four evaluations settle the identity on which Z3 timed out. Linear-MBA simplifiers build on this kind of truth-table reasoning. The trick does **not** apply directly once bitwise operators are applied to arithmetic results (for example `~(2*(x | k) - (x ^ k))`); that is non-linear MBA, and it is what the challenge uses.

Checkpoint: explain in your own words why bit j of `x & y` cannot depend on bit j-1 of `x`, and why `x + y` can.

### 6. From listing to solver
To attack an MBA-protected check:
1. Find the check (strings, cross-references, the compare after the call).
2. Lift the protected function to an expression. At `-O0`, follow each stack slot and register: every `mov` copies a value, and every arithmetic or bitwise instruction builds a bigger expression.
3. Split off parts you can simplify: zero terms, linear sub-expressions, known identities.
4. Hand the rest to Z3 as a constraint `f(x) == target`. Finding one solution is often far easier than proving an identity for all inputs. Then ask Z3 whether a second solution exists.

## Challenge
Read `challenge/CHALLENGE.md`.

## Checkpoint
1. Prove `x + y == (x ^ y) + 2*(x & y)` modulo 2^n in words.
2. Why can Z3 solve `f(x) == target` for the challenge in about a second, yet time out proving `add_mba2` for all inputs?
3. What does `xor reg, -0x1` mean, and why does a compiler emit it?
4. Why did `-O2` remove one MBA and not the other, and what does that imply for protector design?
5. (Module 02) At the machine level these identities also hold for signed values. Why, and why is relying on signed overflow in C source still a bug (undefined behavior)?

Transfer task: the tutor generates an unseen function with a different MBA (for example, a disguised `x - y` plus a zero term). Recover the plain expression and prove the equivalence.

Review-queue seeds: the carry argument for `x + y`; the 0/all-ones test for linear MBA and its limit; why `unknown` is not `sat`; the signature of MBA in a listing.

## Further reading
See `resources.md`, section "Obfuscation and deobfuscation", for the MBA papers and simplifiers named here.
