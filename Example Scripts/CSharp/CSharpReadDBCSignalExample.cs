using System;
using Profinity.Scripting;
using Profinity.Comms.CANBus;
using Profinity.Model.DBC;

public class CSharpReadDBCSignalExample : ProfinityScript, IProfinityRunnableScript
{
    public bool Run()
    {
        // Inject a CAN message with test data (matches Profinity test script pattern)
        // Message: STW_ANGLHP_STAT (CAN ID 14)
        // Signal: StW_AnglHP - raw value 0 gives -819.2 with factor 0.1 and offset -819.2
        byte[] testData = new byte[8];
        testData[0] = 0x00;
        testData[1] = 0x00;

        CanPacket testPacket = new(14, false, false, false, 8, CanPacket.Encoding.LittleEndian, testData);
        Profinity.Console.WriteLine($"Created CAN packet with ID {testPacket.CanId}");

        Profinity.CANBus.InjectReceivedCanPacket(testPacket);
        Profinity.Console.WriteLine("CAN packet injected");

        // Read the DBC signal via Profinity.DBC
        // Requires a component named "TestDBCComponent" with message STW_ANGLHP_STAT and signal StW_AnglHP
        // (or change these to match your profile)
        string componentName = "TestDBCComponent";
        string messageName = "STW_ANGLHP_STAT";
        string signalName = "StW_AnglHP";

        try
        {
            double signalValue = Profinity.DBC.GetDbcSignal(componentName, messageName, signalName).Value;
            Profinity.Console.WriteLine($"Signal value from DBC: {signalValue}");

            double expectedValue = (0 * 0.1) - 819.2;
            if (Math.Abs(signalValue - expectedValue) < 0.01)
            {
                Profinity.Console.WriteLine($"Signal value matches expected: {expectedValue}");
            }
            else
            {
                Profinity.Console.WriteLine($"Signal value mismatch. Expected: {expectedValue}, Got: {signalValue}");
                return false;
            }
        }
        catch (Exception ex)
        {
            Profinity.Console.WriteLine($"Error reading DBC signal: {ex.Message}");
            return false;
        }

        Profinity.Console.WriteLine("DBC read completed successfully");
        return true;
    }
}
