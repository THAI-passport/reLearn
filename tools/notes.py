#!/usr/bin/env python3
"""Create or reset a learner's knowledge base in notes/ from notes/_templates/.

    python3 tools/notes.py init     create any missing notes files (never overwrites)
    python3 tools/notes.py reset    archive current notes to notes/_archive/<timestamp>/, then init
    python3 tools/notes.py status   show which notes files exist and whether they are still templates

notes/ is gitignored except notes/_templates/, so personal progress never enters the public repo.
To version your own notes, keep them in a private fork and delete the `notes/*` lines in .gitignore.
"""
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTES = ROOT / "notes"
TEMPLATES = NOTES / "_templates"
# Template files that are copied into notes/ (journal-entry.md stays a template).
SKIP = {"journal-entry.md"}
DIRS = ["journal", "cheatsheets"]


def template_files():
    for path in sorted(TEMPLATES.rglob("*")):
        if path.is_file() and path.name not in SKIP:
            yield path, NOTES / path.relative_to(TEMPLATES)


def init() -> int:
    for d in DIRS:
        (NOTES / d).mkdir(parents=True, exist_ok=True)
    created = 0
    for src, dst in template_files():
        if dst.exists():
            print(f"  kept     {dst.relative_to(ROOT)}")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"  created  {dst.relative_to(ROOT)}")
        created += 1
    print(f"{created} file(s) created. Existing files were not touched.")
    return 0


def reset() -> int:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    archive = NOTES / "_archive" / stamp
    moved = 0
    for entry in sorted(NOTES.iterdir()):
        if entry.name.startswith("_") or entry.name.startswith("."):
            continue
        archive.mkdir(parents=True, exist_ok=True)
        shutil.move(str(entry), str(archive / entry.name))
        moved += 1
    if moved:
        print(f"Archived {moved} item(s) to {archive.relative_to(ROOT)} (nothing deleted).")
    return init()


def status() -> int:
    for src, dst in template_files():
        if not dst.exists():
            state = "missing"
        elif dst.read_bytes() == src.read_bytes():
            state = "template"
        else:
            state = "in use"
        print(f"  {state:<9} {dst.relative_to(ROOT)}")
    journals = [p for p in (NOTES / "journal").glob("*.md")] if (NOTES / "journal").exists() else []
    print(f"  {len(journals)} journal entr{'y' if len(journals) == 1 else 'ies'}")
    return 0


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    actions = {"init": init, "reset": reset, "status": status}
    if cmd not in actions:
        print(__doc__)
        return 2
    return actions[cmd]()


if __name__ == "__main__":
    sys.exit(main())
