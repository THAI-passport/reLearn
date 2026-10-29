# Module 04: First Look: Disassembler and Decompiler

Kind: core. Time: about 4 hours. Prerequisites: modules 01 and 03.

## Context
Early reversers read machine code by hand from listings. Interactive disassemblers changed that: IDA (1990s) let an analyst rename, annotate, and cross-reference a disassembly as understanding grew. The Hex-Rays decompiler (2007) went one step further and turned functions back into C-like code. In 2019 the NSA released Ghidra as open source, which made a free interactive disassembler and decompiler the default starting point for newcomers.

A decompiler does not recover the original source. The compiler threw away names, types, comments, and structure, and the decompiler infers a plausible C program that does the same thing. Learning to trust what it got right and distrust what it guessed is the core skill of this module.

## Objectives
After this module you can:
- Install Ghidra, import a binary, and run auto-analysis.
- Find `main` in a stripped binary.
- Read the decompiler view of a program you know and list what it got right (logic) and what it lost (names, types, struct layout).
- Rename a variable and retype it, and see the decompiler output change.
- Produce a command-line listing with `objdump` in Intel syntax.

## Prerequisites
You can already:
- Explain what symbols are and what `strip` removes (module 01).
- Explain pointers, arrays, strings, and struct layout in memory (modules 02 and 03).

## Commands on your platform
Captured output below comes from macOS 26 on Intel with Apple clang 17, building for x86_64. Linux commands were not run by the author.

```bash
cd modules/04-first-look
make
mkdir -p work
```
`make` builds the module 03 programs `pointers`, `cstrings`, and `nested` twice each, as `build/<name>` (symbols and debug info) and `build/<name>-stripped`, plus `build/gate` (a password checker with a known password) and the stripped `challenge/gate`. It prints one compiler warning from `pointers.c`; that warning belongs to module 03.

Install Ghidra from https://ghidra-sre.org (the official releases are also on the project's GitHub page). It needs a JDK; check the release notes for the current required version before installing, and run `python3 tools/check_env.py` afterwards. The author did not run Ghidra while writing this module, so the lesson tells you what to look for and does not show decompiler output. The tutor discusses what appears on your screen.

## Guided steps

### 1. A command-line listing first
Predict: what does `nm` show for `build/pointers` and for `build/pointers-stripped`? Then run:
```bash
nm build/pointers
nm build/pointers-stripped
```
macOS: if `nm` or `objdump` on your PATH is not Apple's, use `xcrun nm` and `xcrun objdump`.
<!-- captured: xcrun nm build/pointers; xcrun nm build/pointers-stripped, macOS 26 Intel, Apple clang 17.0.0 (lines cut: only the symbols that differ are shown) -->
```
0000000100000620 t _inside
00000001000004c0 T _main
```
The first command lists `_inside` and `_main`. The stripped build lists only imports (such as `_printf`) and `__mh_execute_header`.

Now the disassembly of `inside`, the function from module 03 that returns `sizeof(arr)` for a pointer parameter:
```bash
objdump -d --x86-asm-syntax=intel --no-show-raw-insn build/pointers      # macOS
objdump -d -M intel --no-show-raw-insn build/pointers                    # Linux (not run by the author)
```
<!-- captured: xcrun objdump -d --x86-asm-syntax=intel --no-show-raw-insn build/pointers, macOS 26 Intel (only the function _inside is shown; other lines cut) -->
```
0000000100000620 <_inside>:
100000620:     	push	rbp
100000621:     	mov	rbp, rsp
100000624:     	mov	qword ptr [rbp - 0x8], rdi
100000628:     	mov	eax, 0x8
10000062d:     	pop	rbp
10000062e:     	ret
```
Predict, using module 03: where does the `8` come from? (Register-level detail comes in module 05; for now the point is that `mov eax, 0x8` is the whole function.) In the stripped build, run the same command and find the same six instructions. The label is gone; you recognize the function by its shape.

Checkpoint: the compiler turned `return sizeof(arr)` into the constant 8. Why does that show that `arr` is a pointer in that function?

### 2. Import into Ghidra
1. Start Ghidra, create a project, and import `build/pointers` (File, Import File). Accept the detected format.
2. Open it in the CodeBrowser and accept auto-analysis with the defaults.
3. In the Symbol Tree, find `main`. The decompiler window shows a C-like version of the selected function.
4. Repeat with `build/pointers-stripped` in the same project.

Questions to answer before moving on (write the answers down; the tutor reads them):
- In the symbol build, which function names and local variable names appear? Where do they come from (debug info or the symbol table)?
- In the stripped build, how did you find `main`? Ghidra may name functions like `FUN_...` and variables like `local_...`. What does that tell you about what the file stored?

### 3. What the decompiler gets right and what it loses
Open `main` of `pointers` and `pointers-stripped` side by side and compare to `src/pointers.c` in module 03. Fill in this table for yourself:

| Item in the source | In the decompiler view of the stripped build |
| :--- | :--- |
| Function and variable names | |
| `int arr[8]` | |
| The call to `inside` and its result | |
| The format strings | |
| Types (`int *`, `uint8_t`) | |

Then do the same with `nested` and its `struct packet`. Predict first: will the decompiler show a struct, or arithmetic on a base pointer? (Module 03 step 4 told you which one the machine code contains.)

Checkpoint: name three things a decompiler cannot recover and why, using what you saw.

### 4. Rename and retype
In the stripped `nested` build, pick one local variable and rename it (select it, press L). Then retype one pointer variable (select it, press Ctrl+L) to the type you know it has from the source. Watch what happens to the arithmetic around it.

Checkpoint: why does a correct type make the code shorter and more readable?

### 5. A password checker
`build/gate` is a small program that takes a password. Try it:
```bash
./build/gate open-sesame
./build/gate sesameopen
```
<!-- captured: the commands above, macOS 26 Intel, Apple clang 17.0.0 -->
```
access granted
access denied
```
Now look at what `strings` shows:
```bash
strings -n 4 build/gate
```
<!-- captured: xcrun strings -n 4 build/gate, macOS 26 Intel (output filtered to the lines from the program itself) -->
```
usage: %s <password>
access granted
access denied
open
-sesame
```
The password never appears whole: `strings` shows two fragments, `open` and `-sesame`. Where a fragment sits in the file says nothing about the order the program joins them in; only the code does. Open `build/gate` in Ghidra and find the function that builds the expected string. In the decompiler view, identify which piece is copied first, which is appended, and what is compared. The source is `src/gate.c`, to read after you have found it yourself.

Checkpoint: if you only had `strings`, how many orderings would you need to try for two fragments? For five? Why is reading the code still the better method?

## Challenge
Read `challenge/CHALLENGE.md`. The stripped `challenge/gate` builds its password from two pieces at run time. Use the decompiler to recover it.

## Checkpoint
Answer without notes first. The tutor grades with the mastery rubric in `AGENTS.md`.
1. Name three things a decompiler cannot recover and why.
2. What is the difference between what a symbol table gives you and what debug info gives you?
3. Why can the same stripped function decompile differently after you retype one variable?
4. Why did `strings` not reveal the gate password, and what did it reveal?
5. (Module 03) What does `sizeof(arr)` return inside a function that takes `int arr[8]`, and how did that show up in this module?

Transfer task: the tutor gives the decompiler output of an unseen 30-line function (no source). Describe what it does, name its parameters and locals, and say which parts of your description are certain and which are guesses.

Review-queue seeds: what `strip` removes; where Ghidra's local names come from; why struct access looks like pointer arithmetic; what a decompiler cannot recover.
