using System;
using Profinity.Scripting;

public class CSharpErrorTest : ProfinityScript, IProfinityRunnableScript
{
    public bool Run()
    {
        Profinity.Console.Error.WriteLine("STDERR");        
        return true;
    }
}