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
i7 = pygame.image.load("img/quizq.png")
i8 = pygame.image.load("img/cross.png")
i9 = pygame.image.load("img/h1.jpg")
i10 = pygame.image.load("img/circle.png")
i11 = pygame.image.load("img/right.png")
i12 = pygame.image.load("img/globeback.jpg")
i13 = pygame.image.load("img/sound.png")
i14 = pygame.image.load("img/mute.png")
i15 = pygame.image.load("img/loading.png")
i16 = pygame.image.load("img/loading1.png")
i17 = pygame.image.load("img/enter.png")
i18 = pygame.image.load("img/patient.png")
i19 = pygame.image.load("img/dblue.jpg")
i20 = pygame.image.load("img/movieback2.jpg")
i21 = pygame.image.load("img/sportback1.jpg")
i22 = pygame.image.load("img/scienceback.jpg")
i23 = pygame.image.load("img/triviaback.jpg")
i24 = pygame.image.load("img/switchon.png")
i25 = pygame.image.load("img/switchoff.png")
i26 = pygame.image.load("img/one (1).png")
i27 = pygame.image.load("img/two (1).png")
i28 = pygame.image.load("img/three (1).png")
i29 = pygame.image.load("img/four (1).png")
i30 = pygame.image.load("img/five (1).png")
i31 = pygame.image.load("img/stop.png")
i32 = pygame.image.load("img/revans.png")
i33 = pygame.image.load("img/new.png")



hcolors = ((219, 176, 102), (204, 153, 51), (223, 129, 35))
gcolors = ((135, 206, 250), (30, 144, 255), (65, 105, 225))
scolors = ((169,169,169), (128,128,128),(105,105,105))
mcolors = ((255,245,238), (255,239,213), (255,228,225))
spcolors = ((233,150,122), (255,127,80), (255,99,71))
tcolors = ((175,238,238), (72,209,204), (95,158,160))


score1 = 0
score2 = 0
p1Name = ""
p2Name = ""
password = ""
running = True
running1 = True
novaIgra = False
data = ""
x = 0
brojIgara = 0
#m1 = pygame.mixer.music.load("msc/seka.mp3")
m2 = pygame.mixer.music.load("msc/m1.mp3")
pygame.display.set_caption("KvizRMT")

def quest(win2, pitanje, colors):
    global score1
    global score2
    global x
    global brojIgara
    crt = 0
    t = pygame.time.get_ticks()
    runn = True
    q, ans1, ans2, ans3, crtProcitano = pitanje.split(",")
    crtProcitano1 = float(crtProcitano)
    questFont = pygame.font.SysFont("comicsansms", 40)
    ansFont = pygame.font.SysFont("comicsansms", 25)
    timerFont = pygame.font.SysFont("comicsansms", 25)
    q1 = questFont.render(q, True, (0, 0, 0))
    ans11 = ansFont.render(ans1, True, (0, 0, 0))
    ans22 = ansFont.render(ans2, True, (0, 0, 0))
    ans33 = ansFont.render(ans3, True, (0, 0, 0))
    scr = 0
    odgovoreno = False
    kraj = False
    gdeJeX = 0

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

    while pygame.time.get_ticks() - t < 6000:
        if 6000 - pygame.time.get_ticks() + t > 5000:
            win2.blit(i30, (920, 70))
        elif 6000 - pygame.time.get_ticks() + t > 4000:
            win2.blit(i29, (920, 70))
        elif 6000 - pygame.time.get_ticks() + t > 3000:
            win2.blit(i28, (920, 70))
        elif 6000 - pygame.time.get_ticks() + t > 2000:
            win2.blit(i27, (920, 70))
        elif 6000 - pygame.time.get_ticks() + t > 1000:
            win2.blit(i26, (920, 70))
        elif 6000 - pygame.time.get_ticks() + t > 0:
            win2.blit(i31, (920, 70))
            if crtProcitano1 == 1:
                pygame.draw.rect(win2, (50,205,50), (0, 170, width, 100))
                win2.blit(ans11, (100, 200))
                win2.blit(i10, (50, 208))
            if crtProcitano1 == 2:
                pygame.draw.rect(win2, (50,205,50), (0, 320, width, 100))
                win2.blit(ans22, (100, 350))
                win2.blit(i10, (50, 358))
            if crtProcitano1 == 3:
                pygame.draw.rect(win2, (50,205,50), (0, 470, width, 100))
                win2.blit(ans33, (100, 500))
                win2.blit(i10, (50, 508))


            if gdeJeX == 1:
                win2.blit(i11, (50, 208))
            if gdeJeX == 2:
                win2.blit(i11, (50, 358))
            if gdeJeX == 3:
                win2.blit(i11, (50, 508))

            kraj = True

        for event in pygame.event.get():
            if not kraj:
                if event.type == pygame.QUIT:
                    runn = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos_x, pos_y = pygame.mouse.get_pos()
                    if 170 < pos_y < 270 and not odgovoreno:
                        win2.blit(i11, (50, 208))
                        crt = 1
                        gdeJeX = 1
                        odgovoreno = True
                    if 320 < pos_y < 420 and not odgovoreno:
                        win2.blit(i11, (50, 358))
                        crt = 2
                        gdeJeX = 2
                        odgovoreno = True
                    if 470 < pos_y < 570 and not odgovoreno:
                        win2.blit(i11, (50, 508))
                        crt = 3
                        gdeJeX = 3
                        odgovoreno = True

        pygame.display.update()

    if crt != 0:
        if crt == crtProcitano1:
            if brojIgara != 4:
                if x % 2 == 1:
                    score1 += 2
                else:
                    score1 += 1
            else:
                score1 += 3
        else:
            if brojIgara != 4:
                if x % 2 == 1:
                    score1 -= 2
                else:
                    score1 -= 1
            else:
                score1 -= 3
    return runn

