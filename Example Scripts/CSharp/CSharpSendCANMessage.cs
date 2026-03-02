using System;
using Profinity.Scripting;
using Profinity.Comms.CANBus;
using Profinity.Services;

public class CSharpRunTest : ProfinityScript, IProfinityRunnableScript
{
    public bool Run()
    {
        CanPacket packet = new CanPacket(0x100)
        {
            Int32Pos0 = 100,
            Int32Pos1 = 200
        };

        Profinity.CANBus.SendMessage(packet);
        return true;
    }
}