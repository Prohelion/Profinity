# CSharp Example Scripts

This directory contains example C# scripts demonstrating various features and error cases for the Profinity scripting environment. Each script is described below:

---

**[CSharpStdOutExample.cs](CSharpStdOutExample.cs)**

Demonstrates how to write a message to standard output (STDOUT) using the Profinity scripting API. Useful for testing output capture and logging.

---

**[CSharpStdErrorExample.cs](CSharpStdErrorExample.cs)**

Shows how to write a message to standard error (STDERR) using the Profinity scripting API. This is helpful for testing error output handling.

---

**[CSharpServiceExample.cs](CSharpServiceExample.cs)**

Implements a full-featured Profinity service with start, stop, pause, and continue lifecycle methods. Each method logs its action to the console, making it a good template for service-based scripts.

---

**[CSharpSendCANMessage.cs](CSharpSendCANMessage.cs)**

Demonstrates sending a CAN bus message using the Profinity CANBus API. It creates a CAN packet, sets some data fields, and sends it, serving as a reference for CAN communication.

---

**[CSharpRunExample.cs](CSharpRunExample.cs)**

A simple runnable script that prints a message and the current Profinity message to the console. Useful for basic script execution and message passing tests.

---

**[CSharpRunFailExample.cs](CSharpRunFailExample.cs)**

Illustrates a script that intentionally returns `false` from its `Run` method, simulating a failure scenario. It prints a message before failing.

---

**[CSharpReceiveExample.cs](CSharpReceiveExample.cs)**

Shows how to implement a receiver script that reacts to incoming CAN packets. It prints the received CAN ID in hexadecimal format to the console.

---

**[CSharpMinimalServiceExample.cs](CSharpMinimalServiceExample.cs)**

A minimal example of a Profinity service, implementing only the `OnStart` method. It prints a message when started, serving as a lightweight service template.

---

**[CSharpFormatErrorExample.cs](CSharpFormatErrorExample.cs)**

Contains a deliberate syntax error ("classy" instead of "class") to demonstrate how the system handles format or compilation errors in scripts.

---

**[CSharpExecutionErrorExample.cs](CSharpExecutionErrorExample.cs)**

Throws an exception during execution to simulate a runtime error. Useful for testing error handling and reporting in the scripting environment.

---

**[CSharpCancelExample.cs](CSharpCancelExample.cs)**

Demonstrates how to handle script cancellation. The script enters a loop, periodically checking if it has been cancelled, and prints its state until cancellation occurs.
