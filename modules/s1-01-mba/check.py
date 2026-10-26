#!/usr/bin/env python3
"""Check track S1.1.

Pass condition: my-answer.txt holds the one 32-bit number (decimal or 0x hex) that makes
challenge/gate print "open". Run `make` first.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402
from build import relab  # noqa: E402


def main() -> int:
    text = relab.read_answer(relab.answer_arg(HERE),
                             "create modules/s1-01-mba/my-answer.txt containing the number that opens the gate.")
    if text is None:
        return 1
    try:
        value = int(text.split()[0], 0)
    except (ValueError, IndexError):
        return relab.verdict(False, "", "write one number, in decimal or as 0x... hex.")
    if value != build.expected():
        return relab.verdict(False, "", "the gate stays closed for that number. Re-check your lifted "
                             "expression against the listing, instruction by instruction.")
    run = subprocess.run([str(HERE / "challenge" / "gate"), str(value)], capture_output=True, text=True)
    return relab.verdict(run.stdout.strip() == "open",
                         "you lifted an MBA-obfuscated check and solved it.",
                         "the number is right but challenge/gate disagrees; run `make` again.")


if __name__ == "__main__":
    sys.exit(main())
