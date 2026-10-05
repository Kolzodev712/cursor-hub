# Platform knowledge (conditional)

Platform facts describe **specific** compilers, CPUs, OS tools, or library implementations. They apply only when project `.cursor/doctrine/workload.md` (or toolchain pins) make that platform relevant.

- Do **not** promote AMD/Intel/LLVM facts into generic decision domains.
- Prefer **SOURCES.md** registry + authoritative docs at research time over copying manuals into the hub.
- Detailed platform files are added **sparingly** after source audit and reuse justification.

Generic decision routing lives under [decision/](../decision/).
