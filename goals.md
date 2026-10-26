# Reverse Engineering Curriculum

## Mission
Teach reverse engineering (RE) from first principles to learners at any starting level. The first concrete milestone is the same for everyone: **take a small compiled C program, disassemble and decompile it, and explain what the original source did.** After that the course adds tools, platforms, languages, and harder targets, and ends with a professional-grade analysis of an unseen binary.

The course is LLM-tutored (see `AGENTS.md`) and self-paced. Each learner's progress is recorded in `notes/` (created from `notes/_templates/` by `make init-notes`), which becomes a personal knowledge base. Learner routes and placement live in `paths/`.

## Principles
1. **C through the lens of memory.** C is taught only as far as RE needs it, always as "what does this look like in memory and in the binary".
2. **Compile, then compare.** Early targets come with source so the learner can check their reading against the truth. Source-less challenges follow.
3. **One new idea at a time.** Predict, explain, do, check, reflect (`AGENTS.md`).
4. **Tools arrive after the pain they remove.** Command-line triage, then disassembler, then decompiler, then debugger, then instrumentation.
5. **Mastery, not exposure.** A module is done when its checkpoint is passed against the rubric in `AGENTS.md`, not when it has been read.
6. **Real output only.** Every disassembly, hex dump, and decompiler listing in a lesson comes from a binary built in this repo.
7. **Safe by default.** Training binaries are built from source here. Hostile or third-party protected samples are analyzed only in an isolated, snapshotted VM, only when the learner brings them, and never committed.

## Platform Scope
- Primary architecture: **x86_64**. It runs natively on Intel Macs and x86_64 Linux, through Rosetta 2 on Apple Silicon (`clang -arch x86_64`), and through a cross compiler plus `qemu-user` on ARM64 Linux. Most CTFs, books, and tooling assume it.
- Second architecture: **ARM64** (module 20), plus brief 32-bit x86 and MIPS/ARM Cortex-M in the firmware track.
- Formats: **Mach-O** (macOS), **ELF** (Linux, most CTFs), **PE** (Windows). Module 08 covers all three; Windows internals (module 24) runs inside a VM.
- Host routes: macOS Intel, macOS Apple Silicon, Linux x86_64, Linux ARM64, and Windows through WSL2 (Linux track) plus a Windows VM (PE track). `tools/check_env.py` detects the host and prints the route. See `README.md`, "Platform routes".

## Phase Outcomes (exit criteria)
| Phase | After this phase the learner can... |
| :--- | :--- |
| A. Foundations | Explain how C becomes a binary, decode raw bytes as integers, floats, and structs, read C pointer/array/struct code, and get a first decompiler view of a program. |
| B. Reading Assembly | Read small x86_64 functions at `-O0` and `-O2`, identify arguments, locals, branches, loops, and calls, and reconstruct them as C. |
| C. Static Analysis | Explain how a binary is linked and loaded, triage an unknown binary, drive Ghidra and its scripting API, recognize library and crypto code, and judge when the decompiler is wrong. |
| D. Dynamic Analysis | Drive a debugger, trace system and library calls, instrument with Frida, and pick emulation, DBI, replay, or fuzzing when they fit. |
| E. Modification | Patch and hook a binary correctly, re-sign it, and write solvers and keygens that pass a checker. |
| F. Platforms and Advanced Targets | Read ARM64 and C++, explain and identify exploit mitigations, use symbolic execution, and recognize and defeat basic anti-analysis, packing, and obfuscation. Electives add Rust/Go, managed runtimes, and OS internals. |
| G. Professional Practice | Analyze an unseen binary end to end, keep a reproducible record, write a report another analyst can verify, and act within legal and disclosure norms. |

## Module Index
Status: **built** = folder exists and is tested; **spec** = specified below, built just in time with `modules/_template/`. Hours are guided-study estimates for a learner meeting the prerequisites; `paths/README.md` turns them into per-path totals.

| ID | Module | Kind | Hours | Prereqs | Status |
| :--- | :--- | :--- | ---: | :--- | :--- |
| P0 | C and Memory Primer (bridge) | bridge | 15 | none | spec |
| 00 | Setup and Sanity Check | core | 1 | none | built |
| 01 | From Source to Binary | core | 4 | 00 | built |
| 02 | Data Representation: Numbers, Bits, and Bytes | core | 5 | 00 | built |
| 03 | C Through the Lens of Memory | core | 6 | 01, 02 | spec |
| 04 | First Look: Disassembler and Decompiler | core | 4 | 01, 03 | spec |
| 05 | CPU, Registers, and Instructions | core | 8 | 02, 04 | spec |
| 06 | Functions, the Stack, and Calling Conventions | core | 8 | 05 | spec |
| 07 | C Constructs and the Optimizer | core | 10 | 06 | spec |
| 08 | Binary Formats, Linking, and Loading | core | 8 | 01, 06 | spec |
| 09 | Triage and Ghidra in Depth | core | 8 | 07, 08 | spec |
| 10 | Crackme Series 1 | core | 8 | 09 | spec |
| 11 | Library Code, Crypto Constants, and Binary Diffing | core | 6 | 09 | spec |
| 12 | Decompiler Internals and Analysis Scripting | core | 8 | 09 | spec |
| 13 | Debugger Fundamentals | core | 6 | 07 | spec |
| 14 | System Calls, Tracing, and Interposition | core | 5 | 08, 13 | spec |
| 15 | Frida in Depth and Runtime Secrets | core | 8 | 13, 14 | spec |
| 16 | Emulation, DBI, Replay, and Fuzzing | elective | 10 | 15 | spec |
| 17 | Patching, Hooking, and Code Signing | core | 8 | 10, 13 | spec |
| 18 | Memory Corruption and Mitigations | core | 8 | 06, 13 | spec |
| 19 | Symbolic Execution, SMT, and Taint | elective | 10 | 10, 12 | spec |
| 20 | ARM64 | core | 8 | 07 | spec |
| 21 | Reversing C++ | core | 8 | 09 | spec |
| 22 | Rust and Go Binaries | elective | 6 | 21 | spec |
| 23 | Managed Runtimes, Bytecode, and WebAssembly | elective | 8 | 09 | spec |
| 24 | Windows Internals for Reversers | elective | 8 | 08, 13 | spec |
| 25 | Linux and macOS Internals for Reversers | elective | 8 | 08, 14 | spec |
| 26 | Anti-Analysis, Anti-Tamper, and Licensing | core | 8 | 15, 17 | spec |
| 27 | Packing and Obfuscation Fundamentals | core | 10 | 26 | spec |
| 28 | Professional Practice: Reporting, Reproducibility, Law, Disclosure | core | 4 | 10 | spec |
| 29 | Capstone | core | 15 | all core | spec |

