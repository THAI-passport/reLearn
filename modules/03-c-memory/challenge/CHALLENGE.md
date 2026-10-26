# Challenge: Reassemble the token

`challenge/vault` is stripped. It keeps a secret token in three pieces: one in a global variable, one in a heap block, and one in a buffer on the stack. Run it with a path for its memory dump:
```bash
./challenge/vault work/dump.bin
```
It prints one line per piece, in token order:
```
piece <number> at <address> length <bytes>
```
and writes `work/dump.bin`, a snapshot of three memory cells taken during that same run (addresses change on every run because of ASLR, so always use the dump and the printout from one run).

Dump format (all integers little-endian):
```
offset 0   4 bytes   magic "MEMD"
offset 4   4 bytes   number of cells (3)
then, for each cell:
           8 bytes   base address of the cell in the process
           8 bytes   size of the cell in bytes
           <size>    the cell's bytes
```
Each piece sits somewhere inside one of the cells, next to filler text that looks like the token but is not part of it.

Your task: find which cell each printed address falls in, extract each piece (its address minus the cell's base gives the offset, and the length is printed), and join the pieces in piece-number order. Write the token on one line to `my-answer.txt`, then run `python3 check.py`.

Rules
- Do the address arithmetic yourself. `xxd` and `python3` as a calculator are fine; reading the pieces out of the binary with a disassembler is not (that comes later).
- Decide, from the addresses, which cell is the global, the heap block, and the stack buffer, and be ready to explain how you know (lesson step 1).

Run `make` first. Every learner's token is different.
