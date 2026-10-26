#!/usr/bin/env python3
"""Reference solver for module 01 (tutor use, behind the hint ladder).

Does what the learner does: list vault.o's symbols with nm, provide every undefined
symbol that the C library does not, call every exported function, and read the token.
"""
import platform
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
import relab  # noqa: E402

vault = HERE / "challenge" / "vault.o"
nm = subprocess.run([relab.tool("nm"), str(vault)], capture_output=True, text=True, check=True).stdout
prefix = "_" if platform.system() == "Darwin" else ""


def c_name(sym: str) -> str:
    return sym[len(prefix):] if prefix and sym.startswith(prefix) else sym


exported = [c_name(m) for m in re.findall(r"^\s*[0-9a-fA-F]+ T (\S+)$", nm, re.M)]
undefined = [c_name(m) for m in re.findall(r"^\s+U (\S+)$", nm, re.M)]
# Names starting with "__" (stack protector and friends) come from the C library.
to_provide = [u for u in undefined if not u.startswith("__")]

main_c = ["#include <stdio.h>"]
main_c += [f'void {u}(const char *m) {{ printf("%s\\n", m); }}' for u in to_provide]
main_c += [f"void {e}(void);" for e in exported]
main_c += ["int main(void) {"] + [f"    {e}();" for e in exported] + ["    return 0;", "}"]

with tempfile.TemporaryDirectory() as tmp:
    src = Path(tmp) / "main.c"
    src.write_text("\n".join(main_c) + "\n")
    exe = Path(tmp) / "solve"
    relab.compile_c([src, vault], exe)
    out = subprocess.run([str(exe)], capture_output=True, text=True, check=True).stdout

found = re.findall(r"RE-[0-9a-f]{8}", out)
if not found:
    sys.exit("no token printed:\n" + out)
print(found[0])
