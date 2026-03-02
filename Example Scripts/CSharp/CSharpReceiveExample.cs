using System;
using Profinity.Scripting;
using Profinity.Comms.CANBus;

public class CSharpRunTest : ProfinityScript, IProfinityReceiverScript
{
    public void Receive(CanPacket canPacket)
    {
        Profinity.Console.WriteLine("CSharp CanId Received : " + canPacket.CanIdAsHex);                
    }
}