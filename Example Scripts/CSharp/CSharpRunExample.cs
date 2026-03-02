/* Profinity Script - CSharp Run Template
*
* This script will execute the code in the run method each time it is called, either as
* part of a scheduled event of just run manually.
*
* For further information on the capabilites of Profinity Scripting, see the example scripts.
*
* Code in the constructor will not be executed when the script is first loaded, so if you want
* to establish anything required by the script, you need to do so in the run method, likewise
* anything that needs to be closed should be done so in the run method as well.
*/

using System;
using Profinity.Scripting;
using Profinity.Comms.CANBus;
using Profinity.Model.DBC;

public class CSharpRunExample : ProfinityScript, IProfinityRunnableScript
{
    public bool Run()
    {
        Profinity.Console.WriteLine("This is a CSharp Message!");
        Profinity.Console.WriteLine(Profinity.Message);

        // ============================================================================
        // EXAMPLE CODE - These examples show how to use major Profinity features
        // ============================================================================
        // The code below demonstrates various capabilities but is commented out so it
        // doesn't affect the script's current functionality. Uncomment and modify as needed.
        // ============================================================================

        /*
        // ----------------------------------------------------------------------------
        // EXAMPLE 1: Read CAN Packet (Latest received packet for a specific CAN ID)
        // ----------------------------------------------------------------------------
        // Get the latest valid CAN packet received for a specific CAN ID
        // Replace 0x100 with your actual CAN ID (can be hex like 0x100 or decimal like 256)
        uint canId = 0x100;
        CanPacket receivedPacket = Profinity.CANBus.LatestValidPacketReceivedByID(canId);
        if (receivedPacket != null)
        {
            // Read major CAN packet properties
            Profinity.Console.WriteLine($"CAN ID: {receivedPacket.CanId} (Hex: {receivedPacket.CanIdAsHex})");
            Profinity.Console.WriteLine($"Data length: {receivedPacket.DataLength} bytes");
            Profinity.Console.WriteLine($"Extended frame: {receivedPacket.Extended}");
            Profinity.Console.WriteLine($"CAN FD: {receivedPacket.CanFD}");
            Profinity.Console.WriteLine($"Remote frame (RTR): {receivedPacket.Rtr}");
            Profinity.Console.WriteLine($"Heartbeat: {receivedPacket.Heartbeat}");
            Profinity.Console.WriteLine($"Settings packet: {receivedPacket.Settings}");
            Profinity.Console.WriteLine($"Data encoding: {receivedPacket.DataEncoding}");
            Profinity.Console.WriteLine($"Age: {receivedPacket.MillisecondsSinceCreated} ms");

            // Read packet data in various formats
            // Access raw byte array
            byte[] rawData = receivedPacket.Data;
            if (rawData != null && rawData.Length > 0)
            {
                Profinity.Console.WriteLine($"Raw data (bytes): {BitConverter.ToString(rawData)}");
            }

            // Access data as 32-bit signed integers (most common)
            if (receivedPacket.Int32Pos0.HasValue)
            {
                Profinity.Console.WriteLine($"Int32 at position 0: {receivedPacket.Int32Pos0.Value}");
            }
            if (receivedPacket.Int32Pos1.HasValue)
            {
                Profinity.Console.WriteLine($"Int32 at position 1: {receivedPacket.Int32Pos1.Value}");
            }

            // Access data as floats (for floating-point values)
            if (receivedPacket.FloatPos0.HasValue)
            {
                Profinity.Console.WriteLine($"Float at position 0: {receivedPacket.FloatPos0.Value}");
            }

            // Access individual bytes
            if (receivedPacket.BytePos0.HasValue)
            {
                Profinity.Console.WriteLine($"Byte at position 0: {receivedPacket.BytePos0.Value} (0x{receivedPacket.BytePos0.Value:X2})");
            }
            if (receivedPacket.BytePos1.HasValue)
            {
                Profinity.Console.WriteLine($"Byte at position 1: {receivedPacket.BytePos1.Value} (0x{receivedPacket.BytePos1.Value:X2})");
            }

            // Access as 16-bit signed integers
            if (receivedPacket.Short16Pos0.HasValue)
            {
                Profinity.Console.WriteLine($"Int16 at position 0: {receivedPacket.Short16Pos0.Value}");
            }

            // Access as unsigned integers
            if (receivedPacket.UInt32Pos0.HasValue)
            {
                Profinity.Console.WriteLine($"UInt32 at position 0: {receivedPacket.UInt32Pos0.Value}");
            }
        }
        else
        {
            Profinity.Console.WriteLine($"No valid CAN packet found for ID {canId:X}");
        }

        // Alternative: Wait for a CAN packet with timeout (blocks until packet arrives or timeout)
        // CanPacket packet = Profinity.CANBus.Receive(canId, timeout: 1000); // 1 second timeout
        */

        /*
        // ----------------------------------------------------------------------------
        // EXAMPLE 2: Write and Read CAN Packets (Complete read/write example)
        // ----------------------------------------------------------------------------
        // This example demonstrates both reading existing packets and creating/sending new ones
        
        // Part A: Read an existing CAN packet
        uint readCanId = 0x100;
        CanPacket existingPacket = Profinity.CANBus.LatestValidPacketReceivedByID(readCanId);
        if (existingPacket != null)
        {
            Profinity.Console.WriteLine($"Read packet - ID: {existingPacket.CanIdAsHex}, Data: {BitConverter.ToString(existingPacket.Data)}");
            
            // Read and display packet properties
            Profinity.Console.WriteLine($"  Extended: {existingPacket.Extended}, Length: {existingPacket.DataLength}");
            if (existingPacket.Int32Pos0.HasValue)
            {
                Profinity.Console.WriteLine($"  Int32[0]: {existingPacket.Int32Pos0.Value}");
            }
        }

        // Part B: Create and send a new CAN packet
        // Method 1: Create with CAN ID only, then set data using typed properties
        CanPacket packetToSend = new CanPacket(0x200)
        {
            Int32Pos0 = 100,    // Set first 4 bytes as signed 32-bit integer
            Int32Pos1 = 200     // Set next 4 bytes as signed 32-bit integer
        };
        Profinity.CANBus.SendMessage(packetToSend);
        Profinity.Console.WriteLine($"Sent packet ID {packetToSend.CanIdAsHex} with Int32 values: {packetToSend.Int32Pos0}, {packetToSend.Int32Pos1}");

        // Method 2: Create packet with float values
        CanPacket floatPacket = new CanPacket(0x300)
        {
            FloatPos0 = 3.14159f,   // Set first 4 bytes as float
            FloatPos1 = 2.71828f    // Set next 4 bytes as float
        };
        Profinity.CANBus.SendMessage(floatPacket);

        // Method 3: Create packet with individual bytes
        CanPacket bytePacket = new CanPacket(0x400)
        {
            BytePos0 = 0x01,
            BytePos1 = 0x02,
            BytePos2 = 0x03,
            BytePos3 = 0x04,
            BytePos4 = 0x05,
            BytePos5 = 0x06,
            BytePos6 = 0x07,
            BytePos7 = 0x08
        };
        Profinity.CANBus.SendMessage(bytePacket);

        // Method 4: Create with byte array (full control)
        byte[] canData = new byte[8] { 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0x00, 0x11 };
        CanPacket detailedPacket = new CanPacket(
            canId: 0x500,
            extendedFrameFormat: false,
            remoteFrame: false,
            errorFrame: false,
            dataLength: 8,
            encoding: CanPacket.Encoding.LittleEndian,
            data: canData
        );
        bool sent = Profinity.CANBus.SendMessage(detailedPacket);
        if (sent)
        {
            Profinity.Console.WriteLine($"CAN packet {detailedPacket.CanIdAsHex} sent successfully");
            Profinity.Console.WriteLine($"  Raw data: {BitConverter.ToString(detailedPacket.Data)}");
            Profinity.Console.WriteLine($"  Data length: {detailedPacket.DataLength} bytes");
        }

        // Method 5: Create extended frame (29-bit CAN ID)
        CanPacket extendedPacket = new CanPacket(
            canId: 0x1FFFFFFF,  // Extended ID (29 bits)
            extendedFrameFormat: true,
            remoteFrame: false,
            errorFrame: false,
            dataLength: 8,
            encoding: CanPacket.Encoding.LittleEndian,
            data: new byte[8] { 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88 }
        );
        Profinity.CANBus.SendMessage(extendedPacket);
        Profinity.Console.WriteLine($"Extended frame {extendedPacket.CanIdAsHex} sent (Extended: {extendedPacket.Extended})");
        */

        /*
        // ----------------------------------------------------------------------------
        // EXAMPLE 3: Read DBC Message and Signal
        // ----------------------------------------------------------------------------
        // Access DBC signals through component name, message name, and signal name
        // Replace these with your actual component, message, and signal names
        string componentName = "YourComponentName";  // e.g., "BatteryPack"
        string messageName = "YourMessageName";      // e.g., "STW_ANGLHP_STAT"
        string signalName = "YourSignalName";        // e.g., "StW_AnglHP"

        try
        {
            // Get the DBC signal and read its value
            DbcSignal signal = Profinity.DBC.GetDbcSignal(componentName, messageName, signalName);
            double signalValue = signal.Value;
            Profinity.Console.WriteLine($"DBC Signal {componentName}.{messageName}.{signalName} = {signalValue}");

            // You can also access signal properties like:
            // - signal.Minimum
            // - signal.Maximum
            // - signal.Unit
            // - signal.Comment
        }
        catch (Exception ex)
        {
            Profinity.Console.WriteLine($"Error reading DBC signal: {ex.Message}");
            // Common errors: Component not found, Message not found, Signal not found
        }
        */

        /*
        // ----------------------------------------------------------------------------
        // EXAMPLE 4: Store State (Local to this script instance)
        // ----------------------------------------------------------------------------
        // Store values that persist between script runs within this script instance
        // Useful for maintaining counters, flags, or temporary data
        
        // Store different data types
        Profinity.State.Set("counter", 42);
        Profinity.State.Set("lastMessage", "Script executed successfully");
        Profinity.State.Set("lastRunTime", DateTime.Now);

        // Retrieve stored values (returns null if key doesn't exist)
        object counterObj = Profinity.State.Get("counter");
        if (counterObj != null && counterObj is int counter)
        {
            counter++; // Increment counter
            Profinity.State.Set("counter", counter);
            Profinity.Console.WriteLine($"Run count: {counter}");
        }

        object lastMsg = Profinity.State.Get("lastMessage");
        if (lastMsg != null)
        {
            Profinity.Console.WriteLine($"Last message: {lastMsg}");
        }
        */

        /*
        // ----------------------------------------------------------------------------
        // EXAMPLE 5: Share State (Global across all scripts)
        // ----------------------------------------------------------------------------
        // Store values that can be accessed by all scripts in the profile
        // Useful for inter-script communication and shared data
        
        // Set global values
        Profinity.GlobalState.Set("sharedCounter", 100);
        Profinity.GlobalState.Set("systemStatus", "Running");
        Profinity.GlobalState.Set("lastUpdateTime", DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"));

        // Read global values set by other scripts
        object sharedCounter = Profinity.GlobalState.Get("sharedCounter");
        if (sharedCounter != null && sharedCounter is int count)
        {
            Profinity.Console.WriteLine($"Shared counter value: {count}");
        }

        object status = Profinity.GlobalState.Get("systemStatus");
        if (status != null)
        {
            Profinity.Console.WriteLine($"System status from other script: {status}");
        }

        // Increment shared counter (example of coordination between scripts)
        if (sharedCounter != null && sharedCounter is int currentCount)
        {
            Profinity.GlobalState.Set("sharedCounter", currentCount + 1);
        }
        */

        /*
        // ----------------------------------------------------------------------------
        // EXAMPLE 6: Check for Script Cancellation (Important for long-running operations)
        // ----------------------------------------------------------------------------
        // Always check Profinity.ScriptCancelled in loops to allow graceful cancellation
        // This allows the script to be stopped gracefully when needed
        
        int iterationCount = 0;
        while (iterationCount < 100 && !Profinity.ScriptCancelled)
        {
            // Do some work here
            Profinity.Console.WriteLine($"Iteration {iterationCount}");
            
            // Check cancellation periodically in long operations
            if (Profinity.ScriptCancelled)
            {
                Profinity.Console.WriteLine("Script was cancelled, exiting loop");
                break;
            }
            
            iterationCount++;
            System.Threading.Thread.Sleep(100); // Small delay to avoid tight loop
        }
        
        // Check cancellation before long operations
        if (!Profinity.ScriptCancelled)
        {
            // Perform time-consuming operation
            // ...
        }
        else
        {
            Profinity.Console.WriteLine("Script was cancelled, skipping operation");
            return false; // Indicate script was cancelled
        }
        */

        return true;
    }
}
