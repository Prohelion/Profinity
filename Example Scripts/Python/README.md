# Python Example Scripts

This directory contains example Python scripts demonstrating various features and error cases for the Profinity scripting environment. Each script is described below:

---

**[PythonStdOutExample.py](PythonStdOutExample.py)**

Demonstrates how to write a message to standard output (STDOUT) using the `print` function. Useful for testing output capture and logging.

---

**[PythonStdErrorExample.py](PythonStdErrorExample.py)**

Shows how to write a message to standard error (STDERR) using a custom function that prints to `sys.stderr`. This is helpful for testing error output handling.

---

**[PythonServiceExample.py](PythonServiceExample.py)**

Implements a full-featured Profinity service with start, stop, pause, continue, and shutdown lifecycle methods. Each method logs its action to the console, making it a good template for service-based scripts.

---

**[PythonSendCANMessage.py](PythonSendCANMessage.py)**

Demonstrates sending a CAN bus message using the Profinity CANBus API. It creates a CAN packet, sets some data fields, and sends it, serving as a reference for CAN communication.

---

**[PythonRunExample.py](PythonRunExample.py)**

A simple runnable script that prints a message and the current Profinity message to the console. Useful for basic script execution and message passing tests.

---

**[PythonRunFailExample.py](PythonRunFailExample.py)**

Illustrates a script that intentionally exits with a non-zero status to simulate a failure scenario. It prints a message before failing.

---

**[PythonReceiveExample.py](PythonReceiveExample.py)**

Shows how to implement a receiver script that reacts to incoming CAN packets. It prints the received CAN ID in hexadecimal format to the console.

---

**[PythonMinimalServiceExample.py](PythonMinimalServiceExample.py)**

A minimal example of a Profinity service, implementing only the `on_start` method. It prints a message when started, serving as a lightweight service template.

---

**[PythonFormatErrorExample.py](PythonFormatErrorExample.py)**

Contains a deliberate syntax error (invalid function definition) to demonstrate how the system handles format or compilation errors in scripts.

---

**[PythonExecutionErrorExample.py](PythonExecutionErrorExample.py)**

Throws an exception during execution to simulate a runtime error. Useful for testing error handling and reporting in the scripting environment.

---

**[PythonCancelExample.py](PythonCancelExample.py)**

Demonstrates how to handle script cancellation. The script enters a loop, periodically checking if it has been cancelled, and prints its state until cancellation occurs. 