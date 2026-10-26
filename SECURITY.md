# Security Policy

This repository contains training material, not a deployed service. "Security issue" here means a problem with the course itself.

## What to report
- An instruction or lab that is unsafe for the learner's machine (for example running unknown code outside a controlled environment, or weakening host protections).
- A challenge whose answer leaks: it can be solved from the repository alone, without the learner's seed.
- Real malware, third-party protected software, or a link to either committed to the repo (none is allowed; see `AGENTS.md`).
- A command that deletes or overwrites data outside the module folder.

## How to report
Open a private security advisory on GitHub (Security tab, "Report a vulnerability"). If that is unavailable, open an issue titled "Security: <short description>" without exploit details and ask for a private channel.

You should get a first reply within 7 days. Confirmed problems are fixed on `main` and noted in `CHANGELOG.md`.

## Out of scope
Vulnerabilities in tools the course uses (Ghidra, LLDB, and so on): report those to their projects. Following the course's own disclosure guidance (module 28) applies to any issue you find in third-party software.
