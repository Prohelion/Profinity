# Profinity Script - Python Service Template
#
# This script will run in the background as a Profinity Service.  There are four states that the service
# can be in and as the service transitions between states these functions are called.  It is not
# necessary to implement each state but it is recomended.
#
# This example demonstrates a simplified service that logs a message every second while running.
# The engine handles all the threading complexity - you just need to implement on_start/on_stop/on_pause/on_continue
# for setup/cleanup, and run() to do your work.
#
# Code outside of the functions will be executed when the script is first run, so if you want
# to establish anything required by the script, do so there.
#
# For more example scripts, search for "Profinity Example Scripts" in your favourite web search engine or check the
# Profinity doumentation on the Prohelion website at https://docs.prohelion.com for links to our examples.

_log_count = 0

def on_start():
    """Called when the service starts"""
    global _log_count
    print('Service started')
    _log_count = 0
    return True

def on_stop():
    """Called when the service stops"""
    print('Service stopped')
    return True

def on_pause():
    """Called when the service is paused"""
    print('Service paused')
    return True

def on_continue():
    """Called when the service is continued after being paused"""
    print('Service continued')
    return True

# Example 1: run() function WITHOUT a loop
# The engine calls run() repeatedly (in its own loop)
# This is useful for simple tasks that run once per iteration
def run():
    """Called repeatedly by the engine - does work once per call"""
    global _log_count
    
    # Do a single piece of work each time run() is called
    _log_count += 1
    from datetime import datetime
    current_time = datetime.now().strftime('%H:%M:%S')
    print(f'Log entry #{_log_count} at {current_time}')
    
    # Optional: Add a delay to control the rate of execution
    import time
    time.sleep(1)
    
    # Return True to continue running, or False to stop the service
    # When run() returns True (or None), the engine will call it again (if service is still running)
    # When run() returns False, the service will stop
    return True

# Example 2: run() function WITH a loop (COMMENTED OUT - for reference only)
# Uncomment this and comment out the function above if you prefer to manage your own loop
# When pause occurs, the cancellation token is cancelled, ScriptCancelled becomes true,
# the loop exits, run() returns, and the service pauses.
# When continue occurs, a new token is created and run() is called again (starting a fresh loop).
"""
def run():
    \"\"\"Called once by the engine - contains its own loop\"\"\"
    global _log_count
    
    # run() contains its own loop - you manage the looping logic
    # The loop continues until Profinity.ScriptCancelled becomes true
    while not Profinity.ScriptCancelled:
        # Do your work here
        _log_count += 1
        from datetime import datetime
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f'Log entry #{_log_count} at {current_time}')
        
        # Script manages its own timing within the loop
        import time
        time.sleep(1)
        
        # You can check cancellation multiple times in your loop if needed
        # for example, before doing long-running operations:
        if Profinity.ScriptCancelled:
            break  # Exit loop early if cancelled
    
    # When the loop exits (because ScriptCancelled became true), run() returns
    # On pause: This happens immediately when pause is called
    # On stop: This happens when stop is called
    print('run() loop exited due to cancellation')
    
    # Return True to allow service to continue (will be called again on continue),
    # or False to stop the service completely
    return True
"""
