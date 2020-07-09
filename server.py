import socket
from _thread import *
from random import randint

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client["quiz_database"]
history_questions = db["history_questions"]

server = "127.0.0.1"
port = 5555

print(history_questions.find_one())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
all_connections = []

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)

print("Waiting for connection, Server started")


def readFromMongo():
    por = ""
    i = 0
    while i < 3:
        rnd = randint(1, 3)
        result = history_questions.find_one({"_id": rnd})
        print("test")
        quest = result["quest"]
        print(quest)
        ans1 = result["ans1"]
        print(ans1)
        ans2 = result["ans2"]
        print(ans2)
        ans3 = result["ans3"]
        print(type(ans3))
        crt = str(result["crt"])
        print(type(crt))
        por = por + quest + ',' + ans1 + ',' + ans2 + ',' + ans3 + ',' + crt + '/'
        # str = str.join((quest, ",", ans1, ",", ans2, ",", ans3, "/"))
        print("ziv sam")
        i = i + 1

    return por


def threaded_client(conn, player):
    while True:
        try:
            data = conn.recv(2048).decode()
            print("primio: " + data)
            if data == "history":
                reply = readFromMongo()
                print("procitao pitanja")
                for c in all_connections:
                    c.sendall(str.encode("pokreni_history::" + reply))
                print(reply)

                continue

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
