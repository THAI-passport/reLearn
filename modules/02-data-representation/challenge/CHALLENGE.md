# Challenge: Decode the stamp

`challenge/stamp` is stripped. Run it to write one record to a file:
```bash
./challenge/stamp challenge/record.bin
```
The record is a `struct record` from `src/record.h`, written on x86_64 exactly as it sits in memory:
```c
struct record {
    uint8_t  version;
    uint16_t flags;
    int32_t  delta;
    uint64_t id;
    float    ratio;
};
```
Decode every field from the raw bytes (`xxd -g 1 challenge/record.bin`) and write them to
`my-answer.txt` in this format:
```
version=<decimal>
flags=<numbers of the bits that are set, lowest first, comma separated, e.g. 0,2,8>
delta=<decimal>
id=<decimal>
ratio=<decimal>
```
Then run `python3 check.py`. It tells you how many fields are right.

Rules
- Work out the offsets and padding yourself (lesson step 6), then decode each field by hand.
- You may use `python3` as a calculator (for example `int('...', 16)`), but decode the float
  from its sign, exponent, and mantissa first, and only then check it with a tool.
- Do not read values out of the program with a disassembler; that comes in a later module.

Run `make` first. Every learner's record is different.
