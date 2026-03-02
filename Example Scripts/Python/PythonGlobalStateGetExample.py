# Read a value from GlobalState that was set by another script (e.g. PythonGlobalStateSetExample)
shared_value = Profinity.GlobalState.Get("sharedKey")
print(f"Read sharedKey from GlobalState: {shared_value}")
