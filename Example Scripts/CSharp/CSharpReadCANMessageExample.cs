using System;
using Profinity.Scripting;
using Profinity.Comms.CANBus;

public class CSharpReadCANMessageExample : ProfinityScript, IProfinityRunnableScript
{
    public bool Run()
    {
        // Get the latest valid CAN packet received for a specific CAN ID (replace 0x100 with your CAN ID)
        uint canId = 0x100;
        CanPacket receivedPacket = Profinity.CANBus.LatestValidPacketReceivedByID(canId);

        if (receivedPacket != null)
        {
            Profinity.Console.WriteLine($"CAN ID: {receivedPacket.CanId} (Hex: {receivedPacket.CanIdAsHex})");
            Profinity.Console.WriteLine($"Data length: {receivedPacket.DataLength} bytes");
            if (receivedPacket.Int32Pos0.HasValue)
            {
                Profinity.Console.WriteLine($"Int32 at position 0: {receivedPacket.Int32Pos0.Value}");
            }
        }
        else
        {
            Profinity.Console.WriteLine($"No valid CAN packet found for ID {canId:X}");
        }

        return true;
    }
}
