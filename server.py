import socket
from _thread import *

server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
all_connections=[]

try:
    s.bind((server, port))
except socket.error as e:
    str(e)


s.listen(2)


print("Waiting for connection, Server started")


def threaded_client(conn, player):

    while True:
        try:
            data = conn.recv(2048).decode()

            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", data)
                print("Sending : ", data)

            for c in all_connections:
                c.sendall(str.encode(data))
        except:
            break

    print("Lost connection")
    all_connections.remove(conn)
    conn.close()

currentPlayer = 0

while True:

    conn, addr = s.accept()
    all_connections.append(conn)
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1



