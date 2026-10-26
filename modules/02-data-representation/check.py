#!/usr/bin/env python3
"""Check module 02.

Pass condition: my-answer.txt lists every field of the record written by challenge/stamp:

    version=<decimal>
    flags=<bit numbers that are set, comma separated, lowest first>
    delta=<decimal, may be negative>
    id=<decimal>
    ratio=<decimal>
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402
from build import relab  # noqa: E402


def parse(text: str) -> dict:
    out = {}
    for line in text.splitlines():
        if "=" not in line:
            continue
        key, value = (part.strip().lower() for part in line.split("=", 1))
        try:
            if key == "flags":
                out[key] = sorted(int(b, 0) for b in value.replace(" ", "").split(",") if b)
            elif key == "ratio":
                out[key] = float(value)
            elif key in build.FIELDS:
                out[key] = int(value, 0)
        except ValueError:
            out[key] = None
    return out


def main() -> int:
    text = relab.read_answer(relab.answer_arg(HERE),
                             "create modules/02-data-representation/my-answer.txt (format in challenge/CHALLENGE.md).")
    if text is None:
        return 1
    got = parse(text)
    want = build.expected()
    missing = [f for f in build.FIELDS if f not in got]
    wrong = [f for f in build.FIELDS if f in got and got[f] != want[f]]
    if not missing and not wrong:
        return relab.verdict(True, "you decoded endianness, padding, two's complement, bit flags, "
                             "and an IEEE 754 float from raw bytes.", "")
    parts = []
    if missing:
        parts.append("missing: " + ", ".join(missing))
    if wrong:
        parts.append("not right yet: " + ", ".join(wrong))
    right = len(build.FIELDS) - len(missing) - len(wrong)
    return relab.verdict(False, "", f"{right}/{len(build.FIELDS)} fields correct ({'; '.join(parts)}).")


if __name__ == "__main__":
    sys.exit(main())
