import socket
import threading
from globals import *

def handleData(client, address, data):
    print(f"from [{str(address)}]: " + str(data))

def handleConnection(client, address):
    while True:
        data = client.recv(1024).decode()
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