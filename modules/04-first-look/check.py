#!/usr/bin/env python3
"""Check module 04. Pass condition: my-answer.txt holds the password that challenge/gate accepts."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402
from build import relab  # noqa: E402


def main() -> int:
    text = relab.read_answer(relab.answer_arg(HERE),
                             "create modules/04-first-look/my-answer.txt (format in challenge/CHALLENGE.md).")
    if text is None:
        return 1
    want = build.expected()
    if text == want:
        return relab.verdict(True, "you recovered a runtime-assembled password from decompiler output.", "")
    hint = "the gate does not accept that."
    if want.startswith(text) or want.endswith(text) or text in want:
        hint += " That is only part of the password: find how the two pieces are combined."
    elif text and text[::-1] == want:
        hint += " Reversed? Re-read the code that builds the expected string."
    elif sorted(text) == sorted(want):
        hint += " Right characters, wrong order: which piece is copied first?"
    return relab.verdict(False, "", hint)


if __name__ == "__main__":
    sys.exit(main())
