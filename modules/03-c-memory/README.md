# Module 03: C Through the Lens of Memory

Kind: core. Time: about 6 hours. Prerequisites: modules 01 and 02.

## Context
C was written at Bell Labs in the early 1970s for the PDP-11, a machine whose instructions addressed memory directly. C's pointers are that machine model made explicit: a pointer is an address, and `p + 1` means "the next object of this type". An array name used in an expression turns into a pointer to its first element (arrays "decay"), which is why `arr[i]` is defined as `*(arr + i)`. Strings follow the same minimalism: a string is bytes up to a NUL (0) byte, so there is no length field to store, and nothing stops a copy from running past the end. Most memory-corruption bugs and exploits you will study later start there.

As a reverser you see the compiled result: no types, no array bounds, only addresses and offsets. This module teaches you to read C as memory.

## Objectives
After this module you can:
- Draw the memory map of a running process (code, read-only data, data, bss, heap, stack, shared libraries) and place an address in it.
- Explain pointers, pointer arithmetic, and the array-pointer relationship.
- Explain C strings and the NUL terminator, and why `sizeof` and `strlen` differ.
- Explain the lifetime of globals, heap blocks, and stack locals.
- Use `-fsanitize=address` to catch a bug and say what memory it touched.

## Prerequisites
You can already:
- Build a module with `make` and compare symbol and stripped builds (module 01).
- Read little-endian bytes in `xxd` output and predict struct sizes and padding (module 02).

## Commands on your platform
Captured output below comes from macOS 26 on Intel with Apple clang 17, building for x86_64. Addresses change on every run (ASLR), so yours will differ. Linux x86_64 should give the same sizes and offsets. The Linux commands in this lesson were not run by the author; if your output differs in a way the lesson does not explain, trust yours and ask the tutor.

```bash
cd modules/03-c-memory
make
mkdir -p work
```
`make` prints two compiler warnings (`pointers.c` and `lifetime.c`). Both are the bugs the lesson is about. Read them: the compiler already tells you what is wrong.

## Guided steps

### 1. The process memory map
Predict first: in `memmap.c` there is a function, a string constant, an initialized global, an uninitialized global, a `malloc` block, and a local. Which of these addresses is highest? Which two are closest together?
```bash
./build/memmap
```
<!-- captured: ./build/memmap, macOS 26 Intel, Apple clang 17.0.0 (your addresses will differ) -->
```
pid          93971
code         0x10cd996d0  (function here)
rodata       0x10cd99700  (const array literal)
data         0x10cd9b000  (initialized global)
bss          0x10cd9b004  (uninitialized global)
heap         0x7fd9f4104080  (malloc(64))
stack        0x7ff7b31655ec  (local in main)
libc         0x7ff81aa3bbe0  (function printf)
```
| Region | Holds | Lifetime |
| :--- | :--- | :--- |
| code (text) | machine instructions | whole run, read-only and executable |
| rodata | string literals, `const` data | whole run, read-only |
| data | initialized globals | whole run, writable |
| bss | uninitialized globals (zero-filled, not stored in the file) | whole run, writable |
| heap | `malloc` blocks | from `malloc` to `free` |
| stack | locals, saved registers, return addresses | from function entry to return |
| libraries | shared code such as libc | whole run |

Code, rodata, data, and bss are neighbors because they come from one file. The heap, stack, and libraries are placed elsewhere, so their addresses are far apart. This is how you tell regions apart from an address alone, which the challenge needs.

Look at the real map. Run with a pause, and from a second terminal:
```bash
./build/memmap --pause
```
macOS (use the pid the program prints): `vmmap <pid>`. Linux: `cat /proc/<pid>/maps`. Find the line that contains each address from the printout. Then press Enter in the first terminal.

Checkpoint: the stack address is much higher than the heap address here. Which way does the stack grow, and what does that tell you about where the next function call's locals go?