def gameWindow(net, backimage, colors, pitanja):
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
            running2 = quest(win2, nizPitanja[i], colors)
            i += 1
            pygame.display.update()
        active = True
        pygame.display.update()
        if i == 3:
            running2 = False

    net.send("Score:" + str(score1))

def dataRead(net):
    global data
    while True:
        data = net.recv()
        if data == "logu":
            print(str(data))
        if data == "logn":
            print(str(data))

def startWindow():
    n = Network()
    start_new_thread(dataRead, (n,))

    global data
    data = ""
    global p1Name
    global password
    global running
    global running1
    screen = pygame.display.set_mode((500, 300))
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(int(500/2 - 100), int(300/2 - 80), 140, 32)
    input_box1 = pygame.Rect(int(500/2 - 100), int(300/2 - 40), 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    text1 = ''
    done = False
    active1 = False
    color1 = color_inactive
    neuspesanLogin = False
    uspesnaRegistracija = False
    neuspesnaRegistracija = False
    state = 0


    while not done:
        if data == "logu":
            break
        if data == "logn":
            state = 1

        if data == "regu":
            state = 2

        if data == "regn":
            state = 3



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                running1 = False
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):

                    active = not active
                else:
                    active = False

                if input_box1.collidepoint(event.pos):

                    active1 = not active
                else:
                    active1 = False

                color = color_active if active else color_inactive
                color1 = color_active if active1 else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

                if active1:
                    if event.key == pygame.K_BACKSPACE:
                        text1 = text1[:-1]
                    else:
                        text1 += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x, pos_y = pygame.mouse.get_pos()
                if 198 < pos_x < 230 and 175 < pos_y < 207:
                    p1Name = text
                    print(p1Name)
                    password = text1
                    print(password)
                    n.send("log/" + p1Name + ":" + password)

                if 270 < pos_x < 302 and 175 < pos_y < 207:
                    p1Name = text
                    password = text1
                    n.send("reg/" + p1Name + ":" + password)

        screen.blit(i19, (0, 0))
        txt_surface = font.render(text, True, color)
        txt_surface1 = font.render("*" * len(text1), True, color)
        txt_surface2 = font.render("Neispravan username/lozinka!", True, (178, 34, 34))
        txt_surface3 = font.render("Uspesno ste se registrovali!", True, (50,205,50))
        txt_surface4 = font.render("Korisnicko ime je zauzeto!", True, (178, 34, 34))



        if state == 1:
            screen.blit(txt_surface2, (85 ,250))

        if state == 2:
            screen.blit(txt_surface3, (85 ,250))

        if state == 3:
            screen.blit(txt_surface4, (85, 250))



        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        input_box1.w = width

        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        screen.blit(txt_surface1, (input_box1.x+5, input_box1.y+5))
        screen.blit(i17, (218 - 20, 175))
        screen.blit(i18, (250 + 20, 175))


        pygame.draw.rect(screen, color, input_box, 2)
        pygame.draw.rect(screen, color1, input_box1, 2)
        pygame.display.update()
        clock.tick(30)

    main(n)

