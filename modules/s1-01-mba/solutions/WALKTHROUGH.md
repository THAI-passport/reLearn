# Track S1.1 walkthrough (reveal only after an attempt; see the hint ladder in AGENTS.md)

Hint ladder suggestions for the tutor:
1. "Where does the program decide between open and closed? Look for the compare right after a call."
2. "The called function has no branches. Write down what each instruction does to eax, ecx, edx."
3. "Look for sub-expressions of the form (x | m) - (x & m) - (x ^ m). What is their value?"
4. "Put the lifted expression into Z3 as `f(x) == TARGET` with x a 32-bit BitVec."

## Steps
1. `strings challenge/gate` shows `open`, `closed`, and the usage message. The decision is in `main`.
2. `objdump -d -M intel --no-show-raw-insn challenge/gate`: `main` calls a function, then
   `cmp eax, <TARGET>` and `jne`. The called function is the gate.
3. The gate function is straight-line code on one input (`edi`, stored to a stack slot). Lift it.
   The generated structure (constants differ per learner) is:
   - the plain function `((x ^ k1) + k2) ^ k3`,
   - with each `^` and `+` rewritten by one of the identities from the lesson, three levels deep,
   - plus two zero terms `k * ((x | m) - (x & m) - (x ^ m))` added and subtracted.
4. Either simplify by hand (drop the zero terms, undo each identity) and invert
   `x = ((TARGET ^ k3) - k2) ^ k1`, or give the lifted expression to Z3 and solve `f(x) == TARGET`.
   Adding `x != first_solution` and getting `unsat` proves the answer is unique.

`solutions/solve.py` automates steps 2-4: it parses the listing, lifts the gate function to Z3
(registers and stack slots), solves, and proves uniqueness. It needs `z3-solver`.

## Explain back
- Why is the gate function a bijection, so that exactly one input works?
- Which part of the lifted expression would `src/linear_check.py` be able to simplify, and which not?
