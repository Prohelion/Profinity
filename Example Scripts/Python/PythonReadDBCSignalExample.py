# Read the DBC signal value via Profinity.DBC (matches Profinity test script pattern)
# Requires a component with this DBC loaded; for a self-contained test run CSharpReadDBCSignalExample first (injects CAN)
# Component: TestDBCComponent, Message: STW_ANGLHP_STAT (CAN ID 14), Signal: StW_AnglHP
# Raw value 0 = -819.2 after factor 0.1 and offset -819.2

component_name = "TestDBCComponent"
message_name = "STW_ANGLHP_STAT"
signal_name = "StW_AnglHP"

try:
    signal = Profinity.DBC.GetDbcSignal(component_name, message_name, signal_name)
    signal_value = signal.Value
    print(f"Signal value from DBC: {signal_value}")

    expected_value = (0 * 0.1) - 819.2  # -819.2
    if abs(signal_value - expected_value) < 0.01:
        print(f"Signal value matches expected: {expected_value}")
    else:
        print(f"Signal value mismatch. Expected: {expected_value}, Got: {signal_value}")
except Exception as ex:
    print(f"Error reading DBC signal: {ex.Message}")
