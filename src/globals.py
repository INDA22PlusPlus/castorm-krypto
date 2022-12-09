from socket import gethostname
PORT = 1338
MAX_CLIENTS = 10
IP_ADDRESS = gethostname()

PACKET_ID_WRITE_FILE = 1
PACKET_ID_READ_FILE = 2
PACKET_ID_GET_TOP_HASH = 3
PACKET_ID_GET_HASH = 4
PACKET_ID_GET_TAMPERED_FILE = 5

class Packet:
    def __init__(self, packet_id: int) -> None:
        self.packet_id = packet_id
        self.data = b''
        self.readpos = 0

    def get_bytes(self):
        return self.packet_id.to_bytes(1, "big", signed=True) + self.data

    def write_int(self, num: int):
        self.data += num.to_bytes(2, "big", signed=True)

    def read_int(self):
        val = int.from_bytes(self.data[self.readpos:self.readpos+2], "big", signed=True)
        self.readpos += 2
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
