import pygame
from pymongo import MongoClient
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
i13 = pygame.image.load("img/sound.png")
i14 = pygame.image.load("img/mute.png")

hcolors = ((219, 176, 102), (204, 153, 51), (223, 129, 35))
gcolors = ((135, 206, 250), (30, 144, 255), (65, 105, 225))

m1 = pygame.mixer.music.load("msc/seka.mp3")
m2 = pygame.mixer.music.load("msc/m1.mp3")


def quest(win2, pitanje, colors):
    crt = 0
    x = pygame.time.get_ticks()
    runn = True
    q, ans1, ans2, ans3, crtProcitano = pitanje.split(",")
    crtProcitano1 = float(crtProcitano)
    questFont = pygame.font.SysFont("comicsansms", 40)
    ansFont = pygame.font.SysFont("comicsansms", 25)
    q1 = questFont.render(q, True, (0, 0, 0))
    ans11 = ansFont.render(ans1, True, (0, 0, 0))
    ans22 = ansFont.render(ans2, True, (0, 0, 0))
    ans33 = ansFont.render(ans3, True, (0, 0, 0))

    win2.blit(q1, (100, 50))
    pygame.draw.rect(win2, colors[0], (0, 170, width, 100))
    win2.blit(ans11, (100, 200))
    win2.blit(i10, (50, 208))
    pygame.draw.rect(win2, colors[1], (0, 320, width, 100))
    win2.blit(ans22, (100, 350))
    win2.blit(i10, (50, 358))
    pygame.draw.rect(win2, colors[2], (0, 470, width, 100))
    win2.blit(ans33, (100, 500))
    win2.blit(i10, (50, 508))

    while pygame.time.get_ticks() - x < 3000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runn = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x, pos_y = pygame.mouse.get_pos()
                if 170 < pos_y < 270:
                    win2.blit(i11, (50, 208))
                    crt = 1
                if 320 < pos_y < 420:
                    win2.blit(i11, (50, 358))
                    crt = 2
                if 470 < pos_y < 570:
                    win2.blit(i11, (50, 508))
                    crt = 3
        pygame.display.update()

    if crt == crtProcitano1:
        print("TACNO")

    return runn


def gameWindow(net, backimage, colors, pitanja):
    print("Usao sam u gamewindow sa pitanjima : " + pitanja)
    running2 = True
    active = False
    x = pygame.time.get_ticks()
    i = 0
    nizPitanja = pitanja.split("/")
    print(nizPitanja[0])
    while running2:
        win2 = pygame.display.set_mode((width, height))
        win2.blit(backimage, (0, 0))
        if active:
            running2 = quest(win2, nizPitanja[i], hcolors)
            i += 1
            pygame.display.update()
        active = True
        pygame.display.update()
        if i == 3:
            running2 = False


data = ""


def dataRead(net):
    global data
    while True:
        data = net.recv()

def startWindow():

    screen = pygame.display.set_mode((500, 300))
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(int(500/2 - 100), int(300/2 - 16), 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text)
                        text = ''
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((119, 136, 153))
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.update()
        clock.tick(30)

    main()






def main():
    global data
    running = True
    n = Network()
    start_new_thread(dataRead, (n,))
    history_true = True
    geography_true = True
    cinema_true = True
    sport_true = True
    science_true = True
    trivia_true = True
    sound_true = True
    score = 0
    scoreFont = pygame.font.SysFont("comicsansms", 40)

    #pygame.mixer.music.play(-1)

    while running:
        scoreText = scoreFont.render(str(score), True, (0, 0, 0))
        win = pygame.display.set_mode((width, height))
        win.fill((119, 136, 153))
        win.blit(scoreText, (10, 10))

        win.blit(i2, (int(width / 5 + offset_x), int(height / 4 + offset_y)))

        if not history_true:
            win.blit(i8, (int(width / 5 + offset_x), int(height / 4 + offset_y)))

        win.blit(i3, (int(width / 5 * 2 + offset_x), int(height / 4 + offset_y)))

        if not geography_true:
            win.blit(i8, (int(width / 5 * 2 + offset_x), int(height / 4 + offset_y)))

        win.blit(i4, (int(width / 5 * 3 + offset_x), int(height / 4 + offset_y)))

        if not cinema_true:
            win.blit(i8, (int(width / 5 * 3 + offset_x), int(height / 4 + offset_y)))

        win.blit(i5, (int(width / 5 + offset_x), int(height / 2 + offset_y)))

        if not sport_true:
            win.blit(i8, (int(width / 5 + offset_x), int(height / 2 + offset_y)))

        win.blit(i6, (int(width / 5 * 2 + offset_x), int(height / 2 + offset_y)))

        if not science_true:
            win.blit(i8, (int(width / 5 * 2 + offset_x), int(height / 2 + offset_y)))

        win.blit(i7, (int(width / 5 * 3 + offset_x), int(height / 2 + offset_y)))

        if not trivia_true:
            win.blit(i8, (int(width / 5 * 3 + offset_x), int(height / 2 + offset_y)))

        if sound_true:
            win.blit(i13, (20, height - 80))

        if not sound_true:
            win.blit(i14, (20, height - 80))
            pygame.mixer.music.pause()


        if str(data).startswith("pokreni_history"):
            niz = data.split("::")
            pitanja = niz[1]
            gameWindow(n, i9, hcolors, pitanja)
            history_true = False

        data = ""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x, pos_y = pygame.mouse.get_pos()
                if width / 5 + offset_x + 128 > pos_x > width / 5 + offset_x and height / 4 + offset_y < pos_y < height / 4 + offset_y + 128 and history_true:
                    n.send("history")
                    # history_true = False

                if width / 5 * 2 + offset_x + 128 > pos_x > width / 5 * 2 + offset_x and height / 4 + offset_y < pos_y < height / 4 + offset_y + 128 and geography_true:
                    n.send("geography")
                    geography_true = False

                if width / 5 * 3 + offset_x + 128 > pos_x > width / 5 * 3 + offset_x and height / 4 + offset_y < pos_y < height / 4 + offset_y + 128 and cinema_true:
                    n.send("cinema")
                    cinema_true = False

                if width / 5 + offset_x + 128 > pos_x > width / 5 + offset_x and height / 2 + offset_y < pos_y < height / 2 + offset_y + 128 and sport_true:
                    n.send("sport")
                    sport_true = False

                if width / 5 * 2 + offset_x + 128 > pos_x > width / 5 * 2 + offset_x and height / 2 + offset_y < pos_y < height / 2 + offset_y + 128 and science_true:
                    n.send("science")
                    science_true = False

                if width / 5 * 3 + offset_x + 128 > pos_x > width / 5 * 3 + offset_x and height / 2 + offset_y < pos_y < height / 2 + offset_y + 128 and trivia_true:
                    n.send("trivia")
                    trivia_true = False

                if 20 < pos_x < 52 and height - 80 < pos_y < height - 80 +32:
                    if sound_true:
                        sound_true = False
                        pygame.mixer.music.pause()

                    elif not sound_true:
                        sound_true = True
                        pygame.mixer.music.unpause()

        pygame.display.update()


#main()
startWindow()