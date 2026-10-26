#!/usr/bin/env python3
"""Check module 01.

Pass condition: my-answer.txt contains the token that challenge/vault.o hands to the
function you had to provide. Run `make` first.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402
from build import relab  # noqa: E402


def main() -> int:
    answer = relab.read_answer(relab.answer_arg(HERE),
                               "create modules/01-source-to-binary/my-answer.txt containing the token.")
    if answer is None:
        return 1
    if answer == build.expected():
        return relab.verdict(True, "you linked a foreign object file, supplied its missing symbol, "
                             "and recovered a token that strings could not see.", "")
    if answer.startswith("RE-") and len(answer) == len(build.expected()):
        return relab.verdict(False, "", "right shape, wrong token. Did you rebuild after changing "
                             "your seed, and did you call the right exported function?")
    return relab.verdict(False, "", "that is not the token. The token starts with RE- and is "
                         "printed by the function you provide, not found with strings.")


if __name__ == "__main__":
    sys.exit(main())
