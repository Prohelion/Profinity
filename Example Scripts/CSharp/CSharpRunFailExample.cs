using System;
using Profinity.Scripting;

public class CSharpRunFailTest : ProfinityScript, IProfinityRunnableScript
{
    public bool Run()
    {
        System.Console.WriteLine("This is a CSharp Runner about to fail!");        
        return false;
    }
}