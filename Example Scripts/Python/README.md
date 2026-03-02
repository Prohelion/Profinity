# Python Example Scripts

This directory contains example Python scripts for the Profinity scripting environment, in two groups: **detailed** (template-style, with many commented examples) and **simple** (minimal, one concept per script).

---

## Detailed script examples

These match the templates shipped with the Profinity engine and include extensive commented examples for CAN, DBC, state, and related patterns.

**[PythonReceiveExample.py](PythonReceiveExample.py)**

Receiver script that reacts to incoming CAN packets. Includes commented examples for reading packet data, sending responses, DBC signals, script state, global state, and filtering by packet content.

**[PythonRunExample.py](PythonRunExample.py)**

Runnable script (run on demand or scheduled). Includes commented examples for reading CAN packets, sending CAN, DBC signals, state, global state, and script cancellation in loops.

**[PythonServiceExample.py](PythonServiceExample.py)**

Service script with `on_start`, `on_stop`, `on_pause`, and `on_continue`. Includes a working `run()` example (log every second) and a commented alternative `run()` with an internal loop and cancellation checks.

---

## Simple examples

Minimal scripts, each focused on a single behaviour or scenario.

**[PythonStdOutExample.py](PythonStdOutExample.py)**

Writes a message to the script console using `print`. For testing output capture and logging.

**[PythonStdErrorExample.py](PythonStdErrorExample.py)**

Writes a message to standard error (STDERR). For testing error output handling.

**[PythonSendCANMessage.py](PythonSendCANMessage.py)**

Creates a CAN packet, sets data fields, and sends it. Minimal reference for sending CAN messages.

**[PythonReadCANMessageExample.py](PythonReadCANMessageExample.py)**

Gets the latest received CAN packet for a given ID via `LatestValidPacketReceivedByID`, then prints ID and data.

**[PythonReadDBCSignalExample.py](PythonReadDBCSignalExample.py)**

Reads a DBC signal via `Profinity.DBC.GetDbcSignal`. Uses TestDBCComponent / STW_ANGLHP_STAT / StW_AnglHP (same as Profinity test scripts). For a self-contained run with data, run CSharpReadDBCSignalExample first to inject CAN. Matches Profinity test script PythonDBCTest.

**[PythonStateExample.py](PythonStateExample.py)**

Sets and gets both local script state (`Profinity.State`) and global state (`Profinity.GlobalState`). Matches Profinity test script PythonStateTest.

**[PythonGlobalStateSetExample.py](PythonGlobalStateSetExample.py)**

Sets a value in GlobalState for another script to read. Run with PythonGlobalStateGetExample (or C# equivalent) to test inter-script sharing. Matches Profinity test script PythonInterscriptSetTest.

**[PythonGlobalStateGetExample.py](PythonGlobalStateGetExample.py)**

Reads a value from GlobalState set by another script. Run PythonGlobalStateSetExample first (or C# equivalent). Matches Profinity test script PythonInterscriptGetTest.

**[PythonRunExitExample.py](PythonRunExitExample.py)**

Runnable script that prints a message then exits with `sys.exit(0)`. For testing exit-code handling. Matches Profinity test script PythonRunExitTest.

**[PythonRunFailExample.py](PythonRunFailExample.py)**

Intentionally exits with a non-zero status to simulate a failure. For testing failure handling.

**[PythonMinimalServiceExample.py](PythonMinimalServiceExample.py)**

Minimal service with only `on_start` implemented. Lightweight starting point for service scripts.

**[PythonFormatErrorExample.py](PythonFormatErrorExample.py)**

Contains a deliberate syntax error to show how the engine reports format/compilation errors.

**[PythonExecutionErrorExample.py](PythonExecutionErrorExample.py)**

Throws an exception during execution. For testing runtime error handling and reporting.

**[PythonCancelExample.py](PythonCancelExample.py)**

Loop that checks `Profinity.ScriptCancelled` and prints state until cancellation. For testing cancellation behaviour. 