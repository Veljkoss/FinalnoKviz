import socket
import pygame

ib = pygame.image.load("img/dblue.jpg")

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = " 192.168.56.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
        except socket.error as e:
            x = pygame.time.get_ticks()
            fnt = pygame.font.SysFont("comicsansms", 50)
            txt = fnt.render("SERVER JE PAO", True, (0, 0, 0))
            while pygame.time.get_ticks() - x < 5000 :
                win = pygame.display.set_mode((1000, 500))
                win.blit(ib, (0,0))
                win.blit(txt, (300, 220))
                pygame.display.update()



    def recv(self):
        try:
            return self.client.recv(2048).decode()
        except:
            pass
