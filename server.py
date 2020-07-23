import socket
from _thread import *
from random import randint
from pymongo import MongoClient
import time

client = MongoClient('mongodb://localhost:27017/')
db = client["quiz_database"]
history_questions = db["history_questions"]
geography_questions = db["geography_questions"]
sport_questions = db["sport_questions"]
cinema_questions = db["cinema_questions"]
science_questions = db["science_questions"]
trivia_questions = db["trivia_questions"]
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
        rnd = randint(1, 10)
        while rnd in izabrani:
            rnd = randint(1,10)


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
    odigraneIgre = []
    sveIgre = ["history", "geography", "cinema", "sport", "science", "trivia"]
    preostaleIgre = []
    while True:
        try:
            data = conn1.recv(2048).decode()
            if data == "history":
                odigraneIgre.append("history")
                reply = readFromMongo(history_questions)
                for c in game_connections:
                    c.sendall(str.encode("pokreni_history::" + reply))
                print(reply)
                continue

            if data == "geography":
                odigraneIgre.append("geography")
                reply = readFromMongo(geography_questions)
                for c in game_connections:
                    c.sendall(str.encode("pokreni_geography::" + reply))
                print(reply)
                continue

            if data == "cinema":
                odigraneIgre.append("cinema")
                reply = readFromMongo(cinema_questions)
                for c in game_connections:
                    c.sendall(str.encode("pokreni_cinema::" + reply))
                print(reply)
                continue

            if data == "sport":
                odigraneIgre.append("sport")
                reply = readFromMongo(sport_questions)
                for c in game_connections:
                    c.sendall(str.encode("pokreni_sport::" + reply))
                print(reply)
                continue

            if data == "science":
                odigraneIgre.append("science")
                reply = readFromMongo(science_questions)
                for c in game_connections:
                    c.sendall(str.encode("pokreni_science::" + reply))
                print(reply)
                continue

            if data == "trivia":
                odigraneIgre.append("trivia")
                reply = readFromMongo(trivia_questions)
                for c in game_connections:
                    c.sendall(str.encode("pokreni_trivia::" + reply))
                print(reply)
                continue

            if data == "fin":
                print("PRIMIO FINNNNNNNN")
                conn2.send(str.encode("turn"))
                time.sleep(0.500)
                continue

            if str(data).startswith("Score:"):
                score = int(str(data).split(":")[1])
                conn2.send(str.encode(data))
                time.sleep(.500)
                continue

            if str(data).startswith("name:"):
                playerName = str(data).split(':')[1]
                conn2.send(str.encode(data))
                continue

            if str(data).startswith("zavrsio"):
                s2 = str(data).split('/')
                preostaleIgre.append(s2[1])
                preostaleIgre.append(s2[2])

                rnd1 = randint(0,1)
                s = preostaleIgre[rnd1]
                if s == "history":
                    reply = readFromMongo(history_questions)
                elif s == "geography":
                    reply = readFromMongo(geography_questions)
                elif s == "cinema":
                    reply = readFromMongo(cinema_questions)
                elif s == "sport":
                    reply = readFromMongo(sport_questions)
                elif s == "science":
                    reply = readFromMongo(science_questions)
                if s == "trivia":
                    reply = readFromMongo(trivia_questions)

                for igra in preostaleIgre:
                    print(igra)

                s1 = "pokreni_" + s + "::" + reply
                print("SALJEEEEEEEM:      " + s1)
                time.sleep(0.800)
                for c in game_connections:
                    c.sendall(str.encode(s1))

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
    for player in pl:
        if playerName == player["name"]:
            players.update_one({ "_id": player["_id"]}, { "$set": {"score": int(player["score"]) + score}})



    print("Lost connection")
    conn.close()


def logHandler(conn):
    global all_connections
    uspesno = False
    logActive = True

    while logActive:
        try:
            registr = False
            data = conn.recv(2048).decode()
            pl = players.find()
            if str(data).startswith("log"):
                user = str(data).split("/")[1].split(":")[0]
                password = str(data).split("/")[1].split(":")[1]
                for player in pl:
                    if user == player["name"] and password == player["password"]:
                        uspesno = True
                        conn.send(str.encode("logu"))
                        logActive = False
                        break
                if not uspesno:
                    conn.send(str.encode("logn"))

            if str(data).startswith("reg"):
                user = str(data).split("/")[1].split(":")[0]
                password = str(data).split("/")[1].split(":")[1]
                for player in pl:
                    if user == player["name"]:
                        conn.send(str.encode("regn"))
                        registr = True
                        break

                if not registr:
                    players.insert_one({"name": user, "password": password, "score": 0})
                    conn.send(str.encode("regu"))

        except:
            break

    if uspesno:
        all_connections.append(conn)

    if len(all_connections) == 2:
        time.sleep(.500)

        for conn in all_connections:
            try:
                conn.send(str.encode("test"))
            except:
                all_connections.remove(conn)

        if len(all_connections) == 2:
            all_connections[0].send(str.encode("prvi"))
            time.sleep(0.500)
            for conn in all_connections:
                conn.send(str.encode("ready"))
            start_new_thread(game, (all_connections[0], all_connections[1]))
            all_connections.clear()
    return


while True:
    conn, addr = s.accept()
    start_new_thread(logHandler, (conn,))
    #all_connections.append(conn)
    print("Connected to:", addr)
