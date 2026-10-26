# Learner Paths and Placement

The same modules serve everyone. A path only changes **where you start, what you may skip by passing a checkpoint, which electives you take, and how fast the tutor moves.** Module details and hours are in `goals.md`.

## How placement works
1. In the first session the tutor runs the diagnostic in `placement.md` (about 20 minutes, no tools needed beyond a terminal).
2. The tutor proposes a path from the decision table below, the learner confirms or adjusts, and the tutor records it in `notes/profile.md` (section "Placement").
3. The learner's path file has its own confirmation quiz. If the learner misses more than two of its items, the tutor moves them one path earlier.
4. **Skipping is earned, never self-assessed.** A module may be skipped only by passing its checkpoint (explain-back questions, the module challenge with `check.py`, and the transfer task) at mastery level 3 or higher in the rubric in `AGENTS.md`. Record a skip in `notes/progress.md` as `Skipped (checkpoint passed)` with the date. A failed skip attempt simply means the learner takes the module, starting at the step the checkpoint showed was weak.
5. The learner can change path at any time. The tutor re-runs the relevant part of the diagnostic first.

## Decision table
| Diagnostic result | Path | File |
| :--- | :--- | :--- |
| Cannot write a small C loop, or has never used a terminal | Absolute beginner | `beginner.md` |
| Writes simple C with help; pointers and assembly are rusty or never learned | Rusty programmer (default) | `rusty.md` |
| Fluent in at least one language, comfortable with C or willing; no RE or assembly | Developer new to security | `developer.md` |
| Reads x86 assembly, has used a debugger and done basic exploitation or CTF reversing | Security practitioner / CTF player | `practitioner.md` |
| Practitioner-level skills plus a research or professional focus (obfuscation, malware, firmware, mobile, protocols) | Researcher / specialist | `specialist.md` |

## Time estimates
Estimates are module hours from `goals.md` plus overhead for review, journaling, and retries (25% for the beginner path, 15% for the others). Real pace varies by a factor of two in either direction; the tutor recalculates from the learner's actual hours after five sessions and records the new estimate in `notes/profile.md`.

| Path | Route | Module hours | With overhead | Weeks at 5 h/week | Weeks at 10 h/week |
| :--- | :--- | ---: | ---: | ---: | ---: |
| Absolute beginner | P0 + all 24 core modules | 187 | ~235 | ~47 | ~24 |
| Rusty programmer | All 24 core modules | 172 | ~200 | ~40 | ~20 |
| Developer new to security | Core, with 01-03 often skipped by checkpoint | ~160 | ~185 | ~37 | ~19 |
| Practitioner / CTF | Core with 01-07 and 18 often skipped, plus electives 16 and 19 | ~147 | ~170 | ~34 | ~17 |
| Specialist | Practitioner route (or own prior path) + one track | + track hours | see `specialist.md` | | |

Electives total 50 hours (16, 19, 22, 23, 24, 25). Any learner may add them.
