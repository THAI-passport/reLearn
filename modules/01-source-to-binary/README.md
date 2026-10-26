# Module 01: From Source to Binary

Kind: core. Time: about 4 hours. Prerequisites: module 00.

## Context
Early Unix compiled C with separate programs run one after another: the preprocessor `cpp`, the compiler proper, the assembler `as`, and the linker `ld`. Modern drivers such as `clang` and `gcc` still run the same stages, just behind one command. The split exists because programs are built from many files compiled separately. The linker joins them later, and the loader finishes the job when the program starts.

For a reverser this history matters because each stage leaves fingerprints in the binary. Symbol tables exist so the linker can join files. Relocations exist because the compiler does not know final addresses. Import tables exist because some code is joined only at load time. Most of these fingerprints can be stripped, but not all of them.

## Objectives
After this module you can:
- Run each compile stage on its own (`-E`, `-S`, `-c`, link) and say what each one produces.
- Read `nm` output: defined vs undefined (`U`), global (uppercase) vs local (lowercase) symbols.
- Explain what a relocation is and why an object file needs it.
- Link object files by hand and fix an "undefined symbols" error.
- List a binary's sections and the dynamic libraries it needs.
- Explain what stripping removed, and why a symbol needed for linking cannot be stripped.

## Prerequisites
You can already:
- Build a C program and identify it with `file` (module 00).
- Find text in a binary with `strings` and view bytes with `xxd` (module 00).

## Commands on your platform
All captured output below comes from macOS on Intel, Apple clang 17, building for x86_64. Your addresses and some details will differ; trust your own output.

| Task | macOS | Linux |
| :--- | :--- | :--- |
| Compile for x86_64 | `clang -arch x86_64 ...` | `gcc ...` or `clang ...` (on an ARM64 host, `x86_64-linux-gnu-gcc ...`) |
| Disassemble (Intel syntax) | `objdump -d --x86-asm-syntax=intel` | `objdump -d -M intel` |
| Relocations | `objdump -r` (or `otool -rv`) | `objdump -r` (or `readelf -r`) |
| Sections | `objdump -h` (or `otool -l`) | `objdump -h` (or `readelf -S`) |
| Dynamic libraries | `otool -L` | `ldd` (or `readelf -d`) |

On macOS, if `which nm otool strip` points into Anaconda or Homebrew, those versions can differ from Apple's. `xcrun nm` and `xcrun otool` always run Apple's.

## Guided steps
Work inside this folder in a scratch directory:
```bash
cd modules/01-source-to-binary
mkdir -p work
make            # builds the reference binaries and the challenge
```
Read `src/main.c`, `src/greet.c`, and `src/greet.h` before you start. Predict: what does the program print when run with the argument `Ada`?

### 1. Preprocess (`-E`)
```bash
clang -arch x86_64 -E src/greet.c -o work/greet.i
wc -l work/greet.i
tail -12 work/greet.i
```
<!-- captured: the commands above, macOS 26 Intel, Apple clang 17.0.0 -->
```
     589 work/greet.i
int greet_count = 0;
static int calls_this_file = 0;

static void bump(void) {
    greet_count++;
    calls_this_file++;
}

void greet(const char *name) {
    bump();
    printf("%s, %s!\n", "Hello", name);
}
```
A 17-line file became 589 lines. The comments are gone, `GREETING` was replaced by `"Hello"`, and `#include <stdio.h>` pasted in hundreds of lines of declarations.

Checkpoint: why does a reverser never see `#define` names like `GREETING` in a binary?

### 2. Compile to assembly (`-S`)
```bash
clang -arch x86_64 -S -O0 -masm=intel src/greet.c -o work/greet.s
less work/greet.s
```
Excerpt (lines 3-24 of the file; nothing else changed):
<!-- captured: the command above, then sed -n '3,24p' work/greet.s -->
```
	.intel_syntax noprefix
	.globl	_greet                          ## -- Begin function greet
	.p2align	4, 0x90
_greet:                                 ## @greet
	.cfi_startproc
## %bb.0:
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset rbp, -16
	mov	rbp, rsp
	.cfi_def_cfa_register rbp
	sub	rsp, 16
	mov	qword ptr [rbp - 8], rdi
	call	_bump
	mov	rdx, qword ptr [rbp - 8]
	lea	rdi, [rip + L_.str]
	lea	rsi, [rip + L_.str.1]
	mov	al, 0
	call	_printf
	add	rsp, 16
	pop	rbp
	ret
```
You do not need to read every instruction yet (that is Phase B). Notice three things:
- The compiler still uses names: `_greet`, `_bump`, `_printf`, `L_.str`. On macOS C names get a leading underscore; on Linux they do not.
- `.globl _greet` marks `greet` as visible to other files. `_bump` has no `.globl` because it is `static`.
- Lines starting with `.` are directives for the assembler, not instructions.

