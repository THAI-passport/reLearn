# Reverse Engineering Learning Lab

A self-paced reverse engineering (RE) course taught by an AI coding agent, for learners at any starting level: from no C at all, to security practitioners who want rigorous RE and tooling, to researchers in obfuscation, malware, firmware, mobile, or protocol analysis.

The first milestone is the same for everyone: take a compiled C program, disassemble and decompile it, and explain what the original source did. The course then covers linking and loading, Ghidra and scripting, debuggers, tracing, Frida, emulation and fuzzing, patching, mitigations, symbolic execution, ARM64, C++, Rust and Go, managed runtimes, OS internals, anti-analysis, packing and obfuscation, and professional practice.

## How it works
- **The AI agent is your tutor.** It follows `AGENTS.md`, so any agent that reads `AGENTS.md` works (Claude Code, Codex, Cursor, and others).
- **Placement first.** In the first session the tutor runs a short diagnostic (`paths/placement.md`) and picks one of five paths (`paths/`). You can skip a module only by passing its checkpoint.
- **You do the work.** You predict, run the commands, and explain. The tutor guides and checks, and gives hints on a ladder instead of answers.
- **Mastery, not exposure.** A module is done when you pass its checkpoint against a rubric. Spaced-repetition reviews bring old material back at the start of each session.
- **Your own challenges.** Each module has labs built from C source and a stripped challenge whose answer is derived from your personal random seed (`.seed`), so answers cannot be looked up. `check.py` gives objective pass/fail feedback.
- **Your knowledge base.** `notes/` holds your profile, progress, journal, glossary, cheatsheets, mistakes, and review queue. It stays on your machine (gitignored).

## Quick start
```bash
git clone https://github.com/THAI-passport/RElearn.git
cd RElearn
make init-notes        # create your notes/ from notes/_templates/
make check-env         # check tools and print your platform route
```
Then open the folder in your AI agent and say: `Start the course.`

## Platform routes
Labs target x86_64. `tools/check_env.py` detects your host, builds and runs a test program, and prints your route.

| Host | Route |
| :--- | :--- |
| macOS, Intel | Native. Install Xcode Command Line Tools: `xcode-select --install`. |
| macOS, Apple Silicon | Labs build with `clang -arch x86_64` and run under Rosetta 2 (`softwareupdate --install-rosetta --agree-to-license`). ARM64 is taught natively in module 20. |
| Linux, x86_64 | Native. Debian/Ubuntu: `sudo apt install build-essential clang gdb binutils file xxd make python3`. |
| Linux, ARM64 | `sudo apt install gcc-x86-64-linux-gnu qemu-user`, or set `RELAB_NATIVE=1` to build native ARM64 labs (the lesson listings will then not match yours). |
| Windows | Install WSL2 (`wsl --install`, then Ubuntu) and follow the Linux x86_64 route inside it. For PE and Windows-internals work (modules 08 and 24), use a separate Windows VM with no shared folders. Building PE files from source works from WSL2 with `x86_64-w64-mingw32-gcc` (`sudo apt install gcc-mingw-w64`). |

The lessons show macOS and Linux commands side by side where they differ. Captured output in the lessons comes from macOS on Intel; your addresses and some details will differ.

## Paths
| Path | For | Rough total |
| :--- | :--- | :--- |
| Absolute beginner | No C, no assembly | ~235 h |
| Rusty programmer | Some C or assembly, long ago | ~200 h |
| Developer new to security | Strong coding, no RE | ~185 h |
| Practitioner / CTF player | Exploitation basics, wants rigor and tooling | ~170 h |
| Researcher / specialist | Practitioner skills plus a track (obfuscation and MBA, malware, firmware, mobile, protocols) | entry path + track |

Details and assumptions: `paths/README.md`.

## Where things are
| Path | What it is |
| :--- | :--- |
| `goals.md` | Curriculum: phases, module index, full module specs, specialist tracks, tools |
| `paths/` | Placement diagnostic, learner paths, time estimates |
| `modules/` | Built modules: lessons, labs, challenges, checkers, gated solutions |
| `notes/_templates/` | Templates for your knowledge base (`notes/` itself is gitignored) |
| `tools/` | `check_env.py`, `relab.py` (seeded build helper), `notes.py`, `selftest.py` |
| `resources.md` | Books, papers, CTFs, and tools |
| `AGENTS.md` | The tutor's protocol |
| `CONTRIBUTING.md` | How to add a module, review checklist |

Built modules so far: 00, 01, 02, and specialist module S1.1 (MBA with Z3). The others are fully specified in `goals.md`, and the tutor builds each one when you reach it.

## Things to say to the tutor
`where am I`, `next`, `quiz me`, `review`, `hint`, `explain differently`, `go deeper`, `context first`, `skip ahead`, `change path`, `wrap up`.

## Safety and ethics
All exercises use binaries built from source in this repo. Use these techniques only on software you own or are authorized to analyze. This repo contains no malware and never downloads any. The malware track runs only in an isolated, snapshotted VM with no network or shared folders, using samples you bring. Module 28 covers the legal and disclosure basics (orientation, not legal advice).

## License
Code (tools, build and check scripts, lab sources): MIT. Course text: CC BY-SA 4.0. See `LICENSE`.