def endWindow(n):
    global p1Name
    global p2Name
    global data
    global running
    global score1
    scoreFont = pygame.font.SysFont("comicsansms", 40)
    winFont = pygame.font.SysFont("", 64)
    global score2
    running2 = True
    revans = False
    global x
    global brojIgara
    score1Text = scoreFont.render(p1Name + ":" + str(score1), True, (0, 0, 0))
    score2Text = scoreFont.render(p2Name + ":" + str(score2), True, (0, 0, 0))
    domacin = score1 > score2

    while running2:
        win = pygame.display.set_mode((width, height))


        if domacin:
            win.blit(i19, (0, 0))
            win.blit(i32, (400, 320))
            win.blit(i33, (536, 320))
            win.blit(score1Text, (20, 10))
            win.blit(score2Text, (950 - len(p2Name) * 20, 10))
            txt = scoreFont.render("Pobeda", True, (0,0,0))
            win.blit(txt, (450, 150))
        else:
            win.blit(i19, (0, 0))
            win.blit(i32, (400, 320))
            win.blit(i33, (536, 320))
            win.blit(score1Text, (20, 10))
            win.blit(score2Text, (950 - len(p2Name) * 20, 10))
            txt = scoreFont.render("Poraz", True, (0,0,0))
            win.blit(txt, (450, 150))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running2 = False
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x, pos_y = pygame.mouse.get_pos()
                if 400 < pos_x < 464 and 320 < pos_y < 384:
                    n.send("revans")
                    if str(data) == "revans":
                        revans = True
                    x = pygame.time.get_ticks()
                    while pygame.time.get_ticks() - x < 5000:
                        if revans:
                            running2 = False
                            break
                        if str(data) == "revans":
                            revans = True


                if 536 < pos_x < 600 and 320 < pos_y < 384:
                    running2 = False
                    x = 0
                    brojIgara = 0
                    score1 = 0
                    score2 = 0
                    startWindow()
                    #n = Network()
                    #main(n)

        pygame.display.update()

