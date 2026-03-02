/* Profinity Script - CSharp Receive Template
*
* This script will receive a CAN Packet in the CAN Id range defined for the component.
*
* IMPORTANT: A receiver is called each time a CAN Bus message in the configured range is received.
* In busy systems this can be 100's of calls a second, to ensure that all CAN packets are processed
* by all receivers at the same time, this process is handled synchronously.  It is important that your
* CAN receiver does not block or pause the main loop as this will impact other components and backlog
* your CAN processing.  We suggest if your script cannot run fast that you put the received CAN messages
* in to a queue and handle them in a background thread.  See the examples for samples of this.
*
* For more example scripts, search for "Profinity Example Scripts" in your favourite web search engine or check the
* Profinity doumentation on the Prohelion website at https://docs.prohelion.com for links to our examples.
*/

using System;
using Profinity.Scripting;
using Profinity.Comms.CANBus;
using Profinity.Model.DBC;

public class CSharpReceiveExample : ProfinityScript, IProfinityReceiverScript
{
    public void Receive(CanPacket canPacket)
    {
        Profinity.Console.WriteLine("CSharp CanId Received : " + canPacket.CanIdAsHex);

        // ============================================================================
        // EXAMPLE CODE - These examples show how to use major Profinity features
        // ============================================================================
        // The code below demonstrates various capabilities but is commented out so it
        // doesn't affect the script's current functionality. Uncomment and modify as needed.
        // ============================================================================

        /*
        // ----------------------------------------------------------------------------
        // EXAMPLE 1: Access Received CAN Packet Data
        // ----------------------------------------------------------------------------
        // The canPacket parameter contains the received CAN packet - no need to read it
        // Access major CAN packet properties
        Profinity.Console.WriteLine($"CAN ID: {canPacket.CanId} (Hex: {canPacket.CanIdAsHex})");
        Profinity.Console.WriteLine($"Data length: {canPacket.DataLength} bytes");
        Profinity.Console.WriteLine($"Extended frame: {canPacket.Extended}");
        Profinity.Console.WriteLine($"CAN FD: {canPacket.CanFD}");
        Profinity.Console.WriteLine($"Remote frame (RTR): {canPacket.Rtr}");
        Profinity.Console.WriteLine($"Heartbeat: {canPacket.Heartbeat}");
        Profinity.Console.WriteLine($"Settings packet: {canPacket.Settings}");
        Profinity.Console.WriteLine($"Data encoding: {canPacket.DataEncoding}");
        Profinity.Console.WriteLine($"Age: {canPacket.MillisecondsSinceCreated} ms");

        // Read packet data in various formats
        // Access raw byte array
        byte[] rawData = canPacket.Data;
        if (rawData != null && rawData.Length > 0)
        {
            Profinity.Console.WriteLine($"Raw data (bytes): {BitConverter.ToString(rawData)}");
        }

        // Access data as 32-bit signed integers (most common)
        if (canPacket.Int32Pos0.HasValue)
        {
            Profinity.Console.WriteLine($"Int32 at position 0: {canPacket.Int32Pos0.Value}");
        }
        if (canPacket.Int32Pos1.HasValue)
        {
            Profinity.Console.WriteLine($"Int32 at position 1: {canPacket.Int32Pos1.Value}");
        }

        // Access data as floats (for floating-point values)
        if (canPacket.FloatPos0.HasValue)
        {
            Profinity.Console.WriteLine($"Float at position 0: {canPacket.FloatPos0.Value}");
        }

        // Access individual bytes
        if (canPacket.BytePos0.HasValue)
        {
            Profinity.Console.WriteLine($"Byte at position 0: {canPacket.BytePos0.Value} (0x{canPacket.BytePos0.Value:X2})");
        }
        if (canPacket.BytePos1.HasValue)
        {
            Profinity.Console.WriteLine($"Byte at position 1: {canPacket.BytePos1.Value} (0x{canPacket.BytePos1.Value:X2})");
        }

        // Access as 16-bit signed integers
        if (canPacket.Short16Pos0.HasValue)
        {
            Profinity.Console.WriteLine($"Int16 at position 0: {canPacket.Short16Pos0.Value}");
        }

        // Access as unsigned integers
        if (canPacket.UInt32Pos0.HasValue)
        {
            Profinity.Console.WriteLine($"UInt32 at position 0: {canPacket.UInt32Pos0.Value}");
        }
        */

        /*
        // ----------------------------------------------------------------------------
        // EXAMPLE 2: Send CAN Packets in Response
        // ----------------------------------------------------------------------------
        // Create and send CAN packets based on received data
        // This is useful for protocol implementation, forwarding, or command responses

        // Method 1: Create with CAN ID only, then set data using typed properties
        CanPacket responsePacket = new CanPacket(0x200)
        {
            Int32Pos0 = 100,    // Set first 4 bytes as signed 32-bit integer
            Int32Pos1 = 200     // Set next 4 bytes as signed 32-bit integer
        };
        Profinity.CANBus.SendMessage(responsePacket);
        Profinity.Console.WriteLine($"Sent response packet ID {responsePacket.CanIdAsHex} with Int32 values: {responsePacket.Int32Pos0}, {responsePacket.Int32Pos1}");

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
        // Store values that persist between packet receptions within this script instance
        // Useful for maintaining counters, flags, or temporary data

        // Store different data types
        Profinity.State.Set("packetCount", 42);
        Profinity.State.Set("lastCanId", canPacket.CanIdAsHex);
        Profinity.State.Set("lastReceiveTime", DateTime.Now);

        // Retrieve stored values (returns null if key doesn't exist)
        object packetCountObj = Profinity.State.Get("packetCount");
        if (packetCountObj != null && packetCountObj is int packetCount)
        {
            packetCount++; // Increment counter
            Profinity.State.Set("packetCount", packetCount);
            Profinity.Console.WriteLine($"Packet count: {packetCount}");
        }

        object lastCanId = Profinity.State.Get("lastCanId");
        if (lastCanId != null)
        {
            Profinity.Console.WriteLine($"Last CAN ID: {lastCanId}");
        }
        */

        /*
        // ----------------------------------------------------------------------------
        // EXAMPLE 5: Share State (Global across all scripts)
        // ----------------------------------------------------------------------------
        // Store values that can be accessed by all scripts in the profile
        // Useful for inter-script communication and shared data

        // Set global values
        Profinity.GlobalState.Set("lastReceivedCanId", canPacket.CanIdAsHex);
        Profinity.GlobalState.Set("systemStatus", "Receiving");
        Profinity.GlobalState.Set("lastUpdateTime", DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"));

        // Read global values set by other scripts
        object lastCanId = Profinity.GlobalState.Get("lastReceivedCanId");
        if (lastCanId != null)
        {
            Profinity.Console.WriteLine($"Last CAN ID from other script: {lastCanId}");
        }

        object status = Profinity.GlobalState.Get("systemStatus");
        if (status != null)
        {
            Profinity.Console.WriteLine($"System status from other script: {status}");
        }

        // Increment shared counter (example of coordination between scripts)
        object sharedCounter = Profinity.GlobalState.Get("sharedCounter");
        if (sharedCounter != null && sharedCounter is int currentCount)
        {
            Profinity.GlobalState.Set("sharedCounter", currentCount + 1);
        }
        */

        /*
        // ----------------------------------------------------------------------------
        // EXAMPLE 6: Filter and Process Based on Packet Content
        // ----------------------------------------------------------------------------
        // Process packets conditionally based on CAN ID, data values, or other properties

        // Filter by specific CAN ID
        if (canPacket.CanId == 0x100)
        {
            Profinity.Console.WriteLine("Received packet with ID 0x100");
            // Process specific message type
        }

        // Filter by data value
        if (canPacket.Int32Pos0.HasValue && canPacket.Int32Pos0.Value > 1000)
        {
            Profinity.Console.WriteLine($"Received packet with Int32Pos0 > 1000: {canPacket.Int32Pos0.Value}");
            // Process high-value packets
        }

        // Filter by extended frame
        if (canPacket.Extended)
        {
            Profinity.Console.WriteLine("Received extended frame");
            // Process extended frames differently
        }

        // Filter by data length
        if (canPacket.DataLength == 8)
        {
            Profinity.Console.WriteLine("Received full 8-byte packet");
            // Process full packets
        }
        */
    }
}
