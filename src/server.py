import socket
import threading
from merkle import *
from globals import *


files = {
    0: b"nonsense data"
}
merkle_tree = build_tree([files[0]])

def handleData(client, address, data):
    packet = Packet(int(data[0]))
    packet.data = data[1:]
    if packet.packet_id == PACKET_ID_WRITE_FILE:
        id = packet.read_int()
        file = packet.read_bytes()
        files[id] = file
        merkle_tree.insert(file)
    if packet.packet_id == PACKET_ID_READ_FILE:
        id = packet.read_int()
        file = files[id]
        response = Packet(PACKET_ID_READ_FILE)
        packet.write_int(id)
        response.write_bytes(file)
        client.send(response.get_bytes())

def handleConnection(client, address):
    while True:
        data = client.recv(1024)
        if not data:
            break
        handleData(client, address, data)
    print(str(address), "disconnected")
    client.close()

def handleInput(data, server):
    if data == "quit":
        print("Closing Server")
        server.close()
        exit()

def handleServer(server):
    while True:
        data = input()
        handleInput(data, server)
        

def server_program():

    server_socket = socket.socket()  
    server_socket.bind((IP_ADDRESS, PORT))  

    server_socket.listen(MAX_CLIENTS)

    threads = []
    s = threading.Thread(target=handleServer, args=(server_socket,))
    s.start()
    threads.append(s)
    while True:
        print("Waiting for client")
        conn, address = server_socket.accept()  
        print("Connection from: " + str(address))
        t = threading.Thread(target=handleConnection, args=(conn, address,))
        t.start()
        threads.append(t)


if __name__ == '__main__':
    server_program()