# Get the latest valid CAN packet received for a specific CAN ID (replace 0x100 with your CAN ID)
can_id = 0x100
received_packet = Profinity.CANBus.LatestValidPacketReceivedByID(can_id)

if received_packet is not None:
    print(f'CAN ID: {received_packet.CanId} (Hex: {received_packet.CanIdAsHex})')
    print(f'Data length: {received_packet.DataLength} bytes')
    if received_packet.Int32Pos0 is not None:
        print(f'Int32 at position 0: {received_packet.Int32Pos0}')
else:
    print(f'No valid CAN packet found for ID {hex(can_id)}')
