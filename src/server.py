import socket
import threading
from merkle import *
from globals import *
import secrets


files = {
    0: b"nonsense data"
}
root = build_tree([files[0]])

def handleData(client, address, data):
    packet = Packet(int(data[0]))
    packet.data = data[1:]
    print("id:", packet.packet_id)
    if packet.packet_id == PACKET_ID_WRITE_FILE:
        id = packet.read_int()
        file = packet.read_bytes()
        files[id] = file
        insert_data_at_index(root, id, file)
        recalculate_hashes(root)
        print("Got file:", file)
    if packet.packet_id == PACKET_ID_READ_FILE:
        id = packet.read_int()
        if id in files:
            file = files[id]
        else:
            print("Requested file does not exist! Id:", id)
            return
        response = Packet(PACKET_ID_READ_FILE)
        response.write_int(id)
        response.write_bytes(file)
        print("Requested file:", id)
        client.send(response.get_bytes())
    if packet.packet_id == PACKET_ID_GET_TOP_HASH:
        response = Packet(PACKET_ID_GET_TOP_HASH)
        response.write_string(root.data)
        print("Requested Top Hash")
        client.send(response.get_bytes())
    if packet.packet_id == PACKET_ID_GET_HASH:
        id = packet.read_int()
        h = get_node_hash(root, id)
        if h is None:
            print("hash does not exist in tree. Id:", id)
            return
        response = Packet(PACKET_ID_GET_HASH)
        response.write_int(id)
        response.write_string(h)
        print("Requested hash:", id)
        client.send(response.get_bytes())
    if packet.packet_id == PACKET_ID_GET_TAMPERED_FILE:
        id = packet.read_int()
        if id in files:
            file = files[id]
        else:
            print("Requested file does not exist! Id:", id)
            return
        response = Packet(PACKET_ID_READ_FILE)
        response.write_int(id)
        file = bytes([_a ^ _b for _a, _b in zip(file, secrets.token_bytes(len(file)))])
        response.write_bytes(file)
        print("Requested file:", id)
        client.send(response.get_bytes())

def handleConnection(client, address):
    while True:
        data = client.recv(1024)
        print("recieved data")
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