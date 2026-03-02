using System;
using Profinity.Scripting;

public class CSharpMinimalServiceTest : ProfinityBaseService
{
    public override bool OnStart()
    {
        System.Console.WriteLine("Started Minimal CSharp Service");
        return true;
    }
}