Without `-masm=intel`, clang prints AT&T syntax (`movq %rsp, %rbp`). This course uses Intel syntax.

### 3. Assemble to object files (`-c`)
```bash
clang -arch x86_64 -c src/greet.c -o work/greet.o
clang -arch x86_64 -c src/main.c  -o work/main.o
file work/greet.o work/main.o
```
<!-- captured: the commands above -->
```
work/greet.o: Mach-O 64-bit object x86_64
work/main.o:  Mach-O 64-bit object x86_64
```
On Linux, `file` reports `ELF 64-bit LSB relocatable, x86-64`. "Relocatable" is the clue: this file is not finished.

### 4. Read the symbol tables
Predict before running: which symbols will `greet.o` define, and which will `main.o` need from elsewhere?
```bash
nm work/greet.o
nm work/main.o
```
<!-- captured: the commands above -->
```
0000000000000030 t _bump
0000000000000114 b _calls_this_file
0000000000000000 T _greet
0000000000000110 S _greet_count
                 U _printf
```
```
                 U _greet
                 U _greet_count
0000000000000000 T _main
                 U _printf
```
How to read it:
| Letter | Meaning |
| :--- | :--- |
| `T` / `t` | code (text section) |
| `D` / `d` | initialized data |
| `B` / `b` | zero-initialized data (bss) |
| `S` / `s` | data in another section (here Mach-O `__DATA,__common`) |
| `U` | undefined: used here, defined somewhere else |

Uppercase means global (other files may use it); lowercase means local (`static`). The number is the symbol's offset inside this object file, not a final address. On Linux, `greet_count` usually shows as `B`, since it is zero-initialized and modern compilers place it in `.bss`.

Checkpoint: `main.o` calls `greet`, but its own symbol table only says `U _greet`. How can the compiler emit a `call` to a function whose address it does not know?

### 5. Relocations: the compiler's notes to the linker
```bash
objdump -d --x86-asm-syntax=intel work/main.o
objdump -r work/main.o
```
Excerpt of the disassembly (lines cut, none changed):
<!-- captured: objdump -d --x86-asm-syntax=intel work/main.o -->
```
      37: 48 8b 7d e8                  	mov	rdi, qword ptr [rbp - 0x18]
      3b: e8 00 00 00 00               	call	0x40 <_main+0x40>
      40: 48 8d 3d 2d 00 00 00         	lea	rdi, [rip + 0x2d]       ## 0x74 <_main+0x74>
      47: e8 00 00 00 00               	call	0x4c <_main+0x4c>
      4c: 48 8b 05 00 00 00 00         	mov	rax, qword ptr [rip]    ## 0x53 <_main+0x53>
```
<!-- captured: objdump -r work/main.o -->
```
RELOCATION RECORDS FOR [__text]:
OFFSET           TYPE                     VALUE
000000000000005f X86_64_RELOC_BRANCH      _printf
0000000000000058 X86_64_RELOC_SIGNED      __cstring
000000000000004f X86_64_RELOC_GOT_LOAD    _greet_count@GOTPCREL
0000000000000048 X86_64_RELOC_BRANCH      _greet
0000000000000043 X86_64_RELOC_SIGNED      __cstring
000000000000003c X86_64_RELOC_BRANCH      _greet
000000000000002d X86_64_RELOC_SIGNED      __cstring
```
Each `call` is encoded as `e8 00 00 00 00`: the opcode `e8` followed by a 4-byte offset of zero. The compiler did not know the target, so it left a hole. The relocation record at offset `0x3c` (the byte right after the `e8` at `0x3b`) tells the linker: "write the distance to `_greet` here." That is all a relocation is: an address of a hole, a kind, and a symbol.

Checkpoint: find the relocation that patches the second call to `_greet`. Which instruction byte does it point at?

