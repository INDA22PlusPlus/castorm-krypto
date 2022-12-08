from socket import gethostname
PORT = 1338
MAX_CLIENTS = 10
IP_ADDRESS = gethostname()

PACKET_ID_WRITE_FILE = 0
PACKET_ID_READ_FILE = 1
PACKET_ID_GET_TOP_HASH = 2

class Packet:
    def __init__(self, packet_id) -> None:
        self.packet_id = packet_id.to_bytes(1, "little")
        self.data = b''
        self.readpos = 0

    def get_bytes(self):
        return self.packet_id + self.data

    def write_int(self, num):
        self.data += num.to_bytes(1, "little")

    def read_int(self):
        val = int(self.data[self.readpos])
        self.readpos += 1
        return val

    def write_string(self, string):
        self.write_int(len(string))
        self.data += string.encode()

    def read_string(self):
        num = self.read_int()
        val = self.data[self.readpos:self.readpos + num]
        self.readpos += num
        return val.decode()
    
    def write_bytes(self, data):
        self.write_int(len(data))
        self.data += data
    
    def read_bytes(self):
        num = self.read_int()
        data = self.data[self.readpos:self.readpos + num]
        self.readpos += num
        return data

