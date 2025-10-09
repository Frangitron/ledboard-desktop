"""
FIXME !!! MAKE A LIB WITH THIS !!!
"""
import socket

from ledboarddesktop.artnet import packet


class ArtnetUniverse:
    def __init__(self, universe_number):
        self.buffer = bytearray(packet.PACKET_SIZE)

        self._universe_number = universe_number
        self._packet_maker = packet.DmxPacketMaker(self._universe_number)

    def make_packet(self) -> bytearray:
        return self._packet_maker.make_dmx_packet(self.buffer)


class ArtnetBroadcaster:
    UDP_PORT = 6454

    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.universes: dict[int, ArtnetUniverse] = dict()

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._socket.settimeout(1)  # todo check if OK

    def add_universe(self, universe_number: int):
        if universe_number in self.universes:
            raise ValueError(f"Universe {universe_number} already exists")

        self.universes[universe_number] = ArtnetUniverse(universe_number)

    def send_data(self):
        for universe in self.universes.values():
            packet = universe.make_packet()
            self._socket.sendto(packet, (self.target_ip, self.UDP_PORT))

    def send_artsync(self):
        self._socket.sendto(packet.ARTSYNC_PACKET, (self.target_ip, self.UDP_PORT))

    def send_data_synced(self):
        self.send_data()
        self.send_artsync()
