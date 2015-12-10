
from terminal_colors import bcolors

try:
    import optirx as rx
except ImportError:
    print bcolors.FAIL + "Error importing library, please install optirx by running: sudo pip install optirx"+ bcolors.ENDC
from event import Event


class NatNetParser(object):
    """
    NatNetParser class connects to a NatNet server, reads MoCap data,
    parses it and makes it available as python objects.
    """

    def __init__(self, host=None, multicast=None, port=None):
        self.host = host
        self.multicast = multicast
        self.port = int(port)
        self.skeletons = []
        self.rigidbodies = []
        self.version = (2, 7, 0, 0)
        self.updated = Event()
        self.connected = False

    def setVersion(self, version):
        self.version=version

    def getVersion(self):
        return version

    def connect(self):
        try:
            if self.host is None:
                self.dsock = rx.mkdatasock() #Connecting to localhost
            elif self.multicast is not None and self.port is not None:
                self.dsock = rx.mkdatasock(ip_address=self.host, multicast_address=self.multicast, port=self.port) #Connecting to multicast address
            else:
                self.dsock = rx.mkdatasock(ip_address=self.host, port=self.port) # Connecting to IP address
            self.connected = True
        except:
            self.connected = False

        return self.connected

    def disconnect():
        self.dsock = None
        self.connected = False

    def isConnected(self):
        return self.connected

    def countSkeletons(self):
        return len(self.skeletons)

    def countRigidbodies(self):
        return len(self.rigidbodies)

    def getSkeleton(self, index):
        if index > -1 and index < countSkeletons():
            return skeletons[index]
        else:
            return None

    def getRigidbody(self, index):
        if index > -1 and index < countRigidbodies():
            return rigidbodies[index]
        else:
            return None

    def run(self):
        while True:
            data = self.dsock.recv(rx.MAX_PACKETSIZE)
            packet = rx.unpack(data, version=version)
            if type(packet) is rx.SenderData:
                setVersion(packet.natnet_version)
            self.parse(packet)
            self.updated()

    def parse(self, packet):
        self.skeletons = packet.skeletons
        self.rigidbodies = []

        for s in packet.skeletons:
            for r in s.rigidbodies:
                self.rigidbodies.append(r)
