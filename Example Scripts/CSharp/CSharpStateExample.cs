using System;
using Profinity.Scripting;

public class CSharpStateExample : ProfinityScript, IProfinityRunnableScript
{
    public bool Run()
    {
        // Test local state (persists between runs of this script instance)
        Profinity.State.Set("testKey", "testValue");
        Profinity.State.Set("testNumber", 42);

        // Test global state (shared across all scripts in the profile)
        Profinity.GlobalState.Set("globalKey", "globalValue");
        Profinity.GlobalState.Set("globalNumber", 100);

        // Verify we can read back
        object localValue = Profinity.State.Get("testKey");
        object globalValue = Profinity.GlobalState.Get("globalKey");

        Profinity.Console.WriteLine($"Local State: {localValue}");
        Profinity.Console.WriteLine($"Global State: {globalValue}");

        return true;
    }
}