Specialist tracks (section "Specialist Tracks") follow the core and have their own module IDs (`S1.1` and so on). `S1.1` is built.

### Changes from v1 of this curriculum
v1 had 24 modules (00-23). v2 regroups them and fills gaps. Mapping for learners who started on v1: 00 unchanged; v1 02 split into 02 (numbers, bits, bytes) and 03 (pointers, stack, heap); v1 03 became 04; v1 04-06 became 05-07 with the assembly checkpoint folded into 07; v1 08-09 became 09; v1 11 became 11 (now with signatures and diffing); v1 12-14 became 13-15; v1 15-16 became 17; v1 17 became 20; v1 18 split into 08 and 24; v1 19 became 21; v1 20 became 26; v1 21 became 27 plus track S1; v1 22 split into 22 and 23; v1 23 became 29. New: 08, 12, 14, 16, 18, 19, 24, 25, 28, P0, and the specialist tracks.

## Module Specifications
Format for each module: kind and hours, prerequisites, context (the history-and-why opener for context-first learners), can-do outcomes, labs, checkpoint. Checkpoints always contain 3-5 explain-it-back questions plus the transfer task named here, and are graded with the mastery rubric in `AGENTS.md`. Every lab has a symbol build and a stripped, seeded challenge built with `tools/relab.py`.

### Bridge

#### P0 C and Memory Primer
- Kind: bridge (absolute-beginner path only). Hours: 15. Prereqs: none.
- Context: C (Ritchie, Bell Labs, early 1970s) was designed to write Unix portably while staying close to the machine. That closeness is why compiled C is the easiest real code to reverse.
- Can do: write, compile, and run small C programs with variables, `if`, loops, functions, arrays, and `printf`; explain what a variable, a type, an address, and a function call are; use a terminal, an editor, and `make`.
- Labs: ten short programs (temperature table, array sum and max, string length by hand, a function with a pointer argument, a struct of a "player"), each with a predict-the-output step. No security content.
- Checkpoint: write from scratch a program that reads numbers, stores them in an array, and prints the largest with its index; explain each line. Transfer: predict the output of an unseen 20-line program.

### Phase A: Foundations

#### 00 Setup and Sanity Check (built)
- Core, 1 h. Prereqs: none.
- Context: what reverse engineering is, where it is used (interoperability, security auditing, malware analysis, vulnerability research, digital preservation), and the legal and ethical frame introduced here and developed in module 28.
- Can do: verify the toolchain with `tools/check_env.py`; build a C program; identify a binary with `file`; find embedded text with `strings`; view bytes with `xxd`; explain what `strip` removes.
- Labs: `hello.c` with a seeded token; challenge: recover the token from a stripped binary.
- Checkpoint: what `strip` removes and keeps; why `strings` still works; one thing `strings` cannot tell you.

#### 01 From Source to Binary (built)
- Core, 4 h. Prereqs: 00.
- Context: the classic Unix toolchain split (`cpp`, `cc1`, `as`, `ld`) still shapes modern compilers and explains why object files, symbols, and relocations exist at all.
- Can do: run each compile stage on its own (`-E`, `-S`, `-c`, link) and say what each produces; read `nm` output (defined vs undefined, global vs local); explain a relocation and why an object file has them; link object files by hand and fix an "undefined symbol" error; list a program's sections and dynamic libraries.
- Labs: a two-file program built stage by stage; `nm`, `otool -r`/`objdump -r`, `otool -l`/`readelf -S`, `otool -L`/`ldd`; strip comparison.
- Challenge: a seeded object file with an encoded token and an undefined symbol the learner must provide, then link and run.
- Checkpoint: the four stages and their outputs; why `main.o` lists `U _printf`; why the token was invisible to `strings`. Transfer: link an unseen object that needs two undefined symbols.

#### 02 Data Representation: Numbers, Bits, and Bytes (built)
- Core, 5 h. Prereqs: 00.
- Context: binary and hexadecimal as notation; why two's complement won over sign-magnitude and ones' complement; the endianness debate (Cohen, "On Holy Wars and a Plea for Peace", 1980); IEEE 754 (1985) ending incompatible floating point formats.
- Can do: convert between binary, hex, and decimal; apply AND, OR, XOR, NOT, shifts, and masks; read two's complement and spot signed vs unsigned interpretations of the same bits; read little-endian multi-byte values in a hex dump; decode an IEEE 754 single by hand; predict C type sizes, alignment, and struct padding with `sizeof` and `offsetof`.
- Labs: `bits.c` (masks, shifts, sign extension), `floats.c` (IEEE 754 fields), `layout.c` (sizes, offsets, padding), a demo record decoded with `xxd`.
- Challenge: a stripped program writes a seeded binary record; decode its fields from the raw bytes.
- Checkpoint: why `0xFFFFFFFF` is both 4294967295 and -1; how to tell endianness from a dump; where padding comes from. Transfer: decode an unseen record layout.

