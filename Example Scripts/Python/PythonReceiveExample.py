# Profinity Script - Python Receive Template
#
# This script will receive a CAN Packet in the CAN Id range defined for the component.
#
# Code outside of the receive function will be executed when the script is first loaded, so if you want
# to establish anything required by the script, do so there.
#
# IMPORTANT: A receiver is called each time a CAN Bus message in the configured range is received.
# In busy systems this can be 100's of calls a second, to ensure that all CAN packets are processed
# by all receivers at the same time, this process is handled synchronously.  It is important that your
# CAN receiver does not block or pause the main loop as this will impact other components and backlog
# your CAN processing.  We suggest if your script cannot run fast that you put the received CAN messages
# in to a queue and handle them in a background thread.  See the examples for samples of this.
#
# For more example scripts, search for "Profinity Example Scripts" in your favourite web search engine or check the
# Profinity doumentation on the Prohelion website at https://docs.prohelion.com for links to our examples.

def receive(canPacket):
    print("Python CanPacket Id Received : " + canPacket.CanIdAsHex)

    # ============================================================================
    # EXAMPLE CODE - These examples show how to use major Profinity features
    # ============================================================================
    # The code below demonstrates various capabilities but is commented out so it
    # doesn't affect the script's current functionality. Uncomment and modify as needed.
    # ============================================================================

    # ----------------------------------------------------------------------------
    # EXAMPLE 1: Access Received CAN Packet Data
    # ----------------------------------------------------------------------------
    # The canPacket parameter contains the received CAN packet - no need to read it
    # Access major CAN packet properties
    # print(f'CAN ID: {canPacket.CanId} (Hex: {canPacket.CanIdAsHex})')
    # print(f'Data length: {canPacket.DataLength} bytes')
    # print(f'Extended frame: {canPacket.Extended}')
    # print(f'CAN FD: {canPacket.CanFD}')
    # print(f'Remote frame (RTR): {canPacket.Rtr}')
    # print(f'Heartbeat: {canPacket.Heartbeat}')
    # print(f'Settings packet: {canPacket.Settings}')
    # print(f'Data encoding: {canPacket.DataEncoding}')
    # print(f'Age: {canPacket.MillisecondsSinceCreated} ms')
    #
    # # Read packet data in various formats
    # # Access raw byte array
    # raw_data = canPacket.Data
    # if raw_data is not None and len(raw_data) > 0:
    #     print(f'Raw data (bytes): {" ".join(f"{b:02X}" for b in raw_data)}')
    #
    # # Access data as 32-bit signed integers (most common)
    # if canPacket.Int32Pos0 is not None:
    #     print(f'Int32 at position 0: {canPacket.Int32Pos0}')
    # if canPacket.Int32Pos1 is not None:
    #     print(f'Int32 at position 1: {canPacket.Int32Pos1}')
    #
    # # Access data as floats (for floating-point values)
    # if canPacket.FloatPos0 is not None:
    #     print(f'Float at position 0: {canPacket.FloatPos0}')
    #
    # # Access individual bytes
    # if canPacket.BytePos0 is not None:
    #     print(f'Byte at position 0: {canPacket.BytePos0} (0x{canPacket.BytePos0:02X})')
    # if canPacket.BytePos1 is not None:
    #     print(f'Byte at position 1: {canPacket.BytePos1} (0x{canPacket.BytePos1:02X})')
    #
    # # Access as 16-bit signed integers
    # if canPacket.Short16Pos0 is not None:
    #     print(f'Int16 at position 0: {canPacket.Short16Pos0}')
    #
    # # Access as unsigned integers
    # if canPacket.UInt32Pos0 is not None:
    #     print(f'UInt32 at position 0: {canPacket.UInt32Pos0}')
    #

    # ----------------------------------------------------------------------------
    # EXAMPLE 2: Send CAN Packets in Response
    # ----------------------------------------------------------------------------
    # Create and send CAN packets based on received data
    # This is useful for protocol implementation, forwarding, or command responses
    #
    # from Profinity.Comms.CANBus import CanPacket
    #
    # # Method 1: Create with CAN ID only, then set data using typed properties
    # response_packet = CanPacket(0x200)
    # response_packet.Int32Pos0 = 100  # Set first 4 bytes as signed 32-bit integer
    # response_packet.Int32Pos1 = 200  # Set next 4 bytes as signed 32-bit integer
    # Profinity.CANBus.SendMessage(response_packet)
    # print(f'Sent response packet ID {response_packet.CanIdAsHex} with Int32 values: {response_packet.Int32Pos0}, {response_packet.Int32Pos1}')
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
    # Store values that persist between packet receptions within this script instance
    # Useful for maintaining counters, flags, or temporary data
    #
    # # Store different data types
    # Profinity.State.Set("packetCount", 42)
    # Profinity.State.Set("lastCanId", canPacket.CanIdAsHex)
    # from datetime import datetime
    # Profinity.State.Set("lastReceiveTime", datetime.now().isoformat())
    #
    # # Retrieve stored values (returns None if key doesn't exist)
    # packet_count_obj = Profinity.State.Get("packetCount")
    # if packet_count_obj is not None:
    #     packet_count = int(packet_count_obj)
    #     packet_count += 1  # Increment counter
    #     Profinity.State.Set("packetCount", packet_count)
    #     print(f'Packet count: {packet_count}')
    #
    # last_can_id = Profinity.State.Get("lastCanId")
    # if last_can_id is not None:
    #     print(f'Last CAN ID: {last_can_id}')
    #

    # ----------------------------------------------------------------------------
    # EXAMPLE 5: Share State (Global across all scripts)
    # ----------------------------------------------------------------------------
    # Store values that can be accessed by all scripts in the profile
    # Useful for inter-script communication and shared data
    #
    # # Set global values
    # Profinity.GlobalState.Set("lastReceivedCanId", canPacket.CanIdAsHex)
    # Profinity.GlobalState.Set("systemStatus", "Receiving")
    # from datetime import datetime
    # Profinity.GlobalState.Set("lastUpdateTime", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #
    # # Read global values set by other scripts
    # last_can_id = Profinity.GlobalState.Get("lastReceivedCanId")
    # if last_can_id is not None:
    #     print(f'Last CAN ID from other script: {last_can_id}')
    #
    # status = Profinity.GlobalState.Get("systemStatus")
    # if status is not None:
    #     print(f'System status from other script: {status}')
    #
    # # Increment shared counter (example of coordination between scripts)
    # shared_counter = Profinity.GlobalState.Get("sharedCounter")
    # if shared_counter is not None:
    #     current_count = int(shared_counter)
    #     Profinity.GlobalState.Set("sharedCounter", current_count + 1)
    #

    # ----------------------------------------------------------------------------
    # EXAMPLE 6: Filter and Process Based on Packet Content
    # ----------------------------------------------------------------------------
    # Process packets conditionally based on CAN ID, data values, or other properties
    #
    # # Filter by specific CAN ID
    # if canPacket.CanId == 0x100:
    #     print("Received packet with ID 0x100")
    #     # Process specific message type
    #
    # # Filter by data value
    # if canPacket.Int32Pos0 is not None and canPacket.Int32Pos0 > 1000:
    #     print(f'Received packet with Int32Pos0 > 1000: {canPacket.Int32Pos0}')
    #     # Process high-value packets
    #
    # # Filter by extended frame
    # if canPacket.Extended:
    #     print("Received extended frame")
    #     # Process extended frames differently
    #
    # # Filter by data length
    # if canPacket.DataLength == 8:
    #     print("Received full 8-byte packet")
    #     # Process full packets
    #
