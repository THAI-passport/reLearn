# Path: Rusty Programmer (default)

For: learned some C or assembly in the past, rusty now; may have a security background.
Route: every core module in order (00-15, 17, 18, 20, 21, 26-29). Electives by interest; 19 is recommended for anyone heading to track S1.
Estimate: ~200 hours (see `README.md`).

## Confirmation quiz (at the start of module 01)
1. What does `sizeof(int)` usually return on x86_64, and what about `sizeof(long)` on macOS/Linux vs Windows?
2. Write a function that reverses a C string in place.
3. Explain a pointer to a struct and how `p->x` relates to `(*p).x`.
4. Convert `0x7F`, `0x80`, and `0xFF` to signed 8-bit values.
5. Name the four compile stages.

Missing three or more: move to the beginner path for P0 only, then return.

## Tutor adjustments
- Re-teach C concepts as they appear, through memory and the binary, without assuming fluency.
- Modules 01-03 are rarely skipped on this path; their checkpoints are short, so attempting a skip is cheap.
- Use comparisons often (`-O0` vs `-O2`, debug vs stripped, source vs decompiler).