#### 03 C Through the Lens of Memory
- Core, 6 h. Prereqs: 01, 02.
- Context: the PDP-11 heritage of C pointers; why arrays decay to pointers; why C strings are NUL-terminated (and the cost: buffer overflows).
- Can do: draw the process memory map (text, data, bss, heap, stack, libraries) for a running program; explain pointers, pointer arithmetic, and the array-pointer relationship; explain C strings and the NUL terminator; explain stack vs heap vs global lifetime; use `-fsanitize=address` to catch a bug and say what memory it touched.
- Labs: programs that print addresses of globals, locals, heap blocks, and functions; a struct with nested arrays walked with pointers; an off-by-one string bug caught by ASan; `vmmap` (macOS) or `/proc/self/maps` (Linux).
- Challenge: a stripped program that stores a seeded token split across a global, a heap block, and a stack buffer and prints only their addresses and lengths; reconstruct the token from a provided core-style memory dump file.
- Checkpoint: why `sizeof(arr)` differs inside and outside a function; what happens to a local after return. Transfer: predict the memory layout of an unseen struct-of-arrays program.

#### 04 First Look: Disassembler and Decompiler
- Core, 4 h. Prereqs: 01, 03.
- Context: from hand disassembly to IDA (1990s) and the Hex-Rays decompiler (2007), to Ghidra's public release by the NSA (2019), which made a free decompiler standard.
- Can do: install Ghidra and import a binary; find `main`; read the decompiler view of a known program and list what it got right (logic) and what it lost (names, types, struct layout); rename and retype one variable; use `objdump -d --x86-asm-syntax=intel` (macOS) or `objdump -d -M intel` (Linux) for a CLI listing.
- Labs: the module 03 programs, with symbols and stripped, side by side in Ghidra.
- Challenge: a stripped binary that checks a seeded password built by concatenating two halves at runtime (so `strings` shows only fragments); read the decompiler output to recover it.
- Checkpoint: three things a decompiler cannot recover and why. Transfer: describe an unseen 30-line function from its decompiler output only.

### Phase B: Reading Assembly (x86_64)

#### 05 CPU, Registers, and Instructions
- Core, 8 h. Prereqs: 02, 04.
- Context: the x86 lineage from the 8086 (1978) through IA-32 to AMD64 (2003), and why register names like `ax`, `eax`, `rax` coexist.
- Can do: describe fetch-decode-execute; name the 16 general-purpose registers and their 8/16/32-bit views, `rip`, `rsp`, and RFLAGS (CF, ZF, SF, OF); read Intel and AT&T syntax; explain `mov`, `lea`, `add`, `sub`, `imul`, `and`, `or`, `xor`, `shl`, `sar`, `shr`, `cmp`, `test`, `jmp`, `jcc`, `movzx`, `movsx`, `cdqe`; predict flag effects; explain why writing `eax` zeroes the upper half of `rax`.
- Labs: tiny hand-written assembly functions called from C; single expressions compiled at `-O0`, read in `objdump` and Ghidra; an instruction-encoding peek with `xxd`.
- Challenge: a stripped function that transforms a seeded 32-bit input with arithmetic and bitwise operations; find the input that yields the target.
- Checkpoint: signed vs unsigned jumps (`jl` vs `jb`); `lea` as arithmetic. Transfer: hand-trace an unseen 12-instruction function.

#### 06 Functions, the Stack, and Calling Conventions
- Core, 8 h. Prereqs: 05.
- Context: why calling conventions exist (separate compilation), the cdecl/stdcall era on 32-bit x86, and the 64-bit split between System V and Microsoft x64.
- Can do: explain `call`/`ret`, prologue and epilogue, frame pointer vs frame-pointer omission; locate locals and arguments in a frame; apply the System V AMD64 ABI (args in `rdi`, `rsi`, `rdx`, `rcx`, `r8`, `r9`, return in `rax`, caller- vs callee-saved registers, 16-byte alignment, red zone) and contrast it with Microsoft x64 (`rcx`, `rdx`, `r8`, `r9`, 32-byte shadow space); recognize Mach-O symbol underscore prefixes; read variadic calls (`al` = number of vector registers).
- Labs: functions with 1-8 arguments, struct-by-value arguments, recursion; draw the stack at a breakpoint (preview of LLDB/GDB).
- Challenge: a stripped binary with a recursive seeded check; recover the argument values that pass.
- Checkpoint: why the seventh argument is on the stack; what `push rbp; mov rbp, rsp` buys. Transfer: annotate the frame of an unseen function.

#### 07 C Constructs and the Optimizer
- Core, 10 h. Prereqs: 06.
- Context: how compilers work (front end, IR in SSA form, optimization passes, back end with instruction selection and register allocation), with LLVM and GCC as the two open examples.
- Can do: recognize `if/else`, `for`/`while`/`do`, `switch` (jump tables and binary decision trees), array indexing, struct field access, and string loops; compare `-O0`, `-O1`, `-O2`, `-Os` output and name the transformations (inlining, constant folding, dead code elimination, strength reduction, division by multiplication with magic numbers, loop unrolling and vectorization, tail calls, conditional moves); read `-emit-llvm` IR for one function.
- Labs: one C file per construct, built at four optimization levels, read in `objdump` and Ghidra; LLVM IR walkthrough.
- Challenge (Phase B checkpoint): three stripped mystery functions; reconstruct each as C without the decompiler. `check.py` compiles the learner's C and compares behavior with the hidden original on random inputs.
- Checkpoint: why `x / 7` becomes a multiply; how to tell a jump table. Transfer: reconstruct an unseen `-O2` function.

