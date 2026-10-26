# Reverse Engineering Learning Lab

A self-paced course that teaches reverse engineering from scratch, taught by an AI coding agent. You do not need to know assembly, and your C can be rusty. By the end of Phase C you will be able to take a compiled C program, disassemble and decompile it, and explain what the original source did. Later phases cover debuggers, Frida, patching, ARM64, C++, anti-analysis, and packing.

## How it works
- The AI agent is your tutor. It reads `AGENTS.md` for its teaching rules, so any agent that supports `AGENTS.md` (Claude Code, Codex, Cursor, and others) works.
- You learn by predicting, doing, and explaining. You run the commands; the tutor guides, checks, and gives hints without handing out answers.
- Your progress is the knowledge base in `notes/`: a session journal, glossary, cheatsheets, a log of your mistakes, and a review queue the tutor uses to quiz you at the start of each session.
- Each module has a lesson, labs built from C source, a stripped challenge binary, and a `check.py` that tells you objectively whether you solved it.

## Quick start
1. Clone the repo (or fork it, so your `notes/` become your own).
2. Open the folder in your AI agent and say: `Start the course.`
3. The tutor interviews you, fills `notes/profile.md`, runs the environment check, and begins Module 00.

Manual environment check:
```bash
python3 tools/check_env.py
```

## What you need
- macOS or Linux (Windows: WSL2 for the Linux track, a VM for Windows binaries)
- A C compiler (clang or gcc), Python 3, and a terminal
- Later: Ghidra (needs JDK 21+), LLDB or GDB, Frida
- Roughly 3-6 hours per week; the full course is open-ended and you set the pace

## Where things are
| Path | What it is |
| :--- | :--- |
| `goals.md` | The curriculum, outcomes per phase, and tool list |
| `modules/` | Lessons, labs, challenges, and checkers |
| `notes/` | Your knowledge base (progress, journal, glossary, cheatsheets, mistakes, review queue) |
| `tools/` | Helper scripts such as the environment check |
| `AGENTS.md` | Instructions for the tutor agent |

## Useful things to say to the tutor
`where am I`, `next`, `quiz me`, `review`, `hint`, `explain differently`, `go deeper`, `wrap up`.

## Safety and ethics
All exercises use binaries built from source in this repo. Do not use these techniques on software you do not own or have permission to analyze. Hostile samples belong only in an isolated, snapshotted VM with no network or shared folders.
