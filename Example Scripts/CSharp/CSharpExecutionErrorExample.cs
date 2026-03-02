using System;
using Profinity.Scripting;

public class CSharpExecutionErrorTest : ProfinityScript, IProfinityRunnableScript
{
    // Bad formatted file
    public bool Run()
    {
        throw new InvalidOperationException("Kaboom");
    }
}