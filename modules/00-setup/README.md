# Module 00: Setup and Sanity Check

## Objectives
After this module you can:
- Verify your machine has a working RE toolchain and know which tools are still missing.
- Build a C program and tell what kind of binary it produced (`file`).
- Extract human-readable text from a binary (`strings`) and look at raw bytes (`xxd`).
- Explain why a stripped binary is harder to read than one with symbols.

Prerequisites: none. Time: 30-60 minutes.

## Steps (the tutor walks you through these one at a time)

### 1. Check the environment
```bash
python3 tools/check_env.py
```
Read the output. Required tools must all be `[ok]`. Ghidra is optional for now; it is installed in module 03.

Checkpoint question: what CPU architecture is your machine, and why does that matter for the binaries you will analyze?

### 2. Build the lab
```bash
cd modules/00-setup
make
```
This produces two binaries from the same `src/hello.c`:
- `build/hello`: compiled with debug info and symbols.
- `challenge/mystery`: stripped.

Read `src/hello.c` first. Predict: what does the program print? Then run `./build/hello` and check.

### 3. Identify the binary
```bash
file build/hello challenge/mystery
```
Checkpoint question: what is the file format and architecture? What would it say on Linux?

### 4. Look inside
```bash
nm build/hello
nm challenge/mystery
strings build/hello
xxd build/hello | head -20
```
Compare the `nm` output of the two binaries. What disappeared in the stripped one, and why does that matter to a reverser?

Note: the `strings`, `nm`, and `otool` on your PATH may come from different packages (for example Anaconda vs Apple). Run `which strings nm otool` and note which one you use.

### 5. Challenge
Read `challenge/CHALLENGE.md`, find the token in `challenge/mystery`, put it in `my-answer.txt`, and run:
```bash
python3 check.py
```

## Wrap-up
Answer in your own words (the tutor records them in `notes/`):
1. What does `strip` remove, and what does it leave?
2. Why did `strings` work even on the stripped binary?
3. Name one thing `strings` cannot tell you about a program.

Then update `notes/profile.md` (environment section) and ask the tutor to `wrap up`.