def main(n):
    global novaIgra
    global p1Name
    global p2Name
    global data
    global running
    #n = Network()
    #start_new_thread(dataRead, (n,))
    history_true = True
    geography_true = True
    cinema_true = True
    sport_true = True
    science_true = True
    trivia_true = True
    sound_true = True
    global score1
    scoreFont = pygame.font.SysFont("comicsansms", 40)
    global score2
    turn = True
    i = 0
    #pygame.mixer.music.play(-1)
    j = 0
    global x
    global brojIgara
    prvi = False
    global running1
    zavrseneIgre = 0
    novaIgra = True

    while running1:
        win = pygame.display.set_mode((width, height))
        win.blit(i19, (0,0))
        #win.fill((119, 136, 153))
        txt = scoreFont.render("Povezivanje sa drugim igracem...", True, (0,0,0))
        win.blit(txt, (100, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running1 = False
                running = False

        if j % 2 == 0:
            win.blit(i15, (450, 300))
        else:
            win.blit(i16, (450, 300))
        pygame.display.update()

        pygame.time.wait(500)
        j = j + 1
        if data == "prvi":
            x = 1
            prvi = True

        if data == "ready":
            break

    pygame.time.wait(500)
    n.send("name:" + p1Name)
    pygame.time.wait(500)
    if str(data).startswith("name:"):
        print("Primio:" + str(data).split(':')[1])
        p2Name = str(data).split(':')[1]



    print(x)
    print("data je: " + str(data))

    data = ""
    while running:
        score1Text = scoreFont.render(p1Name + ":" + str(score1), True, (0, 0, 0))
        score2Text = scoreFont.render(p2Name + ":" + str(score2), True, (0, 0, 0))
        win = pygame.display.set_mode((width, height))
        win.blit(i19, (0,0))
        #win.fill((119, 136, 153))
        win.blit(score1Text, (20, 10))
        win.blit(score2Text, (950 - len(p2Name) * 20 - 20, 10))


        if x % 2 == 1 or x == 1:
            turn = True

        if zavrseneIgre == 5:
            print("ZAVRSENOOOO")
            endWindow(n)
            history_true = True
            geography_true = True
            cinema_true = True
            sport_true = True
            science_true = True
            trivia_true = True
            sound_true = True

            if prvi:
                prvi = False
                x = 0
            else:
                prvi = True
                x = 1

            score1 = 0
            score2 = 0

            brojIgara = 0
            zavrseneIgre = 0


        if brojIgara == 4 and prvi:
            s = "zavrsio"
            if history_true:
                s += "/history"
            if geography_true:
                s += "/geography"
            if cinema_true:
                s += "/cinema"
            if sport_true:
                s += "/sport"
            if science_true:
                s += "/science"
            if trivia_true:
                s += "/trivia"
            n.send(s)
            brojIgara += 1

        if brojIgara >= 4:
            turn = False

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

        if brojIgara != 4:
            if x % 2 == 1:
                win.blit(i24, (484,20))
            else:
                win.blit(i25, (484,20))
        else:
            win.blit(i25, (484, 20))

        if str(data).startswith("pokreni_history"):
            niz = data.split("::")
            pitanja = niz[1]
            gameWindow(n, i9, hcolors, pitanja)
            history_true = False

        if str(data).startswith("pokreni_geography"):
            niz = data.split("::")
            pitanja = niz[1]
            gameWindow(n, i12, gcolors, pitanja)
            geography_true = False

        if str(data).startswith("pokreni_cinema"):
            niz = data.split("::")
            pitanja = niz[1]
            gameWindow(n, i20, mcolors, pitanja)
            cinema_true = False


        if str(data).startswith("pokreni_sport"):
            niz = data.split("::")
            pitanja = niz[1]
            gameWindow(n, i21, spcolors, pitanja)
            sport_true = False

        if str(data).startswith("pokreni_science"):
            niz = data.split("::")
            pitanja = niz[1]
            gameWindow(n, i22, scolors, pitanja)
            science_true = False

        if str(data).startswith("pokreni_trivia"):
            niz = data.split("::")
            pitanja = niz[1]
            gameWindow(n, i23, tcolors, pitanja)
            trivia_true = False




        if str(data).startswith("Score:"):
            score = str(data).split(":")[1]
            print("primio: " + str(score))
            score2 = int(score)
            x += 1
            brojIgara += 1
            zavrseneIgre += 1
            turn = False

        if str(data) == "izasao":
            t = pygame.time.get_ticks()
            fnt = pygame.font.SysFont("comicsansms", 40)
            txt = fnt.render("PROTIVNIK JE NAPUSTIO IGRU", True, (0, 0, 0))
            while pygame.time.get_ticks() - t < 5000 :
                win = pygame.display.set_mode((1000, 500))
                win.blit(i19, (0,0))
                win.blit(txt, (300, 220))
                pygame.display.update()
            x = 0
            brojIgara = 0
            score1 = 0
            score2 = 0
            startWindow()
            break



        data = ""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                n.send("izasao")
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x, pos_y = pygame.mouse.get_pos()
                if 0 < pos_x < 50 and 0 < pos_y < 50:
                    print(turn)
                    print(x)
                    print(history_true)
                    print(brojIgara)
                    print(data)
                if width / 5 + offset_x + 128 > pos_x > width / 5 + offset_x and height / 4 + offset_y < pos_y < height / 4 + offset_y + 128 and history_true and turn:
                    n.send("history")
                    i = 1

                if width / 5 * 2 + offset_x + 128 > pos_x > width / 5 * 2 + offset_x and height / 4 + offset_y < pos_y < height / 4 + offset_y + 128 and geography_true and turn:
                    n.send("geography")
                    i = 1


                if width / 5 * 3 + offset_x + 128 > pos_x > width / 5 * 3 + offset_x and height / 4 + offset_y < pos_y < height / 4 + offset_y + 128 and cinema_true and turn:
                    n.send("cinema")
                    i = 1

                if width / 5 + offset_x + 128 > pos_x > width / 5 + offset_x and height / 2 + offset_y < pos_y < height / 2 + offset_y + 128 and sport_true and turn:
                    n.send("sport")
                    i = 1

                if width / 5 * 2 + offset_x + 128 > pos_x > width / 5 * 2 + offset_x and height / 2 + offset_y < pos_y < height / 2 + offset_y + 128 and science_true and turn:
                    n.send("science")
                    i = 1

                if width / 5 * 3 + offset_x + 128 > pos_x > width / 5 * 3 + offset_x and height / 2 + offset_y < pos_y < height / 2 + offset_y + 128 and trivia_true and turn:
                    n.send("trivia")
                    i = 1

                if 20 < pos_x < 52 and height - 80 < pos_y < height - 80 + 32:
                    if sound_true:
                        sound_true = False
                        pygame.mixer.music.pause()

                    elif not sound_true:
                        sound_true = True
                        pygame.mixer.music.unpause()


        pygame.display.update()

startWindow()
