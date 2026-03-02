using System;
using Profinity.Scripting;

public class CSharpServiceTest : ProfinityBaseService
{
    public override bool OnStart()
    {
        Profinity.Console.WriteLine("Started CSharp Service");
        return true;
    }

    public override bool OnStop()
    {
        Profinity.Console.WriteLine("Stopped CSharp Service");
        return true;
    }

    public override bool OnPause()
    {
        Profinity.Console.WriteLine("Paused CSharp Service");
        return true;
    }

    public override bool OnContinue()
    {
        Profinity.Console.WriteLine("Continue CSharp Service");
        return true;
    }   
}