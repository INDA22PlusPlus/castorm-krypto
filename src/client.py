import socket
import threading
from sign import *
from globals import *

key = key_gen()
signatures = {}

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
            data = encrypt(file.read())
            packet = Packet(PACKET_ID_WRITE_FILE)
            packet.write_int(id)
            packet.write_bytes(data)
            client.send(packet.get_bytes())
    except:
        print("Could not find file")

def handleGetFile(args, client):
    id = int(args[0])
    packet = Packet(PACKET_ID_WRITE_FILE)
    packet.write_int(id)
    client.send(packet.get_bytes())

def handleHelp(args, client):
    pass

cmds = {
    "quit": quit, 
    "sendfile": handleSendFile, 
    "getfile": handleGetFile,
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
    packet = Packet(data[0])
    packet.data = data[1:]
    if packet.packet_id == PACKET_ID_READ_FILE:
        id = packet.read_int()
        file = packet.read_bytes()
        print(decrypt(file, id))

def handleIncoming(client):
    data = client.recv(1024)
    if not data:
        client.close()
    handleData(client, data)
    pass

def client_program():

    client_socket = socket.socket() 
    client_socket.connect((IP_ADDRESS, PORT)) 

    t = threading.Thread(target=handleInput, args=(client_socket,))
    
    t.start()
    t.join()
    
if __name__ == '__main__':
    client_program()