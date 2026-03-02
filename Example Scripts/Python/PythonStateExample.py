# Test script state: local State and global GlobalState (matches Profinity test script pattern)
Profinity.State.Set("testKey", "testValue")
Profinity.State.Set("testNumber", 42)

# Test global state (shared across all scripts in the profile)
Profinity.GlobalState.Set("globalKey", "globalValue")
Profinity.GlobalState.Set("globalNumber", 100)

# Verify we can read back
localValue = Profinity.State.Get("testKey")
globalValue = Profinity.GlobalState.Get("globalKey")

print(f"Local State: {localValue}")
print(f"Global State: {globalValue}")