### 6. Link, and break the link on purpose
Predict first: what happens if you link `main.o` alone?
```bash
clang -arch x86_64 work/main.o -o work/greet
```
<!-- captured: the command above -->
```
Undefined symbols for architecture x86_64:
  "_greet", referenced from:
      _main in main.o
      _main in main.o
  "_greet_count", referenced from:
      _main in main.o
ld: symbol(s) not found for architecture x86_64
clang: error: linker command failed with exit code 1 (use -v to see invocation)
```
The linker read the `U` entries and could not find a definition. `_printf` is missing from the list because the linker found it in the C library, which `clang` links by default. Now link both:
```bash
clang -arch x86_64 work/main.o work/greet.o -o work/greet
./work/greet Ada
```
<!-- captured: the commands above -->
```
Hello, Ada!
Hello, world!
greeted 2 times
```
Look at the filled-in holes:
```bash
objdump -d --x86-asm-syntax=intel --no-show-raw-insn work/greet
```
Excerpt from `_main` (lines cut, none changed):
<!-- captured: the command above -->
```
10000059b:     	call	0x1000005d0 <_greet>
1000005a0:     	lea	rdi, [rip + 0x8c]       ## 0x100000633 <_printf+0x100000633>
1000005a7:     	call	0x1000005d0 <_greet>
1000005ac:     	lea	rax, [rip + 0x1a4d]     ## 0x100002000 <_greet_count>
```
The calls now have real targets. Two more lessons hide in these lines:
- The `mov rax, [rip]` that loaded `greet_count` through the GOT became `lea rax, [...]`. The linker saw that `greet_count` is in the same binary and simplified the access.
- The comment `<_printf+0x100000633>` is wrong: that address is the string `"world"`, not part of `printf`. `objdump` labels addresses with the nearest symbol it knows, and here it guessed badly. Tools annotate; you verify.

### 7. Sections and dynamic libraries
```bash
objdump -h work/greet
otool -L work/greet        # Linux: ldd work/greet
```
<!-- captured: the commands above -->
```
Sections:
Idx Name          Size     VMA              Type
  0 __text        000000c4 0000000100000560 TEXT
  1 __stubs       00000006 0000000100000624 TEXT
  2 __cstring     00000030 000000010000062a DATA
  3 __unwind_info 00000058 000000010000065c DATA
  4 __got         00000008 0000000100001000 DATA
  5 __common      00000004 0000000100002000 BSS
  6 __bss         00000004 0000000100002004 BSS
```
```
work/greet:
	/usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1356.0.0)
```
- `__text` is code. `__cstring` holds the string literals. `__common` and `__bss` hold `greet_count` and `calls_this_file`.
- `__stubs` and `__got` exist for `printf`, which lives in `libSystem` and is bound when the program loads. Module 08 covers this in depth. On Linux the equivalents are `.text`, `.rodata`, `.bss`, `.plt`, and `.got`, and `ldd` lists `libc.so.6`.

Checkpoint: which section would you search first for the string a program compares your password against? Why?

### 8. What stripping removes
```bash
nm build/greet
nm build/greet-stripped
strings build/greet-stripped
```
<!-- captured: the commands above -->
```
0000000100000000 T __mh_execute_header
0000000100000600 t _bump
0000000100002004 b _calls_this_file
00000001000005d0 T _greet
0000000100002000 S _greet_count
0000000100000560 T _main
                 U _printf
```
```
0000000100000000 T __mh_execute_header
                 U _printf
```
```
reverser
world
greeted %d times
%s, %s!
Hello
```
Every name that only helped humans is gone: `main`, `greet`, `bump`, `greet_count`. `_printf` survives because the loader needs it to find `printf` in `libSystem` at run time. Strings survive because they are data the program uses.

Checkpoint: in a stripped binary, which names can you still trust to be present, and why?

## Challenge
Read `challenge/CHALLENGE.md`. You get an object file, not a program. You will need steps 3, 4, and 6. The token is encoded, so `strings` will not find it.

## Checkpoint
Answer without notes, then check with your notes. The tutor grades with the mastery rubric in `AGENTS.md`.
1. Name the four stages, the flag that stops after each, and the file each produces.
2. Why does `main.o` list `U _printf` while the linked program still runs without you providing `printf`?
3. What is a relocation? Point to one in `work/main.o` and say which bytes it fills in.
4. Why did `strings` fail on the challenge object, and what did you do instead?
5. (Module 00) What does `strip` remove, and what can it never remove from a dynamically linked program?

Transfer task: the tutor builds an unseen object file that needs two undefined symbols with different signatures. Link it into a working program.

Review-queue seeds: the meaning of `U`, `T`, and `t`; why calls in a `.o` are encoded as `e8 00 00 00 00`; why `_printf` survives stripping.
