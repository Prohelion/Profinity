using System;
using Profinity.Scripting;
using System.Threading;

public class CSharpCancelTest : ProfinityScript, IProfinityRunnableScript
{
    public bool Run()
    {
        System.Console.WriteLine("This is a CSharp Message!");
        System.Console.WriteLine("Now sleeping");

        while (!Profinity.ScriptCancelled)
        {
            Thread.Sleep(100);
            System.Console.WriteLine("State " +Profinity.ScriptCancelled);
        }

        System.Console.WriteLine(Profinity.Message);
        return true;
    }
}