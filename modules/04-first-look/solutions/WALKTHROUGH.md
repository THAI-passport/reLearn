# Module 04 walkthrough (reveal only after an attempt; see the hint ladder in AGENTS.md)

Hint ladder suggestions for the tutor:
1. "What does the program do with its command-line argument? Follow it in the decompiler from `main`."
2. "Find the function that `main` calls on `argv[1]`. What does it copy and append, and from where?"
3. "Two string literals are stored. Which one does the first copy use?"
4. "Run `strings` on the binary. The two fragments are the pieces; now decide their order from the code."

## Steps
1. Import `challenge/gate`, run auto-analysis, and find `main` (it checks `argc`, prints a usage message, and calls one helper).
2. The helper declares a local buffer, copies one piece into it, appends the other, and compares the buffer with the argument.
3. The two pieces are static strings. Which one is copied first depends on the build; read it from the decompiler output, not from the order they sit in memory or in `strings`.
4. Join the pieces in that order and run `./challenge/gate <password>` to confirm `access granted`.

`solutions/solve.py` takes a shortcut (it tries pairs of fragments from `strings`); the learner's route is the decompiler.

## Explain back
- Why was the order of the fragments in `strings` output no help?
- Which names in your decompiler view came from the file, and which did Ghidra invent?
