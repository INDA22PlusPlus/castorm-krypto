import socket
import threading
from merkle import *
from sign import *
from globals import *

key = key_gen()
signatures = {}

root = build_tree([b"nonsense data"])

def quit(args, client):
    client.close()
    exit()

def encrypt(file, id):
    data, signature = encrypt_and_sign(file.encode(), key)
    signatures[id] = signature
    return data

def decrypt(file, id):
    data = decrypt_and_verify(file, signatures[id], key)
    return data

def handleSendFile(args, client):
    id = int(args[0])
    path = args[1]
    try:
        with open(path, "r") as file:
            data = encrypt(file.read(), id)
            packet = Packet(PACKET_ID_WRITE_FILE)
            packet.write_int(id)
            packet.write_bytes(data)
            insert_data_at_index(root, id, data)
            recalculate_hashes(root)
            client.send(packet.get_bytes())
    except FileNotFoundError:
        print("Could not find file")

def handleGetFile(args, client):
    id = int(args[0])
    packet = Packet(PACKET_ID_READ_FILE)
    packet.write_int(id)
    client.send(packet.get_bytes())

def handleHelp(args, client):
    pass

def handleGetTopHash(args, client):
    packet = Packet(PACKET_ID_GET_TOP_HASH)
    client.send(packet.get_bytes())

cmds = {
    "quit": quit, 
    "sendfile": handleSendFile, 
    "getfile": handleGetFile,
    "gettophash": handleGetTopHash,
    "help": handleHelp
} 

def handleCmd(cmd, args, client):
    if cmd not in cmds:
        print("Unknown command. Type help for a list of all commands.")
        return
    command = cmds[cmd]
    command(args, client)

def handleInput(client):
    message = input()
    
    while True:
        data = message.split()
        cmd = data[0]
        args = data[1:]
        handleCmd(cmd.lower().strip(), args, client)
        message = input()  

def file_error(args, client):
    pass

def file_received(args, client):
    pass

def debug(args, client):
    pass


def handleData(client, data):
    packet = Packet(int(data[0]))
    packet.data = data[1:]
    if packet.packet_id == PACKET_ID_READ_FILE:
        id = packet.read_int()
        file = packet.read_bytes()
        print(decrypt(file, id).decode())
    if packet.packet_id == PACKET_ID_GET_TOP_HASH:
        h = packet.read_string()
        print("got top hash:", h)
        print("actual top hash:", root.data)
        if h == root.data:
            print("Server Merkle Tree is valid")
        else:
            print("Server Merkle Tree is invalid")

def handleIncoming(client):
    while True:
        data = client.recv(1024)
        if not data:
            client.close()
            break
        handleData(client, data)

def client_program():

    client_socket = socket.socket() 
    client_socket.connect((IP_ADDRESS, PORT)) 

    t = threading.Thread(target=handleInput, args=(client_socket,))
    t2 = threading.Thread(target=handleIncoming, args=(client_socket,))
    
    t.start()
    t2.start()

    t.join()
    t2.join()

if __name__ == '__main__':
    client_program()