### Phase C: Static Analysis

#### 08 Binary Formats, Linking, and Loading
- Core, 8 h. Prereqs: 01, 06.
- Context: a.out to COFF to ELF (System V, 1990s) and PE (Windows NT, 1993); Mach-O from NeXTSTEP.
- Can do: walk the headers, load commands/program headers, segments, and sections of Mach-O, ELF, and PE; explain static vs dynamic linking, symbol resolution, relocations, PIC/PIE, lazy binding (PLT/GOT on ELF, stubs and `__la_symbol_ptr` or chained fixups on Mach-O, IAT on PE), and what the loader (`dyld`, `ld.so`, the Windows loader) does before `main`; explain code signing (Mach-O code signature, Authenticode) and macOS entitlements, and inspect them with `codesign -dv --entitlements -`.
- Labs: one program built as Mach-O and ELF (cross-compiled object or Linux host) and a provided PE built from source with `x86_64-w64-mingw32-gcc`; parse headers with LIEF in Python; trace lazy binding at runtime.
- Challenge: a seeded binary whose token is assembled from data placed in a custom section and a constructor function that runs before `main`.
- Checkpoint: segment vs section; what a GOT entry holds before and after the first call. Transfer: identify the format, entry point, imports, and constructors of an unseen binary.

#### 09 Triage and Ghidra in Depth
- Core, 8 h. Prereqs: 07, 08.
- Context: why analysts standardize triage (time-boxing, avoiding running unknown code first).
- Can do: run a repeatable first-15-minutes triage (`file`, hashes, `strings` with encodings, imports, sections, entropy, signatures, packer hints) and record it; in Ghidra, use the Listing, Decompiler, Function Graph, Symbol Tree, Data Type Manager, cross-references, bookmarks; define structs and function signatures and propagate types; recover a program's call graph.
- Labs: triage template in `notes/cheatsheets/`; a struct-heavy program reversed to recovered type definitions.
- Challenge: a stripped binary with a seeded config struct parsed from a file; recover the struct definition and write a valid config.
- Checkpoint: what entropy tells you and what it does not. Transfer: triage report for an unseen binary within 15 minutes.

#### 10 Crackme Series 1
- Core, 8 h. Prereqs: 09.
- Context: crackme culture (crackmes.one) as legal, purpose-built practice; licensing checks as the classic target.
- Can do: solve plaintext compare, transformed strings (XOR, rotation, table lookup), arithmetic checksums, and serial-number schemes; write a solver or keygen for each and validate it with `check.py`.
- Labs: five progressive seeded crackmes.
- Challenge: a two-stage crackme whose serial depends on a seeded username.
- Checkpoint: how to work backward from the success branch. Transfer: solve an unseen crackme of comparable difficulty.

#### 11 Library Code, Crypto Constants, and Binary Diffing
- Core, 6 h. Prereqs: 09.
- Context: statically linked binaries hide thousands of library functions; IDA's FLIRT (Fast Library Identification and Recognition Technology) introduced signature matching; diffing grew from patch analysis.
- Can do: recognize Base64, CRC32, MD5, SHA-1/2, AES (S-box, round constants), RC4, TEA, and simple PRNGs by constants and structure; apply Ghidra Function ID and FLIRT-style signatures to a static binary; use YARA-style byte patterns; diff two builds with BinDiff or Diaphora and Ghidra Version Tracking to locate a changed function.
- Labs: statically linked program with libc functions to identify; crypto-constant scavenger hunt; v1 vs v2 of a program with a silent bug fix.
- Challenge: identify the hash and cipher in a stripped binary and decrypt a seeded blob.
- Checkpoint: why constants beat names for identification. Transfer: find the patched function between two unseen builds.

