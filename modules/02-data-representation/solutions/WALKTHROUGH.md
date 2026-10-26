# Module 02 walkthrough (reveal only after an attempt; see the hint ladder in AGENTS.md)

Hint ladder suggestions for the tutor:
1. "How many bytes did stamp write, and does that match sizeof(struct record)?"
2. "Use `./build/layout` or the alignment rule to find each field's offset. Which bytes are padding?"
3. "x86_64 is little-endian: read each field's bytes from right to left."
4. "For delta, the top bit is set. What does that mean for an int32_t? For ratio, split the 32 bits into 1, 8, and 23."

## Steps
1. The file is 24 bytes: the same as `sizeof(struct record)` from `./build/layout`.
2. Offsets: version 0, padding 1, flags 2-3, delta 4-7, id 8-15, ratio 16-19, tail padding 20-23.
   The padding bytes all have the same value (the memset fill), which is a good sanity check.
3. Reverse each little-endian field:
   - flags: two bytes `lo hi` mean `0xhilo`; list the set bits (bit 0 is the lowest).
   - delta: the value is always negative here: value = (unsigned value) - 2^32.
   - id: eight bytes reversed, then convert hex to decimal.
   - ratio: four bytes reversed gives the IEEE 754 bit pattern; split into sign, exponent
     (subtract 127), and mantissa (prefix the implicit 1), then multiply out. The value is always a
     multiple of 1/8, so the mantissa terminates after a few bits.
4. Equivalent one-liner for checking (after doing it by hand):
   `python3 -c "import struct;print(struct.unpack('<BxHiQf4x', open('challenge/record.bin','rb').read()))"`
   The format string is the layout: `<` little-endian, `x` one padding byte, `4x` tail padding.

`solutions/solve.py` does steps 1-4 and prints the answer file.

## Explain back
- Why did the format string need `x` and `4x`?
- What would change in your decoding if the struct were declared with `__attribute__((packed))`?
