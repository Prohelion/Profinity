/* Profinity Script - CSharp Service Template
*
* This script will run in the background as a Profinity Service.  There are four states that the service
* can be in and as the service transitions between states these functions are called.  It is not
* necessary to implement each state but it is recomended.
*
* This example demonstrates a simplified service that logs a message every second while running.
* The engine handles all the threading complexity - you just need to implement OnStart/OnStop/OnPause/OnContinue
* for setup/cleanup, and Run() to do your work.
*
* For more example scripts, search for "Profinity Example Scripts" in your favourite web search engine or check the
* Profinity doumentation on the Prohelion website at https://docs.prohelion.com for links to our examples.
*/

using System;
using System.Threading;
using Profinity.Scripting;

public class CSharpServiceTest : ProfinityBaseService
{
    private int _logCount = 0;
    
    public override bool OnStart()
    {
        Profinity.Console.WriteLine("Service started");
        _logCount = 0;
        return true;
    }
    
    public override bool OnStop()
    {
        Profinity.Console.WriteLine("Service stopped");
        return true;
    }
    
    public override bool OnPause()
    {
        Profinity.Console.WriteLine("Service paused");
        return true;
    }
    
    public override bool OnContinue()
    {
        Profinity.Console.WriteLine("Service continued");
        return true;
    }
    
    // Example 1: Run() method WITHOUT a loop
    // The engine calls Run() repeatedly (in its own loop)
    // This is useful for simple tasks that run once per iteration
    public override bool Run()
    {
        // Do a single piece of work each time Run() is called
        _logCount++;
        Profinity.Console.WriteLine($"Log entry #{_logCount} at {DateTime.Now:HH:mm:ss}");
        
        // Optional: Add a delay to control the rate of execution
        Thread.Sleep(1000);
        
        // Return true to continue running, or false to stop the service
        // When Run() returns true, the engine will call it again (if service is still running)
        // When Run() returns false, the service will stop
        return true;
    }
    
    // Example 2: Run() method WITH a loop (COMMENTED OUT - for reference only)
    // Uncomment this and comment out the method above if you prefer to manage your own loop
    // When pause occurs, the cancellation token is cancelled, ScriptCancelled becomes true,
    // the loop exits, Run() returns, and the service pauses.
    // When continue occurs, a new token is created and Run() is called again (starting a fresh loop).
    /*
    public override bool Run()
    {
        // Run() contains its own loop - you manage the looping logic
        // The loop continues until Profinity.ScriptCancelled becomes true
        while (!Profinity.ScriptCancelled)
        {
            // Do your work here
            _logCount++;
            Profinity.Console.WriteLine($"Log entry #{_logCount} at {DateTime.Now:HH:mm:ss}");
            
            // Script manages its own timing within the loop
            Thread.Sleep(1000);
            
            // You can check cancellation multiple times in your loop if needed
            // for example, before doing long-running operations:
            if (Profinity.ScriptCancelled)
            {
                break; // Exit loop early if cancelled
            }
        }
        
        // When the loop exits (because ScriptCancelled became true), Run() returns
        // On pause: This happens immediately when pause is called
        // On stop: This happens when stop is called
        Profinity.Console.WriteLine("Run() loop exited due to cancellation");
        
        // Return true to allow service to continue (will be called again on continue),
        // or false to stop the service completely
        return true;
    }
    */
}
