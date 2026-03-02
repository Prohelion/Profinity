def on_start():
    print('Python Service Started!')
    return True

def on_stop():
    print('Python Service Stopped!')
    return True

def on_pause():
    print('Python Service Paused!')
    return True

def on_continue():
    print('Python Service Continued!')
    return True

def on_shutdown():
    print('Python Service Shutdown!')
    return True