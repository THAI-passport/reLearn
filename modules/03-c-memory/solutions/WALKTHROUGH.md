# Module 03 walkthrough (reveal only after an attempt; see the hint ladder in AGENTS.md)

Hint ladder suggestions for the tutor:
1. "Which of the three printed addresses are far from the other two? What does that say about the regions?"
2. "Read the dump header: magic, count, then base and size for each cell. Which cell contains your first address?"
3. "Address minus cell base gives the offset into the cell's bytes. Use the printed length to cut the piece out."
4. "Join the pieces in piece-number order, not in address order."

## Steps
1. Run `./challenge/vault work/dump.bin` once; keep both the printout and the dump from this run (addresses change per run).
2. Parse the dump: bytes 0-3 `MEMD`, bytes 4-7 count (3). Each cell: 8-byte base, 8-byte size (48), 48 bytes. All little-endian.
3. For each printed line, find the cell where `base <= address < base + 48`. Offset = address - base.
4. Take `length` bytes at that offset. The filler text before and after each piece is a decoy.
5. Concatenate in piece-number order. The result is the token (`RE-` plus 8 hex characters).

`solutions/solve.py` does exactly this.

## Explain back
- How can you tell which cell is the global, the heap block, and the stack buffer without the source?
- Why did the program print the pieces in piece-number order rather than address order, and why does that not reveal the regions?
- Why are the filler strings and the bytes after each piece's NUL still in the dump?
