# Path: Security Practitioner or CTF Player

For: knows exploitation basics, reads some x86 assembly, has used GDB or a decompiler; wants rigorous RE and tooling.
Route: module 00, then skip tests for 01-07 and 18 (take any you fail), then the rest of the core with emphasis on 08, 11, 12, 15, 26, 27. Recommended electives: 16 and 19. Then a specialist track if wanted.
Estimate: ~170 hours including electives 16 and 19 (see `README.md`).

## Confirmation quiz (first session)
1. Walk through what happens on the first call to `puts` in a dynamically linked ELF (PLT/GOT) and how it differs on Mach-O.
2. Given a short `-O2` listing with a magic-number multiply, recover the division.
3. Explain why a decompiler can mis-type a function's arguments and how you would fix it in Ghidra.
4. Describe a workflow to recover a runtime-decrypted string with Frida.
5. Explain what symbolic execution can and cannot do on a crackme with a hash check.

Missing three or more: switch to the developer path (with 01-03 skip tests).

## Tutor adjustments
- Rigor over speed: require the learner to justify claims with evidence (addresses, listings, traces) and to keep the module 28 analysis log from the start.
- Prefer harder transfer tasks and timed triage.
- Push tooling depth: scripting (12), Frida internals (15), emulation and DBI (16), solvers (19).
