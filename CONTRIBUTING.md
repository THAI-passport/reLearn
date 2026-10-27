# Contributing

Contributions are welcome: new modules (built from the specs in `goals.md`), fixes, ports to other hosts, and better explanations. Keep the course's rules: no emojis, concise technical tone, real tool output only, and safe training targets.

## Add a module
1. Pick a module with status `spec` in the `goals.md` module index. Its spec (outcomes, labs, challenge, checkpoint) is the contract.
2. Copy the template: `cp -R modules/_template modules/NN-short-name`, and replace `NN` in `build.py`.
3. Write the C sources in `src/`. Build everything in `build.py` with `tools/relab.py`:
   - `relab.compile_c(...)` for symbol builds (`debug=True`) and challenge builds, then `relab.strip(...)`.
   - Derive every secret with `relab.token`, `relab.derive_int`, or `relab.derive_ident`. Never hard-code an answer, and never write generated secrets to a tracked file.
4. Write `check.py`. It uses `relab.answer_arg` (so `--answer-file` works) and prints `PASS:` or `FAIL:` with a hint that does not leak the answer.
5. Write `solutions/solve.py`. It must derive the answer from the built artifacts (the way a learner would: `nm`, `objdump`, running the program, parsing a file), not from the seed, and print the exact content of a correct `my-answer.txt`.
6. Run `python3 tools/selftest.py NN`. It builds with several seeds and checks that the right answer passes, a wrong answer fails, and another seed's answer fails.
7. Write the lesson `README.md`: context, objectives, prerequisites, steps with predictions and checkpoint questions, and the module checkpoint. Paste only output you captured from a real build, labeled with the command and host. Give Linux commands next to macOS ones.
8. Change the module's status in `goals.md` from `spec` to `built`, and mention it in `README.md`.

## Pull requests and CI
`main` is protected: open a pull request. CI runs `tools/lint.py` and `tools/check_env.py` plus `tools/selftest.py` on Ubuntu and macOS, and both selftest jobs must pass before merging. Run `make lint` and `make selftest` locally first. Update `CHANGELOG.md` for curriculum changes.

## Review checklist
- [ ] Matches its `goals.md` spec; prerequisites and objectives are can-do statements.
- [ ] Context section present (for context-first learners).
- [ ] Every lab has a symbol build and a stripped challenge build.
- [ ] Secrets come only from `tools/relab.py`; nothing secret is committed. Build outputs are gitignored.
- [ ] `python3 tools/selftest.py NN` passes. Paste its output into the pull request.
- [ ] Every output block in the lesson was captured from a real build, and the label names the command and host.
- [ ] macOS and Linux commands given where they differ; anything not tested on a platform is marked as untested.
- [ ] Checkpoint has 3-5 explain-back questions, one question from an earlier module, a transfer task, and review-queue seeds.
- [ ] `solutions/` contains `WALKTHROUGH.md` with a hint ladder and `solve.py`.
- [ ] No real malware, no third-party protected software, no instructions for bypassing commercial protection.
- [ ] No learner-specific content (no names, theses, or personal progress); `notes/` changes go only to `notes/_templates/`.
- [ ] Links and citations added to `resources.md` were opened and checked.
- [ ] No emojis.

## Changing the curriculum
Edit `goals.md` and keep the module index, the progress template (`notes/_templates/progress.md`), and `paths/README.md` hour totals consistent. If you renumber modules, add a mapping to "Changes from v1" in `goals.md` so existing learners can migrate their `notes/progress.md`.

## Licensing of contributions
By contributing you agree that code is licensed under MIT and course text under CC BY-SA 4.0 (see `LICENSE`).
