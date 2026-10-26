#!/usr/bin/env python3
"""Reference solver for module 03 (tutor use, behind the hint ladder).

Runs the stripped vault program, reads the piece addresses and lengths it prints, finds the dumped
cell that contains each address, and joins the pieces in order.
"""
import re
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent

with tempfile.TemporaryDirectory() as tmp:
    dump = Path(tmp) / "dump.bin"
    run = subprocess.run([str(HERE / "challenge" / "vault"), str(dump)], check=True, capture_output=True, text=True)
    data = dump.read_bytes()

if data[:4] != b"MEMD":
    sys.exit("bad dump magic")
(count,) = struct.unpack_from("<I", data, 4)
cells, pos = [], 8
for _ in range(count):
    base, size = struct.unpack_from("<QQ", data, pos)
    cells.append((base, data[pos + 16:pos + 16 + size]))
    pos += 16 + size

token = ""
for line in run.stdout.splitlines():
    m = re.fullmatch(r"piece (\d+) at (0x[0-9a-f]+) length (\d+)", line.strip())
    if not m:
        sys.exit(f"unexpected line: {line}")
    addr, length = int(m.group(2), 16), int(m.group(3))
    for base, blob in cells:
        if base <= addr < base + len(blob):
            off = addr - base
            token += blob[off:off + length].decode()
            break
    else:
        sys.exit(f"address {addr:#x} is in no dumped cell")
print(token)
