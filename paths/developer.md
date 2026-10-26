# Path: Developer New to Security

For: strong programmer (any language), comfortable reading C, little or no assembly, no RE.
Route: core modules in order. Attempt the checkpoints of 01, 02, and 03 as skip tests. Recommended electives: 19 and 22 or 23 (match your language background).
Estimate: ~185 hours (see `README.md`).

## Confirmation quiz (first session)
1. Explain stack vs heap allocation and lifetime with a C or C++ example.
2. What is undefined behavior, and why might a compiler delete a check that depends on it?
3. Explain dynamic linking and name the macOS or Linux tool that lists a binary's libraries.
4. What does a debugger breakpoint actually do to the program?
5. Read a 10-line C function with pointer arithmetic and say what it returns.

Missing three or more: switch to the rusty path.

## Tutor adjustments
- Lean on their strengths: have them write the C that a disassembly came from, and write solvers and scripts early (module 12 scripting fits well).
- Spend the saved time in Phase B; assembly is the new skill.
- Introduce the security mindset explicitly: attacker models, why checks fail, mitigations (module 18).
