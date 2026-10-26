#!/usr/bin/env python3
"""Check module 00.

Pass condition: my-answer.txt contains the token hidden in challenge/mystery.
Run after `make`.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build import token  # noqa: E402


def main() -> int:
    answer_file = HERE / "my-answer.txt"
    if not answer_file.exists():
        print("FAIL: create modules/00-setup/my-answer.txt containing the token you found.")
        return 1
    if answer_file.read_text().strip() == token():
        print("PASS: you found the token in a stripped binary using command-line triage.")
        return 0
    print("FAIL: that is not the token. Re-check your strings output (the token starts with RE-).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