### 2. Pointers and arrays
Predict each line, then run:
```bash
./build/pointers
```
<!-- captured: ./build/pointers, macOS 26 Intel, Apple clang 17.0.0 (addresses differ per run) -->
```
sizeof(arr) in main: 32, sizeof(arr) inside a function: 8
p     = 0x7ff7baa6c5c0
p + 1 = 0x7ff7baa6c5c4  (+4 bytes, one int)
p + 3 = 0x7ff7baa6c5cc  *(p + 3) = 40, p[3] = 40, 3[p] = 40
&arr[5] - &arr[1] = 4 elements
(char *)&arr[5] - (char *)&arr[1] = 16 bytes
*(int *)bytes = 0x04030201 (the same 4 bytes read as one int)
```
- `p + 1` adds `sizeof(*p)` bytes, not 1. Pointer subtraction divides by the element size. In a disassembly you will only see the scaled byte offsets (`+4`, `+0xc`, `*4`), so the element size is something you reconstruct.
- `p[3]` is `*(p + 3)`, which is why `3[p]` compiles. An array index is address arithmetic.
- Inside a function, a parameter declared `int arr[8]` is really an `int *`. `sizeof` there is 8 (a pointer), not 32. The size was never passed in.
- The last line reads four bytes as one `int`: byte order from module 02 decides the value.

Checkpoint: why does `sizeof(arr)` differ between `main` and `inside`? What information does the callee have, and what does it lack?

### 3. C strings and the NUL terminator
```bash
./build/cstrings
```
<!-- captured: ./build/cstrings, macOS 26 Intel, Apple clang 17.0.0 -->
```
sizeof(a) = 6, strlen(a) = 5
sizeof(b) = 8, strlen(b) = 2
sizeof(c) = 3 (no NUL)
sizeof(d) = 8 (a pointer), strlen(d) = 5
bytes of a: 68 65 6c 6c 6f 00
after a[2] = 0: strlen(a) = 2, a = "he", a + 3 = "lo"
```
- `sizeof` is the size of the object; `strlen` counts bytes until the first 0.
- `c` has no NUL, so passing it to `strlen` would read past the array into whatever lies next: a bug without an error message.
- `a[2] = 0` shortens the string but leaves `"lo"` in memory. Deleted text stays in dumps. That is why the challenge fillers matter, and why forensic tools find "deleted" strings.
- `d` is a pointer to read-only data; writing through it crashes.

Checkpoint: `strcpy(dst, "reverse")` needs how many bytes in `dst`? Why 8 and not 7?

### 4. A struct with nested arrays
Predict the offsets from the rules of module 02, then run:
```bash
./build/nested
```
<!-- captured: ./build/nested, macOS 26 Intel, Apple clang 17.0.0 -->
```
sizeof(struct packet) = 28
id @0  tag @2  samples @8  range @24
samples[2] via arithmetic: 300
range.hi via arithmetic:   9
raw bytes: 02 01 61 62 00 00 00 00 64 00 00 00 c8 00 00 00 2c 01 00 00 90 01 00 00 03 09 00 00
```
Match every byte to a field: `02 01` is `id` (0x0102, little-endian), `61 62 00 00 00 00` is `tag` (`ab` plus four NUL fill bytes, which belong to the array), and `samples` starts at 8 with no gap. Two bytes in the dump are true padding: find them, and say why the compiler put them there. Then check `src/nested.c`.

In a binary this struct is just "base + 8 + 4*i". There is no `samples` and no `packet`. Decompilers guess the layout from such access patterns; module 04 shows how often they guess partly wrong.

### 5. Lifetimes
```bash
./build/lifetime
```
<!-- captured: ./build/lifetime, macOS 26 Intel, Apple clang 17.0.0 (the second value changes per run) -->
```
heap block after other calls: 99, global counter: 1
dangling pointer, read before clobber(): 1234, after: 0x90be80ac
```
- The global and the heap block are unaffected by function calls.
- `make_local` returned the address of a variable in its own stack frame. The frame is dead, but the memory is still mapped, so the read worked until another call reused that stack space. The compiler warned about exactly this.

Checkpoint: after a function returns, what happens to its locals' memory? Why is the bug silent at first?

### 6. Catching a bug with AddressSanitizer
`src/overflow.c` copies a 7-letter string plus its NUL into a 7-byte heap block. `build/overflow` is built with `-fsanitize=address`, which adds checks around every memory access and shadow memory that marks which bytes are valid.
```bash
./build/overflow
```
The author could not run AddressSanitizer in the authoring environment, so there is no captured output here; the report is yours to read. If it crashes without a report, tell the tutor your OS and CPU. Read the report from the top and answer:
1. What kind of error is it, and which line of `overflow.c` does the first stack frame point to?
2. How many bytes past the end did it touch? Where was that block allocated (the "allocated by" frame)?
3. Fix the bug by changing one expression, rebuild with `make`, and confirm the report disappears.

