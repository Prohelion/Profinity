using System;
using Profinity.Scripting;

public class CSharpRunTest : ProfinityScript, IProfinityRunnableScript
{
    public bool Run()
    {
        Profinity.Console.WriteLine("This is a CSharp Message2!");
        Profinity.Console.WriteLine(Profinity.Message);
        return true;
    }
}