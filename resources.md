# Resources

Books, references, papers, tools, and practice platforms used across the course. The **Module** column says where a resource first becomes useful.

Verification: every URL here was requested on 2026-10-26 and returned HTTP 200, except those marked *(fetch blocked)*. Those sites refused automated requests (HTTP 403); their URLs were confirmed through search listings, not by loading the page. Paper details (authors, venue, year) were checked against the publisher, DBLP, arXiv, or the authors' pages. Links rot: if one breaks, search for the title.

## Books
| Title | Notes | Module |
| :--- | :--- | :--- |
| Bryant and O'Hallaron, *Computer Systems: A Programmer's Perspective* ([site](https://csapp.cs.cmu.edu/)) | Data representation, machine-level code, linking, memory. The best companion to Phases A-B. | 01-07 |
| Dennis Yurichev, *Reverse Engineering for Beginners* ([beginners.re](https://beginners.re/)) | Free; compiler output for many constructs and architectures. | 05-07 |
| Dennis Andriesse, *Practical Binary Analysis* (No Starch, 2018) ([publisher](https://nostarch.com/binaryanalysis)) | ELF, disassembly, instrumentation, taint, symbolic execution. | 08, 16, 19 |
| Kara Nance and Chris Eagle, *The Ghidra Book*, 2nd ed. (No Starch, 2026) ([publisher](https://nostarch.com/ghidra-book-2e)) | Ghidra in depth, including PyGhidra and BSim. | 04, 09, 12 |
| John R. Levine, *Linkers and Loaders* ([author's site](https://www.iecc.com/linker/)) | Classic on linking, relocation, and loading. | 01, 08 |
| Michael Sikorski and Andrew Honig, *Practical Malware Analysis* (No Starch, 2012) ([publisher](https://nostarch.com/malware)) | Dated tooling, but the method still holds. | S2 |

## Specifications and references
| Reference | Module |
| :--- | :--- |
| [System V AMD64 psABI](https://gitlab.com/x86-psABIs/x86-64-ABI) | 06 |
| [Microsoft x64 calling convention](https://learn.microsoft.com/en-us/cpp/build/x64-calling-convention) | 06, 24 |
| [Intel 64 and IA-32 Software Developer's Manuals](https://www.intel.com/content/www/us/en/support/articles/000006715.html) *(fetch blocked)* | 05 |
| [ARM ABI documents (AAPCS64 and others)](https://github.com/ARM-software/abi-aa) | 20 |
| [ELF specification (Linux Foundation refspecs)](https://refspecs.linuxfoundation.org/elf/elf.pdf) | 08 |
| [PE format (Microsoft)](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format) | 08, 24 |
| [Itanium C++ ABI](https://itanium-cxx-abi.github.io/cxx-abi/abi.html) | 21 |
| [Rust v0 symbol mangling (RFC 2603)](https://rust-lang.github.io/rfcs/2603-rust-symbol-name-mangling-v0.html) | 22 |
| [Go internal ABI specification](https://github.com/golang/go/blob/master/src/cmd/compile/abi-internal.md) | 22 |
| [Python `dis` module](https://docs.python.org/3/library/dis.html) | 23 |
| Danny Cohen, "On Holy Wars and a Plea for Peace", IEN 137, 1980 ([text](https://www.rfc-editor.org/ien/ien137.txt)) | 02 |

## Papers
### Foundations and program analysis
- J. C. King, "Symbolic Execution and Program Testing", *Communications of the ACM* 19(7), 1976. [doi:10.1145/360248.360252](https://doi.org/10.1145/360248.360252) *(fetch blocked)*. Module 19.
- C. Cifuentes, *Reverse Compilation Techniques*, PhD thesis, Queensland University of Technology, 1994. Module 12. (No stable link checked.)
- Aleph One, "Smashing The Stack For Fun And Profit", *Phrack* 49, 1996. [phrack.org](http://phrack.org/issues/49/14.html). Module 18.

### Obfuscation and deobfuscation (track S1)
- C. Collberg, C. Thomborson, D. Low, "A Taxonomy of Obfuscating Transformations", Technical Report 148, University of Auckland, 1997. Modules 27, S1.7. (No stable link checked.)
- B. Barak et al., "On the (Im)possibility of Obfuscating Programs", CRYPTO 2001. [doi:10.1007/3-540-44647-8_1](https://doi.org/10.1007/3-540-44647-8_1). Module 27.
- Y. Zhou, A. Main, Y. X. Gu, H. Johnson, "Information Hiding in Software with Mixed Boolean-Arithmetic Transforms", WISA 2007, pp. 61-75. [doi:10.1007/978-3-540-77535-5_5](https://doi.org/10.1007/978-3-540-77535-5_5). Track S1.1.
- T. Blazytko et al., "Syntia: Synthesizing the Semantics of Obfuscated Code", USENIX Security 2017. [paper page](https://www.usenix.org/conference/usenixsecurity17/technical-sessions/presentation/blazytko), [code](https://github.com/RUB-SysSec/syntia). Track S1.6.
- R. David, L. Coniglio, M. Ceccato, "QSynth: A Program Synthesis based Approach for Binary Code Deobfuscation", BAR workshop at NDSS 2020. [doi:10.14722/bar.2020.23009](https://doi.org/10.14722/bar.2020.23009). Track S1.6.
- B. Liu et al., "MBA-Blast: Unveiling and Simplifying Mixed Boolean-Arithmetic Obfuscation", USENIX Security 2021. [paper page](https://www.usenix.org/conference/usenixsecurity21/presentation/liu-binbin), [code](https://github.com/softsec-unh/MBA-Blast). Track S1.6.
- G. Menguy, S. Bardin, R. Bonichon, C. de Souza Lima, "Search-Based Local Black-Box Deobfuscation: Understand, Improve and Mitigate" (Xyntia), ACM CCS 2021. [doi:10.1145/3460120.3485250](https://doi.org/10.1145/3460120.3485250) *(fetch blocked)*, [code](https://github.com/binsec/xyntia). Track S1.6.
- B. Reichenwallner, P. Meerwald-Stadler, "Efficient Deobfuscation of Linear Mixed Boolean-Arithmetic Expressions" (SiMBA), CheckMATE workshop at ACM CCS 2022. [doi:10.1145/3560831.3564256](https://doi.org/10.1145/3560831.3564256) *(fetch blocked)*, [arXiv:2209.06335](https://arxiv.org/abs/2209.06335), [code](https://github.com/DenuvoSoftwareSolutions/SiMBA). Track S1.1, S1.6.
- B. Reichenwallner, P. Meerwald-Stadler, "Simplification of General Mixed Boolean-Arithmetic Expressions: GAMBA", IEEE EuroS&P Workshops 2023. [arXiv:2305.06763](https://arxiv.org/abs/2305.06763), [code](https://github.com/DenuvoSoftwareSolutions/GAMBA). Track S1.6.

## Tools
| Tool | Purpose | Module |
| :--- | :--- | :--- |
| [Ghidra](https://github.com/NationalSecurityAgency/ghidra) | Disassembler, decompiler, scripting | 04 |
| [radare2](https://github.com/radareorg/radare2), [Cutter](https://cutter.re) | Disassembler, r2pipe scripting | 12 |
| [LLDB](https://lldb.llvm.org), [GDB](https://www.sourceware.org/gdb/), [GEF](https://github.com/hugsy/gef), [pwndbg](https://github.com/pwndbg/pwndbg) | Debuggers and GDB extensions | 13 |
| [x64dbg](https://x64dbg.com), [WinDbg time-travel debugging](https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/time-travel-debugging-overview) | Windows debugging, record and replay | 16, 24 |
| [Frida](https://frida.re) | Dynamic instrumentation | 15 |
| [Unicorn](https://www.unicorn-engine.org), [QEMU](https://www.qemu.org) | Emulation | 16 |
| [Intel Pin](https://www.intel.com/content/www/us/en/developer/articles/tool/pin-a-dynamic-binary-instrumentation-tool.html) *(fetch blocked)*, [DynamoRIO](https://dynamorio.org) | Dynamic binary instrumentation | 16 |
| [rr](https://rr-project.org) | Record and replay (Linux) | 16 |
| [AFL++](https://github.com/AFLplusplus/AFLplusplus) | Fuzzing, including QEMU mode for binaries | 16 |
| [ImHex](https://github.com/WerWolv/ImHex) | Hex editor with pattern language | 17, S5 |
| [LIEF](https://lief.re) | Parse and modify ELF, PE, Mach-O | 08, 17 |
| [checksec](https://github.com/slimm609/checksec) | Mitigation checks | 18 |
| [Z3](https://github.com/Z3Prover/z3), [angr](https://angr.io), [Triton](https://triton-library.github.io), [Miasm](https://github.com/cea-sec/miasm) | SMT, symbolic execution, taint, lifting | 19, S1 |
| [BinDiff](https://github.com/google/bindiff), [Diaphora](https://github.com/joxeankoret/diaphora) | Binary diffing | 11 |
| [YARA](https://github.com/VirusTotal/yara), [capa](https://github.com/mandiant/capa) | Pattern rules, capability detection | 11, S2 |
| [ILSpy](https://github.com/icsharpcode/ILSpy), [dnSpyEx](https://github.com/dnSpyEx/dnSpy) | .NET decompilers | 23 |
| [JADX](https://github.com/skylot/jadx), [Apktool](https://apktool.org), [CFR](https://www.benf.org/other/cfr/) | Android and Java | 23, S4 |
| [WABT](https://github.com/WebAssembly/wabt) | WebAssembly tools (`wasm2wat`, `wasm-decompile`) | 23 |
| [binwalk](https://github.com/ReFirmLabs/binwalk) | Firmware extraction | S3 |
| [Kaitai Struct](https://kaitai.io), [Wireshark](https://www.wireshark.org) | Format specs, protocol analysis | S5 |
| [Tigress](https://tigress.wtf) | Source-level obfuscator for research benchmarks | S1.7 |
| [D-810](https://gitlab.com/eshard/d810) | MBA and control-flow-flattening deobfuscation plugin (for IDA) | S1.3 |
| [INetSim](https://www.inetsim.org), [FakeNet-NG](https://github.com/mandiant/flare-fakenet-ng) | Simulated network services for malware VMs | S2 |

## Practice and courses
| Platform | Notes |
| :--- | :--- |
| [crackmes.one](https://crackmes.one) | Community crackmes, built to be reversed |
| [challenges.re](https://challenges.re) | Short RE exercises by the author of *RE for Beginners* |
| [picoCTF](https://picoctf.org) | Beginner-friendly CTF with a reversing category |
| [pwn.college](https://pwn.college) | Structured practice in systems security and RE |
| [Flare-On](https://flare-on.com) | Annual reverse engineering challenge |
| [Microcorruption](https://microcorruption.com) | Embedded RE and exploitation in the browser |
| [CTFtime](https://ctftime.org) | Calendar and write-ups for CTF events |
| [OpenSecurityTraining2](https://ost2.fyi) | Free courses on architecture, debuggers, and RE |

## Legal and disclosure (orientation, not legal advice)
| Resource | Module |
| :--- | :--- |
| [US Copyright Office, Section 1201 rulemaking](https://www.copyright.gov/1201/) | 28 |
| [EU Directive 2009/24/EC on the legal protection of computer programs](https://eur-lex.europa.eu/eli/dir/2009/24/oj) (returned HTTP 202, served after a bot check) | 28 |
| [EFF, Coders' Rights: Reverse Engineering FAQ](https://www.eff.org/issues/coders/reverse-engineering-faq) | 28 |
| [ISO/IEC 29147, vulnerability disclosure](https://www.iso.org/standard/72311.html) | 28 |
| [CERT Guide to Coordinated Vulnerability Disclosure](https://certcc.github.io/CERT-Guide-to-CVD/) | 28 |
