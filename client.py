import pygame
#from pymongo import MongoClient
from network import Network
from _thread import *

pygame.init()

width = 1000
height = 600
offset_x = (width / 5 - 128) / 2
offset_y = (height / 4 - 128) / 2
black = (255, 255, 255)


i2 = pygame.image.load("img/h2.png")
i3 = pygame.image.load("img/globe.png")
i4 = pygame.image.load("img/cinema.png")
i5 = pygame.image.load("img/basketball.png")
i6 = pygame.image.load("img/science.png")
i7 = pygame.image.load("img/quiz.png")
i8 = pygame.image.load("img/cross.png")
i9 = pygame.image.load("img/h1.jpg")
i10 = pygame.image.load("img/circle.png")
i11 = pygame.image.load("img/right.png")
i12 = pygame.image.load("img/globeback.jpg")



hcolors = ((219,176,102), (204,153,51), (223,129,35))
gcolors = ((135,206,250), (30,144,255), (65,105,225))


def gameWindow(net, backimage, colors):
    running2 = True
    active = False
    x = pygame.time.get_ticks()
    i = 0
    while running2:
        win2 = pygame.display.set_mode((width, height))
        win2.blit(backimage, (0, 0))
        if active:
            pygame.display.update()
        active = True
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running2 = False
        if pygame.time.get_ticks() - x > 5000:
            running2 = False





data = ""

def dataRead(net):
    global data
    while True:
        data = net.recv()







def main():
    global data
    running = True
    n = Network()
    start_new_thread(dataRead,(n,))
    history_true = True
    geography_true = True
    cinema_true = True
    sport_true = True
    science_true = True
    trivia_true = True
    score = 0
    scoreFont = pygame.font.SysFont("comicsansms", 40)

    while running:
        scoreText = scoreFont.render(str(score), True, (0, 0, 0))
        win = pygame.display.set_mode((width, height))
        win.fill((119, 136, 153))
        win.blit(scoreText, (10, 10))
        if history_true:
            win.blit(i2, (int(width / 5 + offset_x), int(height / 4 + offset_y)))
        else:
            win.blit(i2, (int(width / 5 + offset_x), int(height / 4 + offset_y)))
            win.blit(i8, (int(width / 5 + offset_x), int(height / 4 + offset_y)))

        if geography_true:
            win.blit(i3, (int(width / 5 * 2 + offset_x), int(height / 4 + offset_y)))
        else:
            win.blit(i3, (int(width / 5 * 2 + offset_x), int(height / 4 + offset_y)))
            win.blit(i8, (int(width / 5 * 2 + offset_x), int(height / 4 + offset_y)))

        if cinema_true:
            win.blit(i4, (int(width / 5 * 3 + offset_x), int(height / 4 + offset_y)))
        else:
            win.blit(i4, (int(width / 5 * 3 + offset_x), int(height / 4 + offset_y)))
            win.blit(i8, (int(width / 5 * 3 + offset_x), int(height / 4 + offset_y)))

        if sport_true:
            win.blit(i5, (int(width / 5 + offset_x), int(height / 2 + offset_y)))
        else:
            win.blit(i5, (int(width / 5 + offset_x), int(height / 2 + offset_y)))
            win.blit(i8, (int(width / 5 + offset_x), int(height / 2 + offset_y)))

        if science_true:
            win.blit(i6, (int(width / 5 * 2 + offset_x), int(height / 2 + offset_y)))
        else:
            win.blit(i6, (int(width / 5 * 2 + offset_x), int(height / 2 + offset_y)))
            win.blit(i8, (int(width / 5 * 2 + offset_x), int(height / 2 + offset_y)))

        if trivia_true:
            win.blit(i7, (int(width / 5 * 3 + offset_x), int(height / 2 + offset_y)))
        else:
            win.blit(i7, (int(width / 5 * 3 + offset_x), int(height / 2 + offset_y)))
            win.blit(i8, (int(width / 5 * 3 + offset_x), int(height / 2 + offset_y)))

        if data == "history":
            gameWindow(n, i9, hcolors)

        data = ""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x, pos_y = pygame.mouse.get_pos()
                if pos_x < width / 5 + offset_x + 128 and pos_x > width / 5 + offset_x and pos_y > height / 4 + offset_y and pos_y < height / 4 + offset_y + 128 and history_true:
                    n.send("history")
                    history_true = False

                if pos_x < width / 5 * 2 + offset_x + 128 and pos_x > width / 5 * 2 + offset_x and pos_y > height / 4 + offset_y and pos_y < height / 4 + offset_y + 128 and geography_true:
                    n.send("geography")
                    geography_true = False

                if pos_x < width / 5 * 3 + offset_x + 128 and pos_x > width / 5 * 3 + offset_x and pos_y > height / 4 + offset_y and pos_y < height / 4 + offset_y + 128 and cinema_true:
                    n.send("cinema")
                    cinema_true = False

                if pos_x < width / 5 + offset_x + 128 and pos_x > width / 5 + offset_x and pos_y > height / 2 + offset_y and pos_y < height / 2 + offset_y + 128 and sport_true:
                    n.send("sport")
                    sport_true = False

                if pos_x < width / 5 * 2 + offset_x + 128 and pos_x > width / 5 * 2 + offset_x and pos_y > height / 2 + offset_y and pos_y < height / 2 + offset_y + 128 and science_true:
                    n.send("science")
                    science_true = False

                if pos_x < width / 5 * 3 + offset_x + 128 and pos_x > width / 5 * 3 + offset_x and pos_y > height / 2 + offset_y and pos_y < height / 2 + offset_y + 128 and trivia_true:
                    n.send("trivia")
                    trivia_true = False

        pygame.display.update()


main()