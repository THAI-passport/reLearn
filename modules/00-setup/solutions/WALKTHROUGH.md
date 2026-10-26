# Module 00 walkthrough (reveal only after an attempt, see the hint ladder in AGENTS.md)

1. `file challenge/mystery` shows a stripped x86_64 executable (Mach-O on macOS, ELF on Linux).
2. `nm challenge/mystery` no longer lists `_secret` or `_main`: `strip` removed the symbol table entries
   that only help humans and debuggers.
3. The token is a string constant, so its bytes are stored verbatim in the read-only data
   (`__TEXT,__cstring` or `__TEXT,__const` on Mach-O, `.rodata` on ELF). Stripping does not touch data.
4. `strings challenge/mystery | grep RE-` prints it.

Explain back: why would XOR-encoding the token have defeated this approach, and what would you
need instead? (Answer comes in module 01's challenge.)
