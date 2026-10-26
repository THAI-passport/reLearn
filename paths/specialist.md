# Path: Researcher or Specialist

For: practitioner-level skills (or a learner who has finished the core) with a research or professional focus. Tracks are defined in `goals.md`, "Specialist Tracks".

| Track | Focus | Core prerequisites | Track hours |
| :--- | :--- | :--- | ---: |
| S1 | Obfuscation and deobfuscation: MBA, opaque predicates, control-flow flattening, VM-based protection, symbolic execution and SMT (Z3, Triton), program synthesis | through 15, plus 19 (S1.1 needs only 07) | 56 |
| S2 | Malware analysis (isolated VM only) | 15, 17, 24 or 25, 26, 27, 28 | 32 |
| S3 | Firmware and embedded | 08, 13, 20 | 26 |
| S4 | Mobile (Android, iOS) | 15, 20, 23 or 25 | 20 |
| S5 | Protocol and file-format reversing | 02, 09, 15 | 16 |

Estimate: your entry path's hours up to the prerequisites, plus the track hours, plus 15% overhead. Example: a practitioner on S1 who skips 01-07 needs roughly 58 core hours (00 and 08-15) + 10 (module 19) + 56 (S1), so ~124 module hours, ~145 with overhead, plus any skip tests failed.

## Confirmation quiz (per track; the first track module's checkpoint is the formal gate)
- S1: Prove or refute `x + y == (x | y) + (x & y)` for 32-bit integers, by reasoning and then with Z3.
- S2: List the isolation properties your analysis VM must have before a sample is copied in.
- S3: How would you find the load address of a raw firmware image with no headers?
- S4: Where does an Android app's native code live in an APK, and how is it called from Java/Kotlin?
- S5: Given two captures of the same message with one field changed, how do you find the length and checksum fields?

## Tutor adjustments
- Pair each track module with a reading from `resources.md` and ask the learner to summarize the paper's method and threats to validity.
- Encourage a research log in `notes/journal/` that can feed a thesis methods chapter (module 28 and S1.7).
- Safety: S2 work does not start until the S2.1 VM checklist is audited. Samples are never copied into this repo.
