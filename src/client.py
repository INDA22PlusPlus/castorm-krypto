import socket
import threading
from globals import *

def quit(args, client):
    client.close()
    exit()

def encrypt(text):
    return text

def decrypt(text):
    return text

def handleSendFile(args, client):
    path = args[0]
    try:
        with open(path, "r") as file:
            text = encrypt(file.read())
            client.send(text.encode())
    except:
        print("Could not find file")

cmds = {
    "quit": quit, 
    "sendfile": handleSendFile, 
    "sendtext": lambda args, client: client.send(" ".join(args).encode())
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

incomingcmds = {
    "fileerror": file_error,
    "file": file_received, 
    "debug": debug
}

def handleIncomingCmd(cmd, args, client):
    if cmd not in incomingcmds:
        print("[WARNING] Received unknown packet type!")
    pass

def handleData(client, data):
    s = str(data)
    ss = s.split()
    cmd = ss[0]
    args = ss[1:]
    handleIncomingCmd(cmd, args, client)

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