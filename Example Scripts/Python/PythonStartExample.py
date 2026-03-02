from Profinity.Comms.CANBus import CanPacket
from time import sleep

def Send500():
    packet = CanPacket(0x500)
    packet.UShort16Pos2 = 1
    packet.UShort16Pos0 = 4098
    Profinity.CANBus.SendMessage(packet)

def Send505(byte0):
    packet = CanPacket(0x505)
    packet.BytePos0 = byte0
    Profinity.CANBus.SendMessage(packet)

print('Engage Tester Starting, run for 10 seconds then shutdown')

count = 0
while (count < 100 and not Profinity.ScriptCancelled):
    count = count + 1
    Send500()    
    if (count < 10):
        Send505(0x0)
    if (count > 10):
        Send505(0x70)
    if (count > 30):
        Send505(0x30)
    sleep(0.1)
    print('Completed Loop ' + str(count))
    
# Cleanly shut it down
Send505(0x0)