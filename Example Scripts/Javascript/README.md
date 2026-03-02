# Javascript Example Scripts

This directory contains example Javascript scripts demonstrating various features and error cases for the Profinity scripting environment. Each script is described below:

---

**[JavascriptStdOutExample.js](JavascriptStdOutExample.js)**

Demonstrates how to write a message to standard output (STDOUT) using the `log` function. Useful for testing output capture and logging.

---

**[JavascriptStdErrorExample.js](JavascriptStdErrorExample.js)**

Shows how to write a message to standard error (STDERR) using the `error` function. This is helpful for testing error output handling.

---

**[JavascriptServiceExample.js](JavascriptServiceExample.js)**

Implements a full-featured Profinity service with start, stop, pause, continue, and shutdown lifecycle methods. Each method logs its action to the console, making it a good template for service-based scripts.

---

**[JavascriptSendCANMessage.js](JavascriptSendCANMessage.js)**

Demonstrates sending a CAN bus message using the Profinity CANBus API. It creates a CAN packet, sets some data fields, and sends it, serving as a reference for CAN communication.

---

**[JavascriptRunExample.js](JavascriptRunExample.js)**

A simple runnable script that prints a message and the current Profinity message to the console. Useful for basic script execution and message passing tests.

---

**[JavascriptRunFailExample.js](JavascriptRunFailExample.js)**

Illustrates a script that intentionally throws an error to simulate a failure scenario. It prints a message before failing.

---

**[JavascriptReceiveExample.js](JavascriptReceiveExample.js)**

Shows how to implement a receiver script that reacts to incoming CAN packets. It prints the received CAN ID in hexadecimal format to the console.

---

**[JavascriptMinimalServiceExample.js](JavascriptMinimalServiceExample.js)**

A minimal example of a Profinity service, implementing only the `onStart` method. It prints a message when started, serving as a lightweight service template.

---

**[JavascriptFormatErrorExample.js](JavascriptFormatErrorExample.js)**

Contains a deliberate syntax error (invalid function declaration) to demonstrate how the system handles format or compilation errors in scripts.

---

**[JavascriptExecutionErrorExample.js](JavascriptExecutionErrorExample.js)**

Throws an exception during execution to simulate a runtime error. Useful for testing error handling and reporting in the scripting environment.

---

**[JavascriptCancelExample.js](JavascriptCancelExample.js)**

Demonstrates how to handle script cancellation. The script enters a loop, periodically checking if it has been cancelled, and prints its state until cancellation occurs. 