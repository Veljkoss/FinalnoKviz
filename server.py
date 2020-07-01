import socket
from _thread import *

server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    s.bind((server, port))
except socket.error as e:
    str(e)


s.listen(2)


print("Wainting for connection, Server started")


def threaded_client(conn, player):
    conn.send(str.encode(""))
    reply = ""
    while True:
        try:
            data = conn.recv(2048).decode()
            if data == "history":
                reply = "history"
            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1



