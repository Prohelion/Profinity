# CSharp Example Scripts

This directory contains example C# scripts for the Profinity scripting environment, in two groups: **detailed** (template-style, with many commented examples) and **simple** (minimal, one concept per script).

---

## Detailed script examples

These match the templates shipped with the Profinity engine and include extensive commented examples for CAN, DBC, state, and related patterns.

**[CSharpReceiveExample.cs](CSharpReceiveExample.cs)**

Receiver script that reacts to incoming CAN packets. Includes commented examples for reading packet data, sending responses, DBC signals, script state, global state, and filtering by packet content.

**[CSharpRunExample.cs](CSharpRunExample.cs)**

Runnable script (run on demand or scheduled). Includes commented examples for reading CAN packets, sending CAN, DBC signals, state, global state, and script cancellation in loops.

**[CSharpServiceExample.cs](CSharpServiceExample.cs)**

Service script with start, stop, pause, and continue lifecycle. Includes a working `Run()` example (log every second) and a commented alternative `Run()` with an internal loop and cancellation checks.

---

## Simple examples

Minimal scripts, each focused on a single behaviour or scenario.

**[CSharpStdOutExample.cs](CSharpStdOutExample.cs)**

Writes a message to the script console (STDOUT) via the Profinity API. For testing output capture and logging.

**[CSharpStdErrorExample.cs](CSharpStdErrorExample.cs)**

Writes a message to standard error (STDERR). For testing error output handling.

**[CSharpSendCANMessage.cs](CSharpSendCANMessage.cs)**

Creates a CAN packet, sets data fields, and sends it. Minimal reference for sending CAN messages.

**[CSharpReadCANMessageExample.cs](CSharpReadCANMessageExample.cs)**

Gets the latest received CAN packet for a given ID via `LatestValidPacketReceivedByID`, then prints ID and data. Matches the pattern used in Profinity tests.

**[CSharpReadDBCSignalExample.cs](CSharpReadDBCSignalExample.cs)**

Injects a CAN packet then reads a DBC signal via `Profinity.DBC.GetDbcSignal`. Uses TestDBCComponent / STW_ANGLHP_STAT / StW_AnglHP (same as Profinity test scripts). Requires a component with that DBC loaded.

**[CSharpStateExample.cs](CSharpStateExample.cs)**

Sets and gets both local script state (`Profinity.State`) and global state (`Profinity.GlobalState`). Matches Profinity test script CSharpStateTest.

**[CSharpGlobalStateSetExample.cs](CSharpGlobalStateSetExample.cs)**

Sets a value in GlobalState for another script to read. Run with CSharpGlobalStateGetExample (or Python equivalent) to test inter-script sharing. Matches Profinity test script CSharpInterscriptSetTest.

**[CSharpGlobalStateGetExample.cs](CSharpGlobalStateGetExample.cs)**

Reads a value from GlobalState set by another script. Run CSharpGlobalStateSetExample first (or Python equivalent). Matches Profinity test script CSharpInterscriptGetTest.

**[CSharpRunFailExample.cs](CSharpRunFailExample.cs)**

Intentionally returns `false` from `Run()` to simulate a failure. For testing failure handling.

**[CSharpMinimalServiceExample.cs](CSharpMinimalServiceExample.cs)**

Minimal service with only `OnStart` implemented. Lightweight starting point for service scripts.

**[CSharpFormatErrorExample.cs](CSharpFormatErrorExample.cs)**

Contains a deliberate syntax error ("classy" instead of "class") to show how the engine reports format/compilation errors.

**[CSharpExecutionErrorExample.cs](CSharpExecutionErrorExample.cs)**

Throws an exception during execution. For testing runtime error handling and reporting.

**[CSharpCancelExample.cs](CSharpCancelExample.cs)**

Loop that checks `Profinity.ScriptCancelled` and prints state until cancellation. For testing cancellation behaviour.