Checkpoint: the program printed `copy = reverse` correctly (without ASan, it does). Why is "it works" not evidence that the code is correct?

### 7. Finding data in a memory dump
`build/vault` is the challenge program with a known token and symbols. It prints where its three pieces are and writes a dump of the memory cells holding them:
```bash
./build/vault work/demo.bin
xxd -g 1 work/demo.bin
```
<!-- captured: the commands above, macOS 26 Intel, Apple clang 17.0.0 (addresses differ per run; the token here is the fixed demo token) -->
```
piece 1 at 0x7ff7b07295c8 length 3
piece 2 at 0x10f7d7010 length 4
piece 3 at 0x7fc9f1f05fa0 length 4
00000000: 4d 45 4d 44 03 00 00 00 00 70 7d 0f 01 00 00 00  MEMD.....p}.....
00000010: 30 00 00 00 00 00 00 00 64 65 6d 6f 2d 62 65 66  0.......demo-bef
00000020: 6f 72 65 2d 31 00 00 00 64 65 6d 6f 00 00 00 00  ore-1...demo....
00000030: 00 00 00 00 00 00 00 00 64 65 6d 6f 2d 61 66 74  ........demo-aft
00000040: 65 72 2d 31 00 00 00 00 90 5f f0 f1 c9 7f 00 00  er-1....._......
00000050: 30 00 00 00 00 00 00 00 64 65 6d 6f 2d 62 65 66  0.......demo-bef
00000060: 6f 72 65 2d 32 00 00 00 31 32 33 34 00 00 00 00  ore-2...1234....
00000070: 00 00 00 00 00 00 00 00 64 65 6d 6f 2d 61 66 74  ........demo-aft
00000080: 65 72 2d 32 00 00 00 00 b8 95 72 b0 f7 7f 00 00  er-2......r.....
00000090: 30 00 00 00 00 00 00 00 64 65 6d 6f 2d 62 65 66  0.......demo-bef
000000a0: 6f 72 65 2d 33 00 00 00 52 45 2d 00 00 00 00 00  ore-3...RE-.....
000000b0: 00 00 00 00 00 00 00 00 64 65 6d 6f 2d 61 66 74  ........demo-aft
000000c0: 65 72 2d 33 00 00 00 00                          er-3....
```
Work it through by hand (the format is in `challenge/CHALLENGE.md`):
- Header: `MEMD`, then a 4-byte little-endian count (3).
- First cell: base `00 70 7d 0f 01 00 00 00` reversed is `0x10f7d7000`, size `0x30` (48), then 48 bytes.
- Piece 2 is at `0x10f7d7010`. That minus the base is 16, so it starts 16 bytes into the first cell (the `before` text is exactly 16 bytes): `demo`, length 4.
- The address `0x10f7d7010` is next to the program's own data, so that cell is the global. The cell at `0x7fc9...` is the heap. The one at `0x7ff7...` is the stack.
- Piece 1 is `RE-` (the stack cell), piece 3 is `1234` (the heap cell). Joined in number order: `RE-demo1234`.

Note what else is in the dump: the filler strings and the bytes after the NUL. Real memory dumps are full of such neighbors.

## Challenge
Read `challenge/CHALLENGE.md`. The stripped `challenge/vault` splits a seeded token across a global, a heap block, and a stack buffer. Reassemble it from the printout and the dump.

## Checkpoint
Answer without notes first. The tutor grades with the mastery rubric in `AGENTS.md`.
1. Why does `sizeof(arr)` differ inside and outside a function?
2. What happens to a local variable's memory after its function returns, and why can a stale pointer still appear to work?
3. Given six addresses (code, global, heap, stack, libc function, string literal), order them from low to high and say how you decided.
4. Why are C strings NUL-terminated, and what does that cost?
5. (Module 02) `struct { char a; int b; char c; }`: give its size and the offset of each field.

Transfer task: the tutor gives an unseen program that has a struct containing arrays plus its printed addresses. Predict its memory layout and the bytes of one instance.

Review-queue seeds: array decay; why `p + 1` adds 4 for an `int *`; strlen vs sizeof; lifetime of a returned local; how to tell stack from heap from an address.
