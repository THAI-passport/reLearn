# Repo-level helpers. Module builds live in modules/NN-name/Makefile.
.PHONY: help check-env init-notes reset-notes notes-status selftest lint

help:
	@echo "make check-env     check the toolchain and print your platform route"
	@echo "make init-notes    create your notes/ knowledge base from notes/_templates (never overwrites)"
	@echo "make reset-notes   archive notes/ to notes/_archive/<timestamp>/ and start fresh"
	@echo "make notes-status  show which notes files exist"
	@echo "make lint          author check: repo rules (no emojis, module structure, nothing secret tracked)"
	@echo "make selftest      author check: build every module and test its checker with wrong and right answers"

check-env:
	python3 tools/check_env.py

init-notes:
	python3 tools/notes.py init

reset-notes:
	python3 tools/notes.py reset

notes-status:
	python3 tools/notes.py status

selftest:
	python3 tools/selftest.py

lint:
	python3 tools/lint.py
