# Reverse Engineering Curriculum: From Zero to Advanced

## Mission
Teach reverse engineering from first principles to someone who knows little C and no assembly. The first milestone is concrete: **take a small compiled C program, disassemble it, decompile it, and explain what the original source did.** Everything after that adds tools and harder targets.

The course is LLM-tutored (see `AGENTS.md`) and self-paced. Progress and everything learned is recorded in `notes/` so the learner ends with a personal knowledge base.

## Principles
1. **C through the lens of memory.** C is revisited only as far as RE needs it: types and sizes, pointers, arrays, strings, structs, stack vs heap, and how they appear in a binary.
2. **Compile, then compare.** Learners always have the source for their first targets, so they can check their reading of the binary against the truth. Source-less challenges come after.
3. **One new idea at a time.** Predict, explain, do, check, reflect.
4. **Tools are introduced when the learner has felt the pain they solve.** Command-line triage first, then the disassembler, then the decompiler, then the debugger.
5. **Everything is recorded.** Journal, glossary, cheatsheets, mistakes, and a review queue for spaced repetition.
6. **Safe by default.** Only repo-built training binaries; isolated VM for anything hostile.

## Platform Scope
- Primary architecture: **x86_64**. Reason: most learning material, CTFs, and tooling assume it, and it runs natively on Intel Macs, Linux, and (via Rosetta) Apple Silicon.
- Later: **ARM64** (Apple Silicon, iOS, Android), and brief **x86 32-bit** conventions.
- Binary formats: **Mach-O** (macOS native), **ELF** (Linux, CTFs), **PE** (Windows). Introduced as each becomes relevant, not all up front.
- Host used by the first learner: macOS on Intel (x86_64). The course detects the host in module 00 and adapts.

## Outcomes by Phase (exit criteria)
| Phase | After this phase the learner can... |
| :--- | :--- |
| A. Foundations | Explain how C becomes a binary, what is in memory when a program runs, and read C pointer/array/struct code confidently. |
| B. Reading Assembly | Read small x86_64 functions, identify arguments, locals, branches, and loops, and map them back to C. |
| C. Static Analysis | Triage an unknown binary, navigate it in Ghidra, use the decompiler critically, and recover logic of simple crackmes. |
| D. Dynamic Analysis | Drive a debugger, inspect registers and memory at runtime, trace calls, and hook functions with Frida. |
| E. Modification | Patch a binary correctly and write keygens/solvers that pass a checker. |
| F. Advanced | Reverse C++ objects, handle other architectures/formats, and recognize and defeat basic anti-analysis and packing. |
| G. Capstone | Analyze an unseen binary end to end and write a professional report (and, if relevant, a thesis-aligned case study). |

## Curriculum

Each module lives in `modules/NN-name/` and follows the structure in `AGENTS.md`. Modules are authored just in time by the tutor; those marked "built" already exist.

### Phase A: Foundations
- **00 Setup and Sanity Check** (built). Install and verify the toolchain. Record host OS/CPU. First `file`, `strings`, `xxd` on a hello-world binary.
- **01 From Source to Binary.** The four compile stages (preprocess, compile, assemble, link). Object files vs executables. What a Mach-O/ELF file contains at a high level: headers, sections, symbols. Why stripped binaries are harder.
- **02 C Through the Lens of Memory.** Integer sizes and signedness, endianness, pointers, arrays, C strings and the null terminator, structs and padding, stack vs heap vs globals. Small programs that print addresses so the learner sees the layout.
- **03 First Look: Disassembler and Decompiler.** Run Ghidra on a known tiny C program. Compare decompiler output to the source. See what the decompiler gets right and wrong (names, types, loops). This delivers the first early win and motivates the assembly work that follows.

### Phase B: Reading Assembly (x86_64)
- **04 CPU, Registers, and Instructions.** Fetch-decode-execute, general purpose registers, `RIP`, `RSP`, flags. Intel vs AT&T syntax (the course uses Intel). Core instructions: `mov`, `lea`, `add`, `sub`, `cmp`, `test`, `jmp`/`jcc`.
- **05 Functions and the Stack.** `call`/`ret`, prologue/epilogue, stack frames, locals, the System V AMD64 calling convention (arguments in `rdi`, `rsi`, `rdx`, `rcx`, `r8`, `r9`; return in `rax`).
- **06 C Constructs in Assembly.** `if/else`, `for`/`while`, `switch` (jump tables), arrays and indexing, struct field access, string operations. Same code at `-O0`, `-O1`, `-O2` to see what the optimizer changes.
- **07 Assembly Checkpoint.** Three mystery functions to reconstruct as C without the decompiler. Checker compares behavior against the hidden original.

