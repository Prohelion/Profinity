import time

def Loop():
    print('This is a Python loop!')
    while not (Profinity.ScriptCancelled):
        print('About to sleep')
        time.sleep(1)
        print('Finished Sleeping')

Loop()
print('Exiting the Program')