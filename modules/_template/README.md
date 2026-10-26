# Module NN: Title

Kind: core | elective | track. Time: N hours. Prerequisites: modules NN, NN (as can-do statements below).

## Context
For context-first learners the tutor starts here; for hands-on-first learners after the first lab.
Two or three short paragraphs: where this topic came from, why it exists, why a reverser cares.

## Objectives
After this module you can:
- (can-do statement, observable and testable)

## Prerequisites
You can already:
- (can-do statement from an earlier module)

## Concepts
Short sections, one idea each. Each starts with a prediction question for the learner.
Output blocks are captured from real builds and labeled like this:

<!-- captured: `command that produced it` on <host, compiler version>; addresses differ per machine -->
```
(paste real output only)
```

## Guided steps
Numbered steps with exact commands (macOS and Linux side by side where they differ).
Each ends with a checkpoint question.

## Challenge
`challenge/CHALLENGE.md` describes the task. Do not include the answer.

## Checkpoint
1-4. Explain-it-back questions (reasoning, not recall).
5. One question from an earlier module this one depends on.
Transfer task: one small task on a binary the learner has not seen.
Mastery: graded with the rubric in `AGENTS.md`; Done at level 3.

---
## Author checklist (delete when finished)
- [ ] Spec in `goals.md` matches objectives, prerequisites, labs, and checkpoint here
- [ ] Context section written (history and the why)
- [ ] `src/` compiles cleanly on macOS (x86_64 and via Rosetta) and Linux; Linux commands listed next to macOS ones
- [ ] Every lab has a symbol build and a stripped challenge build, both made by `build.py` through `tools/relab.py`
- [ ] Secrets come from `relab.token` / `relab.derive_int` / `relab.derive_ident` only
- [ ] `check.py` accepts `--answer-file` and gives objective PASS/FAIL
- [ ] `solutions/solve.py` reads the built artifacts (not the seed) and prints the answer file content
- [ ] `python3 tools/selftest.py NN` passes (wrong answer fails, right answer passes, across seeds)
- [ ] Every output block was captured from a real build and is labeled with command and host
- [ ] Review-queue seeds: 3-5 reasoning questions listed under Checkpoint
- [ ] `goals.md` status changed from spec to built
