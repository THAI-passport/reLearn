# notes/

Your personal knowledge base: profile, progress, journal, glossary, cheatsheets, mistakes, review queue.

- Create it with `make init-notes` (or `python3 tools/notes.py init`). Existing files are never overwritten.
- Start over with `make reset-notes`: the current notes are moved to `notes/_archive/<timestamp>/`, not deleted.
- Everything here except `_templates/` and this README is gitignored, so your progress stays on your machine. To version it, use a private fork and remove the `notes/*` lines from `.gitignore`.
- The tutor reads and updates these files every session (see `AGENTS.md`).
