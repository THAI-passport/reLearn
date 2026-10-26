#!/usr/bin/env python3
"""Check module 00.

Pass condition: my-answer.txt contains the token hidden in challenge/mystery.
Run after `make`.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402
from build import relab  # noqa: E402


def main() -> int:
    answer = relab.read_answer(relab.answer_arg(HERE),
                               "create modules/00-setup/my-answer.txt containing the token you found.")
    if answer is None:
        return 1
    return relab.verdict(answer == build.token(),
                         "you found the token in a stripped binary using command-line triage.",
                         "that is not the token. Re-check your strings output (the token starts with RE-).")


if __name__ == "__main__":
    sys.exit(main())