#### 12 Decompiler Internals and Analysis Scripting
- Core, 8 h. Prereqs: 09.
- Context: decompilation research (Cifuentes' 1994 thesis), structuring algorithms, and why decompilers are heuristic.
- Can do: describe the pipeline (disassembly, lifting to an IR such as Ghidra P-code, data-flow analysis, type recovery, control-flow structuring); predict and spot failure modes (wrong function boundaries, bad prototypes, aliasing, irreducible control flow, overlapping instructions, missed tail calls, misidentified switch tables); fix them with overrides; write Ghidra scripts in Java and Python (PyGhidra or Jython) and a headless analysis; write an r2pipe script for radare2.
- Labs: binaries crafted to break the decompiler, with fixes; a script that renames functions from log strings; a headless batch report.
- Challenge: a stripped binary with 200 generated functions where only one contains the seeded check; find it with a script, not by hand.
- Checkpoint: why decompiler output must be verified against assembly. Transfer: script a query over an unseen binary.

### Phase D: Dynamic Analysis

#### 13 Debugger Fundamentals
- Core, 6 h. Prereqs: 07.
- Context: how debuggers work (`ptrace`, Mach exception ports, Windows debug API) and how software breakpoints replace a byte with `int3`.
- Can do: in LLDB and GDB (command map side by side), set breakpoints, step, inspect registers and memory, set watchpoints, change values, and script simple automation (LLDB Python, GDB Python); debug a stripped binary by address with ASLR in mind.
- Labs: guided sessions on module 06/07 binaries; the same session in LLDB and GDB.
- Challenge: a stripped binary that computes a seeded key at runtime and never stores it in the file.
- Checkpoint: hardware vs software breakpoints. Transfer: extract a runtime value from an unseen binary.

#### 14 System Calls, Tracing, and Interposition
- Core, 5 h. Prereqs: 08, 13.
- Context: the user/kernel boundary and why every useful program ends in system calls.
- Can do: explain the syscall instruction and calling convention on Linux x86_64 and macOS; trace with `strace`/`ltrace` (Linux) and `dtruss`/`fs_usage` (macOS, with SIP limits explained); interpose functions with `LD_PRELOAD` and `DYLD_INSERT_LIBRARIES` (and why hardened runtime blocks the latter).
- Labs: trace file and network activity of a lab program; a preload library that logs `strcmp` arguments.
- Challenge: recover a seeded password by interposing the comparison function, without a debugger.
- Checkpoint: why `ltrace` misses statically linked calls. Transfer: map an unseen program's file activity.

#### 15 Frida in Depth and Runtime Secrets
- Core, 8 h. Prereqs: 13, 14.
- Context: dynamic binary instrumentation and why injected JavaScript became the field's universal tool.
- Can do: attach and spawn; `Interceptor.attach`/`replace`; read and write memory; call native functions with `NativeFunction`; scan memory; trace with `frida-trace`; use Stalker for code tracing; hook Objective-C methods; write a reusable agent with a Python host.
- Labs: hook a lab program's check function; dump decrypted strings; replace a return value.
- Challenge (Phase D checkpoint): a multi-stage binary that decrypts its secret only at runtime, with a time gate; extract it with both LLDB and Frida.
- Checkpoint: when Frida beats a debugger and when it does not. Transfer: instrument an unseen binary to log every call to one function.

#### 16 Emulation, DBI, Replay, and Fuzzing
- Elective, 10 h. Prereqs: 15.
- Context: when you cannot or should not run code natively; partial execution; the rise of coverage-guided fuzzing.
- Can do: emulate a single function with Unicorn and run a whole binary with QEMU user mode; write a basic Pin or DynamoRIO tool (instruction count, memory trace); record and replay with `rr` (Linux) and explain time-travel debugging (WinDbg TTD); fuzz a parser with AFL++ (source build and QEMU mode) and use crashes and coverage to understand code.
- Labs: Unicorn harness for a decryption routine; DBI tracer; `rr` session on a nondeterministic bug; AFL++ on a format parser.
- Challenge: a seeded decryption routine that only runs on a machine with a specific hostname; emulate it instead of satisfying the check.
- Checkpoint: emulation vs DBI vs debugger trade-offs. Transfer: emulate an unseen function.

### Phase E: Modification

#### 17 Patching, Hooking, and Code Signing
- Core, 8 h. Prereqs: 10, 13.
- Context: patching for interoperability and bug fixing; why modern OSes verify code signatures.
- Can do: convert between virtual addresses and file offsets; patch bytes (flip branches, force return values, NOP-out) in ImHex and with LIEF; re-sign on macOS (`codesign -s -`); find code caves; write a trampoline hook; compare static patching with runtime hooking.
- Labs: patch a crackme three different ways; inline hook with a trampoline.
- Challenge: patch a seeded binary so it prints its hidden success message; `check.py` runs the patched file and verifies that only the intended bytes changed.
- Checkpoint: why the patched binary crashed before re-signing. Transfer: patch an unseen binary's check.

### Phase F: Platforms and Advanced Targets

#### 18 Memory Corruption and Mitigations
- Core, 8 h. Prereqs: 06, 13.
- Context: the Morris worm (1988) and "Smashing the Stack for Fun and Profit" (1996); the mitigation arms race since.
- Can do: explain stack and heap overflows, use-after-free, integer overflow, and format string bugs at the level needed to recognize them in disassembly; identify mitigations and their artifacts: stack canaries (`__stack_chk_fail`), NX/DEP, ASLR and PIE, RELRO, FORTIFY_SOURCE, CFG and CET shadow stacks, ARM PAC and BTI, macOS hardened runtime; check them with `checksec`-style tooling.
- Labs: the same vulnerable function built with and without each mitigation, compared in disassembly and in the debugger. Exploitation beyond crash analysis is out of scope.
- Challenge: identify every mitigation in five seeded binaries and the vulnerable function in one of them.
- Checkpoint: what a canary does and does not stop. Transfer: mitigation report for an unseen binary.

#### 19 Symbolic Execution, SMT, and Taint
- Elective, 10 h. Prereqs: 10, 12. Required for specialist track S1.
- Context: King (1976) symbolic execution; SMT solvers; concolic testing (DART, CUTE, SAGE).
- Can do: model constraints in Z3 (bit-vectors, arrays); solve a crackme with angr (find/avoid addresses, hooks); trace symbolically with Triton; explain concolic execution and path explosion; run a taint analysis to find which input bytes reach a comparison.
- Labs: Z3 puzzles; angr on module 10 crackmes; Triton taint on a parser.
- Challenge: a seeded crackme with a path explosion trap; solve it by constraining the right part only.
- Checkpoint: why symbolic execution stalls on hash loops. Transfer: solve an unseen crackme with a solver.

#### 20 ARM64
- Core, 8 h. Prereqs: 07.
- Context: ARM's RISC heritage and its move into servers and Macs.
- Can do: read AArch64 (`x0`-`x30`, `sp`, `pc`, `xzr`), load/store architecture, AAPCS64 calling convention, condition flags and `csel`/`cbz`, addressing modes, PAC instructions; compare the same C on x86_64 and ARM64; run ARM64 natively on Apple Silicon or with `qemu-aarch64` elsewhere.
- Labs: module 07 constructs recompiled for ARM64; universal (fat) binaries with `lipo`.
- Challenge: an ARM64-only seeded crackme.
- Checkpoint: why ARM64 needs more instructions for a constant load. Transfer: reconstruct an unseen ARM64 function.

#### 21 Reversing C++
- Core, 8 h. Prereqs: 09.
- Context: the Itanium C++ ABI (used by GCC and Clang everywhere but MSVC) vs the MSVC ABI.
- Can do: demangle names (`c++filt`); recover classes from constructors; read vtables and RTTI; recognize `this` passing, virtual calls, multiple inheritance adjustments, templates, STL containers (`std::string`, `std::vector`), and exceptions (`__cxa_throw`, unwind tables); rebuild the hierarchy in Ghidra.
- Labs: class hierarchies with and without RTTI; STL-heavy program at `-O2`.
- Challenge: a stripped seeded program with a virtual-dispatch validation chain.
- Checkpoint: how to find a vtable from a constructor. Transfer: recover an unseen class hierarchy.

#### 22 Rust and Go Binaries
- Elective, 6 h. Prereqs: 21.
- Context: memory-safe languages are now common in tooling and malware; their runtimes change what a binary looks like.
- Can do: recognize Rust (name mangling v0 and legacy, panics, slices as pointer+length, `Option`/`Result` layouts) and Go (runtime, goroutines, its register-based ABI (amd64 since Go 1.17; arm64, ppc64, and ppc64le since 1.18), `pclntab` for recovering function names, string headers); use language-aware plugins and scripts.
- Labs: the same small program in C, Rust, and Go, compared.
- Challenge: seeded crackmes in Rust and Go.
- Checkpoint: why Go binaries keep function names even when stripped. Transfer: find `main` logic in an unseen Go binary.

#### 23 Managed Runtimes, Bytecode, and WebAssembly
- Elective, 8 h. Prereqs: 09.
- Context: bytecode keeps types and names, so decompilation is close to exact; obfuscators exist because of that.
- Can do: decompile .NET (ILSpy, dnSpyEx) and Java (CFR, JADX); unpack and read Android APKs (apktool, smali, JADX); disassemble and decompile WebAssembly (WABT `wasm2wat`, `wasm-decompile`); read Python bytecode (`dis`); explain how an interpreter or bytecode VM dispatches, which leads into track S1.4.
- Labs: one seeded check in C#, Java, Kotlin/Android, Wasm, and Python, each built from source here.
- Challenge: the Wasm and Android variants, solved without running them.
- Checkpoint: why .NET decompiles better than C. Transfer: an unseen bytecode crackme.

#### 24 Windows Internals for Reversers
- Elective, 8 h. Prereqs: 08, 13. Runs in a Windows VM.
- Context: the NT architecture, Win32 vs Native API.
- Can do: walk the PE loader path; read the TEB and PEB (module list, `BeingDebugged`); explain SEH on x86 and table-based exception handling on x64, VEH; trace user-to-kernel transitions (`ntdll` stubs, syscall numbers, why they change across builds); recognize API hashing and dynamic resolution; use x64dbg and WinDbg.
- Labs: programs built from source with MinGW or MSVC in the VM; PEB walking; an API-hash resolver.
- Challenge: a seeded PE that resolves its imports by hash.
- Checkpoint: why malware walks the PEB. Transfer: resolve the hashed imports of an unseen PE.

#### 25 Linux and macOS Internals for Reversers
- Elective, 8 h. Prereqs: 08, 14.
- Context: two Unix lineages, two loaders, one ABI family.
- Can do: Linux: process startup (`_start`, `__libc_start_main`, auxv), vDSO, `/proc`, seccomp basics; macOS: `dyld` and the shared cache (extracting libraries), Objective-C runtime (`objc_msgSend`, selectors, class metadata, `class-dump`-style recovery), Swift metadata and name demangling (`swift demangle`), XPC basics, SIP and TCC as analysis constraints.
- Labs: trace startup on both systems; recover classes from an Objective-C program and a Swift program built here.
- Challenge: an Objective-C seeded check reached through `objc_msgSend`.
- Checkpoint: why `objc_msgSend` breaks naive call graphs. Transfer: map the classes of an unseen Objective-C binary.

#### 26 Anti-Analysis, Anti-Tamper, and Licensing
- Core, 8 h. Prereqs: 15, 17.
- Context: the economics of software protection, DRM, and licensing; what protection can and cannot achieve (a determined analyst with the binary can always read it; protection raises cost).
- Can do: recognize and bypass debugger detection (`ptrace(PT_DENY_ATTACH)`, `sysctl` P_TRACED, `IsDebuggerPresent`), timing checks, integrity checks (self-hashing), environment and VM checks; explain licensing schemes (online activation, signed license files, hardware binding) and DRM building blocks (white-box crypto, secure enclaves) at a conceptual level.
- Labs: a repo-built binary with five layered checks, each defeated with a script, a patch, or a hook.
- Challenge: a seeded protected binary with integrity checks that detect naive patches.
- Checkpoint: why an integrity check breaks breakpoints. Transfer: identify the protections in an unseen binary.
- Scope: only repo-built training binaries. No circumvention of third-party commercial protection.

#### 27 Packing and Obfuscation Fundamentals
- Core, 10 h. Prereqs: 26.
- Context: packers began as compressors (UPX) and became protectors; obfuscation theory (Collberg, Thomborson, Low 1997 taxonomy; Barak et al. 2001 impossibility of general obfuscation).
- Can do: recognize a packed binary (entropy, few imports, stub); unpack UPX and a custom packer by finding the original entry point and dumping memory; recognize string encryption, opaque predicates, control-flow flattening, instruction substitution, MBA expressions, and virtualization at the survey level, and choose the matching specialist technique.
- Labs: custom packer built here; the same function under each obfuscation, produced with an LLVM pass or a source transformer in this repo.
- Challenge: unpack a seeded custom packer and solve the inner crackme.
- Checkpoint: why dumping at the OEP works. Transfer: unpack an unseen layer.

### Phase G: Professional Practice

#### 28 Professional Practice: Reporting, Reproducibility, Law, Disclosure
- Core, 4 h. Prereqs: 10.
- Context: RE as evidence; findings that cannot be reproduced do not count.
- Can do: keep an analysis log (hashes, tool versions, commands, timestamps); write a report with executive summary, method, findings, and evidence an independent analyst can verify; version Ghidra projects and scripts; explain the legal frame in general terms (contract and EULA terms, anti-circumvention law such as DMCA section 1201 and its security-research exemption in the US, the EU Software Directive interoperability provisions) and when to seek legal advice; follow coordinated vulnerability disclosure (ISO/IEC 29147, vendor programs, CERT/CC).
- Labs: rewrite a past module's notes into a report; a mock disclosure email to a fictional vendor.
- Checkpoint: what makes a finding reproducible. Transfer: a one-page report on a module 10 crackme.
- Note: legal content is orientation, not legal advice.

#### 29 Capstone
- Core, 15 h. Prereqs: all core modules.
- Can do: analyze an unseen multi-feature binary (triage, static, dynamic, patch or keygen) and deliver a module 28 report.
- Labs: one seeded capstone binary per learner combining C++, a custom protocol, runtime decryption, and one anti-analysis layer.
- Specialization option: a learner on a specialist track may substitute a track capstone (for example, deobfuscating a protected binary for track S1, or analyzing a sample they bring in an isolated VM for track S2).

## Specialist Tracks
Taken after the listed core prerequisites, in any order. Each track has its own placement check (its first module's checkpoint).

### S1 Obfuscation and Deobfuscation
Prereqs: core through 15, plus 19. S1.1 can start after 07.

| ID | Module | Hours | Status |
| :--- | :--- | ---: | :--- |
| S1.1 | Mixed Boolean-Arithmetic (MBA) with Z3 | 6 | built |
| S1.2 | Opaque Predicates | 6 | spec |
| S1.3 | Control-Flow Flattening | 8 | spec |
| S1.4 | Virtualization-Based Protection | 12 | spec |
| S1.5 | Symbolic Deobfuscation at Scale | 10 | spec |
| S1.6 | Program Synthesis for Deobfuscation | 8 | spec |
| S1.7 | Research Methods: Benchmarks and Metrics | 6 | spec |

- **S1.1 MBA with Z3 (built).** Context: MBA expressions mix arithmetic and bitwise operators over n-bit integers (Zhou et al., 2007). Can do: explain why identities such as `x + y == (x ^ y) + 2*(x & y)` hold mod 2^n; read an MBA-obfuscated check in disassembly; lift it to a Z3 expression; prove an equivalence or find a counterexample; solve for the accepted input; observe what the optimizer does to MBA at `-O2`. Labs and challenge: see `modules/s1-01-mba/`.
- **S1.2 Opaque Predicates.** Can do: explain invariant (always true/false) and contextual predicates, number-theoretic constructions (for example `x*(x+1) % 2 == 0`), and detect them statically with an SMT query per branch and dynamically with coverage. Labs: a source-level obfuscator in this repo inserting seeded predicates. Checkpoint transfer: remove the dead branches of an unseen function.
- **S1.3 Control-Flow Flattening.** Can do: recognize the dispatcher loop and state variable, recover the original CFG by symbolically executing each block to its next state, and rebuild it with a Ghidra script or a Miasm/angr pipeline. Labs: flattening via an LLVM pass built here. Transfer: unflatten an unseen function.
- **S1.4 Virtualization-Based Protection.** Can do: find the VM entry, dispatcher, handlers, and virtual registers; write a disassembler for the bytecode; lift it to C or an IR; discuss devirtualization approaches. Labs: a small repo-built VM protector with seeded opcode permutation. Transfer: write a disassembler for an unseen opcode table.
- **S1.5 Symbolic Deobfuscation at Scale.** Can do: use Triton, Miasm, and angr on obfuscated traces; simplify expressions with SMT plus rewriting; recognize anti-symbolic techniques (for example, input-dependent loops and hash-based predicates) and their limits. Transfer: simplify an unseen obfuscated trace.
- **S1.6 Program Synthesis for Deobfuscation.** Can do: explain sampling-based synthesis of semantically equivalent simple expressions (Syntia 2017, QSynth 2020, Xyntia 2021) and MBA simplifiers (MBA-Blast 2021, SiMBA 2022, GAMBA 2023); run one tool; compare to SMT-based simplification. Transfer: simplify an unseen MBA set and report accuracy.
- **S1.7 Research Methods.** Can do: build a reproducible obfuscation benchmark (Tigress or LLVM-based passes over a fixed corpus), measure potency, resilience, stealth, and cost (Collberg et al.), and report results with variance. Output: a short methods section suitable for a thesis.

### S2 Malware Analysis (isolated VM only)
Prereqs: 15, 17, 24 or 25, 26, 27, 28. No malware is included in or downloaded by this repo.
- **S2.1 Lab Safety and Setup (4 h).** Build an isolated, snapshotted analysis VM: host-only or no networking, no shared folders, no clipboard sharing, simulated services (INetSim or FakeNet-NG), revert after each session. Checkpoint: the tutor audits the VM checklist before any sample work starts.
- **S2.2 Triage and Behavioral Analysis (8 h).** Static triage, sandbox-style behavioral monitoring (Procmon, Sysmon, `strace`), indicators of compromise.
- **S2.3 Unpacking and Config Extraction (10 h).** Real-world packers and loaders, extracting C2 configuration, writing an extractor.
- **S2.4 Detection Engineering (6 h).** YARA rules from analysis, testing for false positives on clean corpora.
- **S2.5 Reporting (4 h).** Malware report with IOCs, ATT&CK mapping, and reproducible method.
- Samples: the learner obtains them, inside the VM only, from research sources they are entitled to use. Training substitutes built here (benign programs with malware-like behavior) are used for all graded labs.

### S3 Firmware and Embedded
Prereqs: 08, 13, 20.
- **S3.1 Firmware Extraction (6 h).** Image formats, `binwalk`, compression and file systems (SquashFS, JFFS2), finding the base address of raw images.
- **S3.2 Bare-Metal Code (8 h).** ARM Cortex-M (Thumb-2, vector table, MMIO peripherals) and MIPS basics; loading raw images correctly in Ghidra with a memory map from a datasheet.
- **S3.3 Emulation and Rehosting (8 h).** QEMU system and user modes, Unicorn, and peripheral modeling.
- **S3.4 Hardware Interfaces Overview (4 h).** UART, JTAG, SWD at the conceptual level; only on hardware the learner owns.
- Labs: firmware images built from source in this repo with an embedded toolchain (`arm-none-eabi-gcc`).

### S4 Mobile
Prereqs: 15, 20, 23 (Android) or 25 (iOS).
- **S4.1 Android (10 h).** APK structure, DEX/smali, JNI native libraries, Frida on an emulator, certificate pinning concepts on a repo-built app.
- **S4.2 iOS (10 h).** App bundle, Mach-O ARM64, Objective-C and Swift, entitlements, Frida on a device or simulator the learner controls, using a repo-built app.
- Scope: apps the learner builds or is authorized to test.

### S5 Protocol and File Format Reversing
Prereqs: 02, 09, 15.
- **S5.1 File Formats (8 h).** Differential analysis of files, ImHex patterns, Kaitai Struct specs, checksums and compression fields.
- **S5.2 Network Protocols (8 h).** Capturing with Wireshark, framing and state machines, writing a dissector (Lua or Kaitai), replay and fuzzing with a format-aware fuzzer.
- Labs: a repo-built client/server pair with a seeded custom protocol and a matching file format.

## Learning Records (the knowledge base)
Created per learner in `notes/` by `make init-notes` from `notes/_templates/` (gitignored, so personal progress never enters the public repo).

| File | Purpose |
| :--- | :--- |
| `profile.md` | Background, goals, path and placement result, teaching preferences, environment |
| `progress.md` | Module status (with mastery level) and the exact resume point |
| `journal/` | One entry per session |
| `glossary.md` | Every term learned, with its module |
| `cheatsheets/` | Commands, instruction patterns, tool tips |
| `mistakes.md` | Misconceptions and the corrected model |
| `review-queue.md` | Spaced-repetition items with box and due date |

## Tooling Reference
Install commands for macOS (Homebrew) and Debian/Ubuntu. Versions and links: `resources.md`.

| Category | Tool | macOS | Linux (Debian/Ubuntu) | From module |
| :--- | :--- | :--- | :--- | :--- |
| Compiler | clang or gcc | `xcode-select --install` | `sudo apt install build-essential clang` | 00 |
| Binutils | `file`, `strings`, `nm`, `objdump`, `xxd` | Xcode CLT | `sudo apt install binutils file xxd` | 00 |
| Format inspectors | `otool` / `readelf`, LIEF | Xcode CLT, `pip install lief` | binutils, `pip install lief` | 01, 08 |
| Disassembler/decompiler | Ghidra (JDK 21+) | `brew install --cask ghidra` | release zip from GitHub + `sudo apt install openjdk-21-jdk` | 04 |
| Alternative | radare2 / Cutter, rizin | `brew install radare2`, `brew install --cask cutter` | distro package or release | 12 |
| Debugger | LLDB, GDB (+ GEF or pwndbg) | Xcode CLT (LLDB) | `sudo apt install gdb lldb` | 13 |
| Tracing | `dtruss` / `strace`, `ltrace` | built in (SIP limits) | `sudo apt install strace ltrace` | 14 |
| Instrumentation | Frida | `pip install frida-tools` | `pip install frida-tools` | 15 |
| Emulation, DBI, fuzzing | Unicorn, QEMU, Pin, DynamoRIO, rr, AFL++ | `pip install unicorn`, `brew install qemu` | `pip install unicorn`, `sudo apt install qemu-user rr afl++` | 16 |
| Hex editor | ImHex | `brew install --cask imhex` | release AppImage | 17 |
| Solvers | Z3, angr, Triton | `pip install z3-solver angr` | same | 19, S1 |
| Cross targets | mingw-w64, aarch64 and x86_64 cross gcc | `brew install mingw-w64` | `sudo apt install gcc-mingw-w64 gcc-x86-64-linux-gnu gcc-aarch64-linux-gnu` | 08, 20 |

Use a Python virtual environment for pip installs (`python3 -m venv .venv && . .venv/bin/activate`).
