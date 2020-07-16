import socket
from _thread import *
from random import randint
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client["quiz_database"]
history_questions = db["history_questions"]
geography_questions = db["geography_questions"]
players = db["players"]


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
    izabrani = []
    while i < 3:
        rnd = randint(1, 3)
        while rnd in izabrani:
            rnd = randint(1,3)


        izabrani.append(rnd)

        result = oblast.find_one({"_id": rnd})
        quest = result["quest"]
        ans1 = result["ans1"]
        ans2 = result["ans2"]
        ans3 = result["ans3"]
        crt = str(result["crt"])
        por = por + quest + ',' + ans1 + ',' + ans2 + ',' + ans3 + ',' + crt + '/'
        i = i + 1

    return por


def game(conn1, conn2):
    start_new_thread(threaded_client, (conn1, conn2))
    start_new_thread(threaded_client, (conn2, conn1))


def threaded_client(conn1, conn2):
    playerName = ""
    score = 0

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
                score = int(str(data).split(":")[1])
                conn2.send(str.encode(data))
                continue

            if str(data).startswith("name:"):
                playerName = str(data).split(':')[1]
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

    print(playerName)
    print(score)

    pl = players.find()
    postoji = False
    for player in pl:
        if playerName == player["name"]:
            players.update_one({ "_id": player["_id"]}, { "$set": {"score": int(player["score"]) + score}})
            postoji = True

    if not postoji:
        players.insert_one({ "name": playerName, "score": score})

    lvl = score / 30

    print("Lost connection")
    conn.close()

def logHandler(conn):
    while True:
        try:
            data = conn.recv(2048).decode()
            if data == "log":
                pass
            if data == "reg":
                pass
        except:
            break



while True:
    conn, addr = s.accept()
    all_connections.append(conn)
    print("Connected to:", addr)
    if len(all_connections) == 2:
        for conn in all_connections:
            conn.send(str.encode("ready"))
        start_new_thread(game, (all_connections[0], all_connections[1]))
        all_connections.clear()