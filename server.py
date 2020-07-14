import socket
from _thread import *
from random import randint
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client["quiz_database"]
history_questions = db["history_questions"]
geography_questions = db["geography_questions"]


server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
all_connections = []

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)

print("Waiting for connection, Server started")


def readFromMongo(oblast):
    por = ""
    i = 0
    while i < 3:
        rnd = randint(1, 3)
        result = oblast.find_one({"_id": rnd})
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


def game(conn1, conn2):
    start_new_thread(threaded_client, (conn1, conn2))
    start_new_thread(threaded_client, (conn2, conn1))


def threaded_client(conn1, conn2):
    game_connections = []
    game_connections.append(conn1)
    game_connections.append(conn2)
    while True:
        try:
            data = conn1.recv(2048).decode()
            if data == "history":
                reply = readFromMongo(history_questions)
                print("procitao pitanja")
                for c in game_connections:
                    c.sendall(str.encode("pokreni_history::" + reply))
                print(reply)
                continue

            if data == "geography":
                reply = readFromMongo(geography_questions)
                print("procitao pitanja")
                for c in game_connections:
                    c.sendall(str.encode("pokreni_geography::" + reply))
                print(reply)
                continue

            if data == "fin":
                conn2.send(str.encode("turn"))
                continue

            if str(data).startswith("Score:"):
                conn2.send(str.encode(data))
                continue

            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", data)
                print("Sending : ", data)

            for c in game_connections:
                c.sendall(str.encode(data))

        except:
            break

    print("Lost connection")
    conn.close()


while True:
    conn, addr = s.accept()
    all_connections.append(conn)
    print("Connected to:", addr)
    if len(all_connections) == 2:
        for conn in all_connections:
            conn.send(str.encode("ready"))
        start_new_thread(game, (all_connections[0], all_connections[1]))
        all_connections.clear()