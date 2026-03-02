using System;
using Profinity.Scripting;

public class CSharpStdOutTest : ProfinityScript, IProfinityRunnableScript
{
    public bool Run()
    {
        Profinity.Console.WriteLine("STDOUT");
        return true;
    }
}