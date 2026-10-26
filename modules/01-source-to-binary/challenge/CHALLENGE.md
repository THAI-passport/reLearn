# Challenge: Open the vault

`vault.o` is an object file compiled from C that you do not have. One of its exported functions
decodes a token (it starts with `RE-`) and hands it to a function that `vault.o` does not define.
Your job is to supply that missing function, link a program around the object file, and make it
print the token.

Rules
- Use only command-line tools from this module (`file`, `nm`, `strings`, `objdump -r`, the compiler).
  No debugger, no decompiler.
- Every undefined function you have to provide takes one argument, `const char *`, and returns nothing.
- Some undefined symbols are supplied by the C library. Work out which ones are yours.
- The object file was built for x86_64. Your program must be too (`clang -arch x86_64` on macOS).

When you have the token:
```bash
echo RE-xxxxxxxx > my-answer.txt
python3 check.py
```
Run `make` first. Each learner's vault has different names and a different token.
