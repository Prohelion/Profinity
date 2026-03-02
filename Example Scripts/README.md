# Example Scripts

This directory contains example scripts for C# and Python that run inside the Profinity scripting engine. Each language subdirectory includes two kinds of examples:

- **Detailed script examples** — Match the templates shipped with the Profinity engine. They include extensive commented examples for CAN packet handling, DBC signals, script state, global state, cancellation, and related patterns. Use these when you want a single reference file with many patterns in one place.
- **Simple examples** — Minimal, focused scripts for one concept each: stdout/stderr, send CAN, read CAN, read DBC signal, script state, global state (set/get), cancellation, run fail, run exit, errors. Use these for quick tests or when you only need one behaviour. These align with the script patterns used in Profinity tests.

## Subdirectories

---

**[CSharp/](CSharp/README.md)**

C# examples: detailed (Receive, Run, Service) and simple (StdOut, StdError, Send CAN, RunFail, MinimalService, FormatError, ExecutionError, Cancel). Each script is described in the subdirectory's README.

---

**[Python/](Python/README.md)**

Python examples: detailed (Receive, Run, Service) and simple (StdOut, StdError, Send CAN, RunFail, MinimalService, FormatError, ExecutionError, Cancel). Each script is described in the subdirectory's README.

---

For more details on each script, refer to the README.md file within each language-specific subdirectory.
