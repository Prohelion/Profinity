using System;
using Profinity.Scripting;

public class CSharpGlobalStateSetExample : ProfinityScript, IProfinityRunnableScript
{
    public bool Run()
    {
        // Set a value in GlobalState for another script to read (e.g. CSharpGlobalStateGetExample or Python)
        Profinity.GlobalState.Set("sharedKey", "sharedValue");
        Profinity.Console.WriteLine("Set sharedKey in GlobalState");
        return true;
    }
}