### Phase C: Static Analysis
- **08 Triage Workflow.** `file`, `strings`, `nm`, `otool -L`/`ldd`, symbols, imports, entropy. Build a repeatable first-10-minutes checklist.
- **09 Ghidra In Depth.** Project setup, Listing and Decompiler views, cross-references, renaming and retyping, function signatures, structs, control-flow graphs.
- **10 Crackme Series 1.** Plaintext compare, transformed strings (XOR, Caesar), checksum validation. Learner writes a keygen/solver for each.
- **11 Recognizing Algorithms.** Constants and patterns for Base64, CRC32, MD5/SHA, AES S-box, simple PRNGs; library function recognition (FLIRT-style thinking), `libc` calls.

### Phase D: Dynamic Analysis
- **12 Debugger Fundamentals (LLDB).** Breakpoints, stepping, registers, memory inspection, watchpoints, scripting basics. How breakpoints work (`int3`).
- **13 Tracing and Instrumentation.** `dtruss`/`strace`/`ltrace` equivalents, `DYLD_`/`LD_PRELOAD`-style interposition, Frida basics: hook a function, log args and return values.
- **14 Runtime Secrets.** Binary that decrypts data only at runtime; extract it with the debugger and with Frida. Time-gated and multi-stage challenge.

### Phase E: Modification
- **15 Binary Patching.** Byte-level patching, flipping branches, forcing return values, NOP-ing, file offsets vs virtual addresses, fixing code signature on macOS. Verify patch with the checker.
- **16 Code Caves and Hooking.** Finding free space, redirecting control flow, trampolines.

### Phase F: Advanced Targets
- **17 ARM64.** Registers (`x0`-`x30`, `sp`, `pc`), AAPCS, common instructions, reading the same C compiled for ARM64 (cross-compile on any host; run natively on Apple Silicon or emulate).
- **18 ELF and PE.** Sections/segments, PLT/GOT, dynamic loading; PE headers, IAT/EAT, Windows x64 calling convention. Analysis on provided binaries; running Windows code only inside a VM.
- **19 Reversing C++.** Name mangling, object layout, vtables, RTTI, constructors/destructors, exceptions. Recover class hierarchies in Ghidra.
- **20 Anti-Analysis.** `ptrace(PT_DENY_ATTACH)`, timing checks, debugger detection, and bypassing them with scripts and patches.
- **21 Packing and Obfuscation.** Packer stubs, OEP, memory dumping and unpacking a custom packer, control-flow flattening, opaque predicates.
- **22 Language Targets (optional).** Rust and Go binary quirks; managed code overview (.NET, Java) and when to use different tools.

### Phase G: Capstone
- **23 Capstone.** An unseen multi-feature binary: triage, static, dynamic, patch or keygen, and a written analysis report. If the thesis involves malware or protection analysis, the tutor and learner agree on an isolated VM setup first and a thesis-aligned case study replaces or extends this module.

## Learning Records (the knowledge base)
Located in `notes/`:
| File | Purpose |
| :--- | :--- |
| `profile.md` | Learner background, goals, host environment, pace |
| `progress.md` | Module status and exact resume point |
| `journal/` | One entry per session: what was done, what clicked, what was confusing |
| `glossary.md` | Every term learned, with the module it came from |
| `cheatsheets/` | Commands, instruction patterns, tool tips accumulated while learning |
| `mistakes.md` | Misconceptions and the corrected mental model |
| `review-queue.md` | Questions for spaced review at the start of sessions |

## Tooling Reference
| Category | Tool | Install (macOS, Homebrew) | Used from module |
| :--- | :--- | :--- | :--- |
| Compiler | clang (Xcode CLT) | `xcode-select --install` | 00 |
| Binary utilities | `file`, `strings`, `nm`, `otool`, `objdump`, `xxd` | included with Xcode CLT / macOS | 00 |
| Disassembler/decompiler | Ghidra (needs JDK 21+) | `brew install --cask ghidra` | 03 |
| Debugger | LLDB | included with Xcode CLT | 12 |
| Linux debugger | GDB with GEF/pwndbg | Docker or Linux VM | 12 (optional) |
| GUI triage | Cutter / radare2 | `brew install --cask cutter` | 08 (optional) |
| Hooking | Frida | `pip install frida-tools` | 13 |
| Hex editor | ImHex | `brew install --cask imhex` | 15 |

Linux users: use `apt`/`dnf` equivalents (`build-essential`, `gdb`, `binutils`, `ghidra`). Windows users: use WSL2 for the Linux track and a VM for PE analysis.
