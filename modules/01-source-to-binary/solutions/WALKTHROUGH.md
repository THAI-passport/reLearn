# Module 01 walkthrough (reveal only after an attempt; see the hint ladder in AGENTS.md)

Hint ladder suggestions for the tutor:
1. "What kind of file is vault.o, and can you run it?"
2. "Which tool lists what an object file defines and what it needs?"
3. "Look at the `U` lines. Which of them would the C library provide?"
4. "Write a main.c that defines the missing function so it prints its argument, then calls the exported functions."

## Steps
1. `file challenge/vault.o`: a relocatable x86_64 object, not an executable.
2. `strings challenge/vault.o` shows the decoy message and a few bytes of noise, but no token: the token is XOR-encoded in a data array and decoded at run time.
3. `nm challenge/vault.o` (names differ per learner; this run used one seed):
   - two `T` symbols named `_vault_<hex>`: exported functions you can call.
   - `U _sink_<hex>`: the function you must provide.
   - `U ___stack_chk_fail` and `U ___stack_chk_guard`: stack protector support from the C library
     (the vault function has a local char buffer). Leave them to libc.
   - local symbols were stripped with `strip -x`; the decoder survives only as an anonymous `t` label.
   On Linux the names have no leading underscore.
4. Write `work/main.c`, dropping the leading underscore from the Mach-O names:
   ```c
   #include <stdio.h>
   void sink_XXXXXX(const char *m) { printf("%s\n", m); }
   void vault_AAAAAA(void);
   void vault_BBBBBB(void);
   int main(void) { vault_AAAAAA(); vault_BBBBBB(); return 0; }
   ```
5. `clang -arch x86_64 work/main.c challenge/vault.o -o work/open && ./work/open`
   One call prints the decoy message, the other prints the token.

`solutions/solve.py` automates exactly these steps.

## Explain back
- Why did linking fail if `sink_...` was declared but not defined in `main.c`?
- Why did `___stack_chk_fail` not need a definition from you?
- Why could `strip -x` not remove the `_vault_` and `_sink_` names from the object file?
