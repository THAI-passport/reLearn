#!/usr/bin/env python3
"""Check module NN. Pass condition: (describe it)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402
from build import relab  # noqa: E402


def main() -> int:
    answer = relab.read_answer(relab.answer_arg(HERE), "create my-answer.txt in this module folder.")
    if answer is None:
        return 1
    return relab.verdict(answer == build.expected(), "(what the learner proved)", "(a hint that does not leak the answer)")


if __name__ == "__main__":
    sys.exit(main())
