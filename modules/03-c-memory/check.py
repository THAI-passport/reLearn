#!/usr/bin/env python3
"""Check module 03. Pass condition: my-answer.txt holds the full token that challenge/vault split across
a global, a heap block, and a stack buffer."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402
from build import relab  # noqa: E402


def main() -> int:
    text = relab.read_answer(relab.answer_arg(HERE),
                             "create modules/03-c-memory/my-answer.txt (format in challenge/CHALLENGE.md).")
    if text is None:
        return 1
    want = build.expected()
    if text == want:
        return relab.verdict(True, "you mapped addresses to regions and reassembled the token from raw memory.", "")
    hint = "not the token yet."
    if len(text) != len(want):
        hint += f" The token has {len(want)} characters; yours has {len(text)}."
    elif text.startswith("RE-") and sorted(text) == sorted(want):
        hint += " The right characters, in the wrong order: check the piece numbers."
    return relab.verdict(False, "", hint)


if __name__ == "__main__":
    sys.exit(main())
