from Profinity.Comms.CANBus import CanPacket

packet = CanPacket(0x100);
packet.Int32Pos0 = 100;
packet.Int32Pos1 = 200;

Profinity.CANBus.SendMessage(packet);