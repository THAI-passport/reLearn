# Challenge: Recover the password

`challenge/gate` is stripped. It accepts exactly one password:
```bash
./challenge/gate <password>
```
It prints `access granted` or `access denied`. The password is never stored whole: the program builds it at run time from two pieces, so `strings` shows only fragments.

Your task: import `challenge/gate` into Ghidra, find the function that builds the expected password, read the decompiler output to see which piece comes first, and write the password on one line to `my-answer.txt`. Then run `python3 check.py`.

Rules
- Use the decompiler view. Do not guess by trying fragment pairs against the program; the point is to read how the string is built.
- Be ready to explain to the tutor which function does the work, what its decompiled form shows, and which parts of it the decompiler named for you versus which you named.

Run `make` first. Every learner's password is different.
