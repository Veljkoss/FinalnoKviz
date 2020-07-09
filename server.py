import socket
from _thread import *
from pymongo import MongoClient



client = MongoClient('mongodb://localhost:27017/')
db = client["quiz_datebase"]
history_questions = db["history_questions"]






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

def readFromMongo(type):

    str = ""

    for i in range(3):
        rnd = randint(1, 3)
        result = type.find_one({"_id": rnd})
        quest = result["quest"]
        ans1 = result["ans1"]
        ans2 = result["ans2"]
        ans3 = result["ans3"]

        str = str + quest + ',' + ans1 + ',' + ans2 + ',' + ans3 + ',' + result["crt"] + '/'

    return str






def threaded_client(conn, player):
    while True:
        try:
            data = conn.recv(2048).decode()

            if data == "historyActive":
                reply = readFromMongo(history_questions)
                for c in all_connections:
                    c.sendall(str.encode(reply))
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
