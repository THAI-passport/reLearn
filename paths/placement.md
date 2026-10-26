# Placement Diagnostic (tutor-run, about 20 minutes)

Run the sections in order and stop at the first section where the learner gets fewer than two of three items. Ask one question at a time and let the learner answer before revealing anything. Record each answer as correct, partial, or wrong in `notes/profile.md`.

The learner may use a terminal, a compiler, and `man` pages. No web search, no LLM help.

## Section A: programming basics
1. What does this print? `int s = 0; for (int i = 1; i <= 4; i++) s += i; printf("%d\n", s);`
   Strong answer: 10, with the loop traced.
2. Write a C function that returns the larger of two ints, then compile and call it.
   Strong answer: compiles first or second try; correct signature and return.
3. What is the difference between a variable and its address?
   Strong answer: value vs location in memory; mentions `&` or a pointer.

Fail here: absolute beginner path.

## Section B: C and memory
1. `char s[] = "hi";` How many bytes is `s`, and what are they?
   Strong answer: 3 bytes: `h`, `i`, and a terminating NUL (0).
2. A function returns the address of one of its local variables. What goes wrong?
   Strong answer: the local's stack storage is invalid after return (dangling pointer).
3. What is `0x2A` in decimal, and what is `-1` as a 32-bit value in hex?
   Strong answer: 42 and `0xFFFFFFFF` (two's complement).

Fail here: rusty programmer path.

## Section C: systems and tooling
1. What happens between `clang hello.c` and a running process? Name at least three steps.
   Strong answer: preprocess, compile, assemble, link, then the loader maps it and resolves dynamic libraries.
2. What does `nm` show, and what does a `U` mean?
   Strong answer: the symbol table; `U` is an undefined symbol resolved at link or load time.
3. Name two things `strip` removes and one thing it cannot remove.
   Strong answer: symbol table and debug info; it cannot remove string literals, code, or imported symbol names needed for dynamic linking.

Fail here with strong A and B: developer path. Fail here with weak B: rusty path.

## Section D: assembly and debugging
Show this listing. It is real output of `clang -arch x86_64 -O2 -c` on macOS for a one-line function, from `objdump -d --x86-asm-syntax=intel --no-show-raw-insn` (System V x86_64 calling convention, Intel syntax). Regenerate it on the learner's machine if possible.
```
0000000000000000 <_f>:
       0:      	push	rbp
       1:      	mov	rbp, rsp
       4:      	lea	eax, [rdi + 2*rsi]
       7:      	pop	rbp
       8:      	ret
```
1. Write the C function this most likely came from.
   Strong answer: `int f(int a, int b) { return a + 2*b; }` with `rdi` and `rsi` identified as the first two arguments.
2. What is the difference between `jl` and `jb` after `cmp`?
   Strong answer: signed vs unsigned less-than (SF/OF vs CF).
3. In a debugger, how would you find the value a function returns?
   Strong answer: break after the call (or at `ret`) and read `rax`/`eax`, or use `finish`.

Fail here: developer path. Pass: continue.

## Section E: practitioner depth
1. A stripped binary compares your input with something you cannot find in `strings`. Give two approaches.
   Strong answer: debugger breakpoint on the compare or on `strcmp`/`memcmp`; static reading of the decoding routine; Frida/LD_PRELOAD hook.
2. What are ASLR and stack canaries, and how does each show up when you reverse a binary?
   Strong answer: randomized base addresses (PIE, relative addressing); canary load from a guard and a `__stack_chk_fail` call in the epilogue.
3. When would you use Ghidra's decompiler output with suspicion?
   Strong answer: wrong prototypes, aliasing, obfuscation, irreducible control flow, missed switch tables; always verify against assembly.

Pass: practitioner path. If the learner also names a research or professional focus, offer `specialist.md`.
