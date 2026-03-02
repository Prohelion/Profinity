using System;
using Profinity.Scripting;

public class CSharpGlobalStateGetExample : ProfinityScript, IProfinityRunnableScript
{
    public bool Run()
    {
        // Read a value from GlobalState that was set by another script (e.g. CSharpGlobalStateSetExample)
        object sharedValue = Profinity.GlobalState.Get("sharedKey");
        Profinity.Console.WriteLine($"Read sharedKey from GlobalState: {sharedValue}");
        return true;
    }
}
