#!/usr/bin/env python3
"""Build module 01 targets.

build/greet            two-file program with symbols and debug info (lab reference)
build/greet-stripped   same program, stripped
challenge/vault.o      seeded object file: encoded token, seeded symbol names, local symbols stripped
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
import relab  # noqa: E402

MODULE = "01"


def expected() -> str:
    return relab.token(MODULE)


def vault_defines() -> dict:
    secret = expected().encode()
    key = relab.derive_int(MODULE, "key", 1, 255)
    step = relab.derive_int(MODULE, "step", 3, 97) | 1
    blob = bytes(b ^ ((key + i * step) & 0xFF) for i, b in enumerate(secret))
    return {
        "ENTRY": relab.derive_ident(MODULE, "entry", "vault_"),
        "DECOY": relab.derive_ident(MODULE, "decoy", "vault_"),
        "SINK": relab.derive_ident(MODULE, "sink", "sink_"),
        "KEY": key,
        "STEP": step,
        "LEN": len(secret),
        "BLOB": relab.c_bytes(blob),
    }


def main() -> int:
    src = HERE / "src"
    relab.compile_c([src / "main.c", src / "greet.c"], HERE / "build" / "greet", debug=True)
    stripped = relab.compile_c([src / "main.c", src / "greet.c"], HERE / "build" / "greet-stripped")
    relab.strip(stripped)
    vault = relab.compile_c(src / "vault.c", HERE / "challenge" / "vault.o",
                            defines=vault_defines(), object_only=True)
    relab.strip(vault, local_only=True)
    print("Built build/greet, build/greet-stripped, and challenge/vault.o.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
