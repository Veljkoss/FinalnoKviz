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

server = "192.168.0.30"
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
            rnd = randint(1, 10)

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
    global all_connections
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
                reply = readFromMongo(history_questions)
                for c in game_connections:
                    c.sendall(str.encode("pokreni_history::" + reply))
                print(reply)
                continue

            if data == "geography":
                reply = readFromMongo(geography_questions)
                for c in game_connections:
                    c.sendall(str.encode("pokreni_geography::" + reply))
                print(reply)
                continue

            if data == "cinema":
                reply = readFromMongo(cinema_questions)
                for c in game_connections:
                    c.sendall(str.encode("pokreni_cinema::" + reply))
                print(reply)
                continue

            if data == "sport":
                reply = readFromMongo(sport_questions)
                for c in game_connections:
                    c.sendall(str.encode("pokreni_sport::" + reply))
                print(reply)
                continue

            if data == "science":
                reply = readFromMongo(science_questions)
                for c in game_connections:
                    c.sendall(str.encode("pokreni_science::" + reply))
                print(reply)
                continue

            if data == "trivia":
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

                rnd1 = randint(0, 1)
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

            if data == "Nova igra":
                print("NOVA IGRA")
                all_connections.append(conn1)
                return

            if data == "revans":
                conn2.send(str.encode("revans"))
                continue

            if data == "izasao":
                conn2.send(str.encode("izasao"))
                conn.close()
                return

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
            players.update_one({"_id": player["_id"]}, {"$set": {"score": int(player["score"]) + score}})

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

    if len(all_connections) > 1:
        time.sleep(.500)

        for conn in all_connections:
            try:
                conn.send(str.encode("test"))
            except:
                all_connections.remove(conn)

        if len(all_connections) > 1:
            i = -1
            for conn in all_connections:
                i += 1

            print(i)
            first = randint(0, i)
            all_connections[first].send(str.encode("prvi"))
            time.sleep(0.800)
            conn1 = all_connections[first]
            all_connections.remove(conn1)
            second = randint(0, i - 1)
            conn2 = all_connections[second]
            all_connections.remove(conn2)
            conn1.send(str.encode("ready"))
            conn2.send(str.encode("ready"))
            start_new_thread(game, (conn1, conn2))


            # all_connections[0].send(str.encode("prvi"))
            # time.sleep(0.500)
            # conn1 = all_connections[0]
            # conn2 = all_connections[1]
            # all_connections.clear()
            # conn1.send(str.encode("ready"))
            # conn2.send(str.encode("ready"))

            # for conn in all_connections:
            #    conn.send(str.encode("ready"))
            # start_new_thread(game, (conn1, conn2))
            # all_connections.clear()

    return


def main():
    while True:
        conn, addr = s.accept()
        start_new_thread(logHandler, (conn,))
        print("Connected to:", addr)


main()
