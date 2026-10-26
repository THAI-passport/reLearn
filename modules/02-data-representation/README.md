# Module 02: Data Representation: Numbers, Bits, and Bytes

Kind: core. Time: about 5 hours. Prerequisites: module 00.

## Context
A binary file is just bytes, and so is memory. Every number, string, and struct you will meet as a reverser is some pattern of bits. The tools show you that pattern in hexadecimal, and you have to know how it is read.

Most of the conventions you will see were settled by history. Early machines represented negative numbers several ways (sign-magnitude, ones' complement). Two's complement won because the same adder circuit works for signed and unsigned numbers. Byte order split the industry into "little-endian" (Intel x86, and now most ARM systems) and "big-endian" (network protocols, many older RISC machines). Danny Cohen's 1980 note "On Holy Wars and a Plea for Peace" named the camps after Gulliver's Travels. Floating point was a mess of incompatible vendor formats until the IEEE 754 standard of 1985. Its single- and double-precision formats are what you will decode here.

## Objectives
After this module you can:
- Convert between binary, hexadecimal, and decimal, and read hex as groups of 4 bits.
- Apply AND, OR, XOR, NOT, shifts, and masks, and test or set a single bit.
- Read a two's complement value and explain why the same bits are -42 or 4294967254.
- Explain sign extension vs zero extension.
- Read little-endian multi-byte values in a hex dump.
- Decode an IEEE 754 single-precision float by hand (sign, exponent, mantissa).
- Predict type sizes, field offsets, alignment, and padding of a struct.

## Prerequisites
You can already:
- Build a module with `make` and run a program (module 00).
- Look at bytes with `xxd` (module 00).

## Commands on your platform
All captured output below comes from macOS 26 on Intel with Apple clang 17, building for x86_64. Linux x86_64 (and macOS under Rosetta) give the same values for everything in this module, because they share the LP64 data model and little-endian byte order. Windows is different: `long` is 4 bytes there (LLP64).

```bash
cd modules/02-data-representation
make
mkdir -p work
```

## Guided steps

### 1. Hexadecimal is shorthand for bits
One hex digit is exactly 4 bits, so `0x2A` is `0010 1010`. Predict before checking: what are `0xFF`, `0x80`, and `0x0F` in binary and in decimal?

Check your conversions with Python (any time you like):
```bash
python3 -c "print(hex(42), bin(42), int('2a', 16), int('101010', 2))"
```

### 2. Bit operations
Predict each line, then run:
```bash
./build/bits
```
First seven lines:
<!-- captured: ./build/bits, macOS 26 Intel, Apple clang 17.0.0 -->
```
x              0x0000002a  0000_0000_0000_0000_0000_0000_0010_1010
x << 4         0x000002a0  0000_0000_0000_0000_0000_0010_1010_0000
x >> 1         0x00000015  0000_0000_0000_0000_0000_0000_0001_0101
x & 0xF        0x0000000a  0000_0000_0000_0000_0000_0000_0000_1010
x | 0x100      0x0000012a  0000_0000_0000_0000_0000_0001_0010_1010
x ^ 0xFF       0x000000d5  0000_0000_0000_0000_0000_0000_1101_0101
~x             0xffffffd5  1111_1111_1111_1111_1111_1111_1101_0101
```
Idioms to recognize in binaries later:
| C | Meaning |
| :--- | :--- |
| `x & (1 << n)` | test bit n |
| `x \| (1 << n)` | set bit n |
| `x & ~(1 << n)` | clear bit n |
| `x ^ k` | flip the bits that are 1 in k (and `(x ^ k) ^ k == x`, the basis of XOR "encryption") |
| `x << n` | multiply by 2^n |
| `x & 0xF` | keep the low 4 bits (a mask) |

Checkpoint: why is XOR with the same key twice the identity? Where did you meet XOR in module 01?

### 3. Two's complement, signed and unsigned
<!-- captured: ./build/bits (continued) -->
```
-42            0xffffffd6  1111_1111_1111_1111_1111_1111_1101_0110
-42 read as unsigned: 4294967254
int8_t  0xFF widened: -1 (0xffffffff)
uint8_t 0xFF widened: 255 (0x000000ff)
INT32_MAX + 1 as unsigned: 2147483648, same bits as int32_t: -2147483648
-20 >> 2 (signed): -5, (uint32_t)-20 >> 2: 1073741819
```
- To negate in two's complement, invert all bits and add 1: `~42 = 0xffffffd5`, plus 1 gives `0xffffffd6` = -42.
- The bits do not know their type. The same 32 bits mean -42 as `int32_t` and 4294967254 as `uint32_t`. The code that uses them (and in assembly, the instruction) decides. Module 05 shows the signed and unsigned jump instructions that make this choice.
- Widening a signed byte copies the sign bit into the new upper bits (sign extension); widening an unsigned byte fills them with zeros (zero extension).
- Right-shifting a negative signed value keeps the sign (arithmetic shift) with clang and gcc. The C standard leaves this implementation-defined; unsigned shifts always fill with zeros (logical shift).

Checkpoint: a hex dump shows the 4 bytes `fe ff ff ff`. Give two different values they could be, and say what you would need to know to choose.

### 4. Byte order
<!-- captured: ./build/bits (last line) -->
```
0x11223344 in memory, lowest address first: 44 33 22 11
```
x86_64 is little-endian: the least significant byte is stored at the lowest address. A hex dump lists bytes from low to high address, so multi-byte numbers appear "backwards". Read them from right to left within the field.

Checkpoint: in network byte order (big-endian), how would the same value be stored?

### 5. IEEE 754 floats
```bash
./build/floats
```
<!-- captured: ./build/floats -->
```
1          0x3f800000  sign 0  exponent 127 (2^0   )  mantissa 0x000000
-1         0xbf800000  sign 1  exponent 127 (2^0   )  mantissa 0x000000
1.5        0x3fc00000  sign 0  exponent 127 (2^0   )  mantissa 0x400000
2          0x40000000  sign 0  exponent 128 (2^1   )  mantissa 0x000000
0.75       0x3f400000  sign 0  exponent 126 (2^-1  )  mantissa 0x400000
-13.375    0xc1560000  sign 1  exponent 130 (2^3   )  mantissa 0x560000
0.1        0x3dcccccd  sign 0  exponent 123 (2^-4  )  mantissa 0x4ccccd
0          0x00000000  sign 0  exponent   0 (2^-127)  mantissa 0x000000
-0         0x80000000  sign 1  exponent   0 (2^-127)  mantissa 0x000000
inf        0x7f800000  sign 0  exponent 255 (2^128 )  mantissa 0x000000
nan        0x7fc00000  sign 0  exponent 255 (2^128 )  mantissa 0x400000
0.1f + 0.2f == 0.3f ? yes
0.1 + 0.2 == 0.3 (double) ? no
```
A 32-bit float is 1 sign bit, 8 exponent bits (stored with a bias of 127), and 23 mantissa bits. For normal numbers:

value = (-1)^sign x 1.mantissa (binary) x 2^(exponent - 127)

Worked example, `-13.375` = `0xc1560000`:
- `0xc1560000` = `1 10000010 10101100000000000000000`
- sign 1, so negative. Exponent `10000010` = 130, so 2^(130-127) = 2^3.
- mantissa `.1010110`, so 1.1010110 (binary) = 1 + 1/2 + 1/8 + 1/32 + 1/64 = 1.671875.
- 1.671875 x 8 = 13.375.

Special cases: exponent 0 means zero or a subnormal number (the program's "2^-127" label does not apply there). Exponent 255 means infinity (mantissa 0) or NaN (mantissa non-zero). `0.1` has no exact binary form, so its mantissa is a rounded repeating pattern (`...cccd`). That is why one equality test above happens to be true for `float` and false for `double`. Never rely on either.

Checkpoint: decode `0x3f400000` by hand, then explain why 0.75 needs an exponent of 126.

### 6. Sizes, alignment, and padding
Read `src/record.h` first. Predict the offset of each field and the total size, then run:
```bash
./build/layout
```
<!-- captured: ./build/layout -->
```
char 1, short 2, int 4, long 8, long long 8, pointer 8, float 4, double 8
struct record: size 24, align 8
  version @0  flags @2  delta @4  id @8  ratio @16
struct reordered: size 24
struct wasteful: size 24, struct compact: size 16
```
The rule: each field starts at a multiple of its own size (its alignment), and the whole struct is padded to a multiple of its largest alignment.
- `version` (1 byte) at 0, then 1 byte of padding so `flags` (2 bytes) starts at 2.
- `delta` (4) at 4, `id` (8) at 8, `ratio` (4) at 16, then 4 bytes of tail padding so the size (24) is a multiple of 8.
- Reordering helps sometimes (`wasteful` 24 vs `compact` 16) and sometimes not (`record` and `reordered` are both 24, because of tail padding).

Padding bytes are not guaranteed to be zero. Whatever was in memory stays there, and that can leak data into files and network packets.

### 7. Decode a record from raw bytes
`build/stamp` writes one `struct record` to a file exactly as it sits in memory. Its values are in `build.py` (`DEMO`). Predict the dump first, then check:
```bash
./build/stamp work/demo.bin
xxd -g 1 work/demo.bin
```
<!-- captured: the commands above -->
```
wrote 24 bytes to work/demo.bin
00000000: 02 aa 05 01 fe ff ff ff 88 77 66 55 44 33 22 11  .........wfUD3".
00000010: 00 00 c0 3f aa aa aa aa                          ...?....
```
| Offset | Bytes | Field | Value |
| :--- | :--- | :--- | :--- |
| 0 | `02` | version | 2 |
| 1 | `aa` | padding | (left over from `memset`) |
| 2 | `05 01` | flags | `0x0105`: bits 0, 2, 8 set |
| 4 | `fe ff ff ff` | delta | `0xfffffffe` = -2 |
| 8 | `88 77 66 55 44 33 22 11` | id | `0x1122334455667788` |
| 16 | `00 00 c0 3f` | ratio | `0x3fc00000` = 1.5 |
| 20 | `aa aa aa aa` | tail padding | |

Checkpoint: if `stamp` had been compiled for a big-endian machine, which rows of this table would change, and which would not?

## Challenge
Read `challenge/CHALLENGE.md`. The stripped `challenge/stamp` writes a record with values derived from your seed. Decode all five fields by hand.

## Checkpoint
Answer without notes first. The tutor grades with the mastery rubric in `AGENTS.md`.
1. Why is `0xFFFFFFFF` both 4294967295 and -1? What decides which one a program means?
2. How can you tell the byte order of a file format from a hex dump when you know one field's value?
3. Where does struct padding come from, and why might it contain leftover data?
4. Decode `0xc1560000` as a float and show your steps.
5. (Module 01) The challenge program is stripped. Which names can `nm challenge/stamp` still show you, and do any of them help here?

Transfer task: the tutor gives an unseen struct definition and a hex dump of one instance written on x86_64. Decode every field and mark every padding byte.

Review-queue seeds: sign vs zero extension; why tail padding exists; how to spot little-endian in a dump; what the exponent bias is for.
