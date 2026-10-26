# Challenge: Open the gate

`challenge/gate` is stripped. It takes one number and prints `open` or `closed`:
```bash
./challenge/gate 12345
```
Exactly one 32-bit value opens it. The check is a short function hidden behind seeded MBA
rewrites, so every learner's gate is different.

Find the value, write it to `my-answer.txt` (decimal or `0x` hex), and run `python3 check.py`.

Rules
- Do not brute-force the binary by running it 2^32 times. The point is to read the check.
- Allowed: `strings`, `objdump`, Ghidra, Z3, your own scripts. A debugger is allowed for
  confirming a value, not for searching.
- Write down the plain (deobfuscated) function you recovered. The tutor will ask for it.

Run `make` first.
