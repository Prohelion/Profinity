# Profinity Script - Python Run Template
#
# This script will execute the code in the run method each time it is called, either as
# part of a scheduled event of just run manually.
#
# For further information on the capabilites of Profinity Scripting, see the example scripts.
#

def RunMe():
    print('This is a Python message!')
    print(Profinity.Message)

    # ============================================================================
    # EXAMPLE CODE - These examples show how to use major Profinity features
    # ============================================================================
    # The code below demonstrates various capabilities but is commented out so it
    # doesn't affect the script's current functionality. Uncomment and modify as needed.
    # ============================================================================

    # ----------------------------------------------------------------------------
    # EXAMPLE 1: Read CAN Packet (Latest received packet for a specific CAN ID)
    # ----------------------------------------------------------------------------
    # Get the latest valid CAN packet received for a specific CAN ID
    # Replace 0x100 with your actual CAN ID (can be hex like 0x100 or decimal like 256)
    # can_id = 0x100
    # received_packet = Profinity.CANBus.LatestValidPacketReceivedByID(can_id)
    # if received_packet is not None:
    #     # Read major CAN packet properties
    #     print(f'CAN ID: {received_packet.CanId} (Hex: {received_packet.CanIdAsHex})')
    #     print(f'Data length: {received_packet.DataLength} bytes')
    #     print(f'Extended frame: {received_packet.Extended}')
    #     print(f'CAN FD: {received_packet.CanFD}')
    #     print(f'Remote frame (RTR): {received_packet.Rtr}')
    #     print(f'Heartbeat: {received_packet.Heartbeat}')
    #     print(f'Settings packet: {received_packet.Settings}')
    #     print(f'Data encoding: {received_packet.DataEncoding}')
    #     print(f'Age: {received_packet.MillisecondsSinceCreated} ms')
    #
    #     # Read packet data in various formats
    #     # Access raw byte array
    #     raw_data = received_packet.Data
    #     if raw_data is not None and len(raw_data) > 0:
    #         print(f'Raw data (bytes): {" ".join(f"{b:02X}" for b in raw_data)}')
    #
    #     # Access data as 32-bit signed integers (most common)
    #     if received_packet.Int32Pos0 is not None:
    #         print(f'Int32 at position 0: {received_packet.Int32Pos0}')
    #     if received_packet.Int32Pos1 is not None:
    #         print(f'Int32 at position 1: {received_packet.Int32Pos1}')
    #
    #     # Access data as floats (for floating-point values)
    #     if received_packet.FloatPos0 is not None:
    #         print(f'Float at position 0: {received_packet.FloatPos0}')
    #
    #     # Access individual bytes
    #     if received_packet.BytePos0 is not None:
    #         print(f'Byte at position 0: {received_packet.BytePos0} (0x{received_packet.BytePos0:02X})')
    #     if received_packet.BytePos1 is not None:
    #         print(f'Byte at position 1: {received_packet.BytePos1} (0x{received_packet.BytePos1:02X})')
    #
    #     # Access as 16-bit signed integers
    #     if received_packet.Short16Pos0 is not None:
    #         print(f'Int16 at position 0: {received_packet.Short16Pos0}')
    #
    #     # Access as unsigned integers
    #     if received_packet.UInt32Pos0 is not None:
    #         print(f'UInt32 at position 0: {received_packet.UInt32Pos0}')
    # else:
    #     print(f'No valid CAN packet found for ID {hex(can_id)}')
    #
    # # Alternative: Wait for a CAN packet with timeout (blocks until packet arrives or timeout)
    # # packet = Profinity.CANBus.Receive(can_id, timeout=1000)  # 1 second timeout
    #

    # ----------------------------------------------------------------------------
    # EXAMPLE 2: Write and Read CAN Packets (Complete read/write example)
    # ----------------------------------------------------------------------------
    # This example demonstrates both reading existing packets and creating/sending new ones
    #
    # # Part A: Read an existing CAN packet
    # from Profinity.Comms.CANBus import CanPacket
    #
    # read_can_id = 0x100
    # existing_packet = Profinity.CANBus.LatestValidPacketReceivedByID(read_can_id)
    # if existing_packet is not None:
    #     print(f'Read packet - ID: {existing_packet.CanIdAsHex}, Data: {" ".join(f"{b:02X}" for b in existing_packet.Data)}')
    #     # Read and display packet properties
    #     print(f'  Extended: {existing_packet.Extended}, Length: {existing_packet.DataLength}')
    #     if existing_packet.Int32Pos0 is not None:
    #         print(f'  Int32[0]: {existing_packet.Int32Pos0}')
    #
    # # Part B: Create and send a new CAN packet
    # # Method 1: Create with CAN ID only, then set data using typed properties
    # packet_to_send = CanPacket(0x200)
    # packet_to_send.Int32Pos0 = 100  # Set first 4 bytes as signed 32-bit integer
    # packet_to_send.Int32Pos1 = 200  # Set next 4 bytes as signed 32-bit integer
    # Profinity.CANBus.SendMessage(packet_to_send)
    # print(f'Sent packet ID {packet_to_send.CanIdAsHex} with Int32 values: {packet_to_send.Int32Pos0}, {packet_to_send.Int32Pos1}')
    #
    # # Method 2: Create packet with float values
    # float_packet = CanPacket(0x300)
    # float_packet.FloatPos0 = 3.14159  # Set first 4 bytes as float
    # float_packet.FloatPos1 = 2.71828  # Set next 4 bytes as float
    # Profinity.CANBus.SendMessage(float_packet)
    #
    # # Method 3: Create packet with individual bytes
    # byte_packet = CanPacket(0x400)
    # byte_packet.BytePos0 = 0x01
    # byte_packet.BytePos1 = 0x02
    # byte_packet.BytePos2 = 0x03
    # byte_packet.BytePos3 = 0x04
    # byte_packet.BytePos4 = 0x05
    # byte_packet.BytePos5 = 0x06
    # byte_packet.BytePos6 = 0x07
    # byte_packet.BytePos7 = 0x08
    # Profinity.CANBus.SendMessage(byte_packet)
    #
    # # Method 4: Create with byte array (full control)
    # can_data = [0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0x00, 0x11]
    # detailed_packet = CanPacket(0x500, False, False, False, 8, CanPacket.Encoding.LittleEndian, can_data)
    # sent = Profinity.CANBus.SendMessage(detailed_packet)
    # if sent:
    #     print(f'CAN packet {detailed_packet.CanIdAsHex} sent successfully')
    #     print(f'  Raw data: {" ".join(f"{b:02X}" for b in detailed_packet.Data)}')
    #     print(f'  Data length: {detailed_packet.DataLength} bytes')
    #
    # # Method 5: Create extended frame (29-bit CAN ID)
    # extended_packet = CanPacket(
    #     0x1FFFFFFF,  # Extended ID (29 bits)
    #     True,        # extendedFrameFormat
    #     False,       # remoteFrame
    #     False,       # errorFrame
    #     8,           # dataLength
    #     CanPacket.Encoding.LittleEndian,
    #     [0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88]
    # )
    # Profinity.CANBus.SendMessage(extended_packet)
    # print(f'Extended frame {extended_packet.CanIdAsHex} sent (Extended: {extended_packet.Extended})')
    #

    # ----------------------------------------------------------------------------
    # EXAMPLE 3: Read DBC Message and Signal
    # ----------------------------------------------------------------------------
    # Access DBC signals through component name, message name, and signal name
    # Replace these with your actual component, message, and signal names
    # component_name = "YourComponentName"  # e.g., "BatteryPack"
    # message_name = "YourMessageName"      # e.g., "STW_ANGLHP_STAT"
    # signal_name = "YourSignalName"        # e.g., "StW_AnglHP"
    #
    # try:
    #     # Get the DBC signal and read its value
    #     signal = Profinity.DBC.GetDbcSignal(component_name, message_name, signal_name)
    #     signal_value = signal.Value
    #     print(f'DBC Signal {component_name}.{message_name}.{signal_name} = {signal_value}')
    #
    #     # You can also access signal properties like:
    #     # - signal.Minimum
    #     # - signal.Maximum
    #     # - signal.Unit
    #     # - signal.Comment
    # except Exception as ex:
    #     print(f'Error reading DBC signal: {ex.Message}')
    #     # Common errors: Component not found, Message not found, Signal not found
    #

    # ----------------------------------------------------------------------------
    # EXAMPLE 4: Store State (Local to this script instance)
    # ----------------------------------------------------------------------------
    # Store values that persist between script runs within this script instance
    # Useful for maintaining counters, flags, or temporary data
    #
    # # Store different data types
    # Profinity.State.Set("counter", 42)
    # Profinity.State.Set("lastMessage", "Script executed successfully")
    # from datetime import datetime
    # Profinity.State.Set("lastRunTime", datetime.now().isoformat())
    #
    # # Retrieve stored values (returns None if key doesn't exist)
    # counter_obj = Profinity.State.Get("counter")
    # if counter_obj is not None:
    #     counter = int(counter_obj)
    #     counter += 1  # Increment counter
    #     Profinity.State.Set("counter", counter)
    #     print(f'Run count: {counter}')
    #
    # last_msg = Profinity.State.Get("lastMessage")
    # if last_msg is not None:
    #     print(f'Last message: {last_msg}')
    #

    # ----------------------------------------------------------------------------
    # EXAMPLE 5: Share State (Global across all scripts)
    # ----------------------------------------------------------------------------
    # Store values that can be accessed by all scripts in the profile
    # Useful for inter-script communication and shared data
    #
    # # Set global values
    # Profinity.GlobalState.Set("sharedCounter", 100)
    # Profinity.GlobalState.Set("systemStatus", "Running")
    # from datetime import datetime
    # Profinity.GlobalState.Set("lastUpdateTime", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #
    # # Read global values set by other scripts
    # shared_counter = Profinity.GlobalState.Get("sharedCounter")
    # if shared_counter is not None:
    #     count = int(shared_counter)
    #     print(f'Shared counter value: {count}')
    #
    # status = Profinity.GlobalState.Get("systemStatus")
    # if status is not None:
    #     print(f'System status from other script: {status}')
    #
    # # Increment shared counter (example of coordination between scripts)
    # if shared_counter is not None:
    #     current_count = int(shared_counter)
    #     Profinity.GlobalState.Set("sharedCounter", current_count + 1)
    #

    # ----------------------------------------------------------------------------
    # EXAMPLE 6: Check for Script Cancellation (Important for long-running operations)
    # ----------------------------------------------------------------------------
    # Always check Profinity.ScriptCancelled in loops to allow graceful cancellation
    # This allows the script to be stopped gracefully when needed
    #
    # iteration_count = 0
    # while iteration_count < 100 and not Profinity.ScriptCancelled:
    #     # Do some work here
    #     print(f'Iteration {iteration_count}')
    #
    #     # Check cancellation periodically in long operations
    #     if Profinity.ScriptCancelled:
    #         print('Script was cancelled, exiting loop')
    #         break
    #
    #     iteration_count += 1
    #     import time
    #     time.sleep(0.1)  # Small delay to avoid tight loop
    #
    # # Check cancellation before long operations
    # if not Profinity.ScriptCancelled:
    #     # Perform time-consuming operation
    #     pass
    # else:
    #     print('Script was cancelled, skipping operation')
    #     return False  # Indicate script was cancelled
    #


RunMe()
