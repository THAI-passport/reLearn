#!/usr/bin/env python3
"""Reference solver for module 02 (tutor use, behind the hint ladder).

Runs the stripped stamp program, then decodes the record from its raw bytes with the
layout a learner derives by hand: little-endian, 1 padding byte after version,
4 tail padding bytes, 24 bytes total.
"""
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent

with tempfile.TemporaryDirectory() as tmp:
    out = Path(tmp) / "record.bin"
    subprocess.run([str(HERE / "challenge" / "stamp"), str(out)], check=True, capture_output=True)
    data = out.read_bytes()

if len(data) != 24:
    sys.exit(f"expected 24 bytes, got {len(data)}")
version, flags, delta, ident, ratio = struct.unpack("<BxHiQf4x", data)
bits = ",".join(str(b) for b in range(16) if flags >> b & 1)
print(f"version={version}\nflags={bits}\ndelta={delta}\nid={ident}\nratio={ratio}")
