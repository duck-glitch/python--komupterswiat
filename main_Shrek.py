import pygame    #importujemy biblioteke do tworzenia gier
import os
import random
import math
from time import sleep

pygame.init()       #niezbedne do dzialania modulu pygame, inicjujemy jego dzialanie

szer = 800                 #definiujemy szerokosc okna gry
wys = 650                 #definiujemy wysokosc okna gry
screen = pygame.display.set_mode( (szer, wys) )              #nasze okno graficzne gry


def napisz(tekst, x, y, rozmiar ):                                                     #funkcja wyswietlania tekstu
    cz = pygame.font.SysFont("Arial", rozmiar)              #czcionka, ktorej uzyjemy podczas wypisania tekstu
    rend = cz.render(tekst, 1, (100, 255, 100))                   #tworzymy obiekt - tekst [1-wygladzenie tekstu, 0-nie, kolor RGB]
    #x = (szer - rend.get_rect().width) /2       srodek        #tzw 600 - prostokat potrzebny na tekst /2 daje nam srodek ekranu
    #y = (wys - rend.get_rect().height) /2      ekranu        #x i y to wspolrzedne w pikselach gdzie bedzie wyswietlony tekst
    screen.blit(rend, (x, y) )                                                         #umieszcza wyrenderowany tekst w oknie graficznym [o wsp (x,y)]



copokazuje = "menu"
if copokazuje == "menu":
    sound = pygame.mixer.Sound('s1my_swamp.wav')
    sound.play()
    


class Przeszkoda():
    def __init__(self, x, szerokosc):
        self.x = x
        self.szerokosc = szerokosc
        self.y_gora = 0
        self.wys_gora = random.randint(150,250)
        self.odstep = 180
        self.y_dol = self.wys_gora + self.odstep
        self.wys_dol = wys - self.y_dol
        self.kolor = (120,60,10)
        self.ksztalt_gora = pygame.Rect(self.x, self.y_gora, self.szerokosc, self.wys_gora)
        self.ksztalt_dol = pygame.Rect(self.x, self.y_dol, self.szerokosc, self.wys_dol)

    def rysuj(self):
        pygame.draw.rect(screen, self.kolor, self.ksztalt_gora, 3)   #0-grubosc krawedzi prostokata
        pygame.draw.rect(screen, self.kolor, self.ksztalt_dol, 3)

    def ruch(self, v):
        self.x = self.x - v
        self.ksztalt_gora = pygame.Rect(self.x, self.y_gora, self.szerokosc, self.wys_gora)
        self.ksztalt_dol = pygame.Rect(self.x, self.y_dol, self.szerokosc, self.wys_dol)

    def kolizja(self, player):
        if self.ksztalt_gora.colliderect(player) or self.ksztalt_dol.colliderect(player):
            return True
        else:
            return False


        
class Kitku():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wysokosc = 50
        self.szerokosc = 35
        self.ksztalt = pygame.Rect(self.x, self.y, self.szerokosc, self.wysokosc)
        self.grafika = pygame.image.load(os.path.join('p3kitku_najezdzca.png'))
        
    def rysuj(self):
        screen.blit(self.grafika, (self.x, self.y) )

    def ruch(self, v):
        self.y = self.y + v
        self.ksztalt = pygame.Rect(self.x, self.y, self.szerokosc, self.wysokosc)
        


przeszkody = []
for i in range(21):
    przeszkody.append(Przeszkoda(i * szer/20, szer/20))

gracz = Kitku(250,275)

dy = 0
tablica = []
global flaga
global flaga2
flaga = 1
flaga2 = 1


        
while True:                                                                                            #Glowna petla gry
    for event in pygame.event.get():                                        #sprawdzamy eventy czyli klikniecia ruch myszka itp
        if event.type == pygame.QUIT:                                          #jezeli gracz nacisnie 'x' zeby zamknac okno gry
            pygame.quit()                                                                         #okno graficzne sie zamknie
            quit()                                                                                             #oraz idle
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            if event.key == pygame.K_UP:
                dy = -0.1
            if event.key == pygame.K_DOWN:
                dy = 0.1
            if event.key == pygame.K_SPACE:
                if copokazuje == "zasady":
                    gracz = Kitku(250,275)
                    dy = 0
                    copokazuje = "rozgrywka"
                    punkty = 0
                if copokazuje == "menu":
                    copokazuje = "zasady"
                #if copokazuje == "rozgrywka":
                    #copokazuje = "koniec"
                if copokazuje == "koniec":
                    gracz = Kitku(250,275)
                    dy = 0
                    copokazuje = "rozgrywka"
                    punkty = 0
        

    screen.fill( (0, 0, 0) )
    if copokazuje == "menu":
        napisz( "Nacisnij spacje, aby kontynuowac", 235, 590, 24)        #wypisanie tekstu- parametry[tekst, wsp oraz rozmiar]
        napisz("copyright", 6, 18, 14)
        napisz("by ", 20, 36, 14)
        napisz("D&P", 16, 54, 15)
        napisz("kitku w", 6, 72, 14)
        napisz("grocie nestle", 6, 90, 14)
        napisz("17.05.2020", 6, 108, 14)
        napisz("03:23- koniec", 6, 126, 14)
        grafika = pygame.image.load(os.path.join('p1logo.png'))
        screen.blit(grafika, (74, 10))
        grafikasound = pygame.image.load(os.path.join('p0soundon.png'))
        screen.blit(grafikasound, (618, 180))
        grafika01 = pygame.image.load(os.path.join('p01text.png'))
        screen.blit(grafika01, (546, 10))

    elif copokazuje == "zasady":
        grafika_zasady = pygame.image.load(os.path.join('p2zasady.png'))
        screen.blit(grafika_zasady, (0, 0))
        if flaga == 1:
            pygame.mixer.music.load('s2zasady.wav')
            pygame.mixer.music.play()
            flaga = flaga - 1
        
        
            
        
    elif copokazuje == "rozgrywka":
        for p in przeszkody:
            p.ruch(1)
            p.rysuj()
            if p.kolizja(gracz.ksztalt):
                pygame.mixer.music.load('s3laught.wav')
                pygame.mixer.music.play(0)
                grafika3 = pygame.image.load(os.path.join('p4shreku.png'))
                screen.blit(grafika3, (275, 275) )
                napisz("TO MOJE BAGNO!", 350, 280, 20)
                copokazuje = "koniec"
        for p in przeszkody:
            if p.x <= -p.szerokosc:
                przeszkody.remove(p)
                przeszkody.append( (Przeszkoda(szer, szer/20) ))
                punkty = int(punkty + int(10 * math.fabs(dy)))
        gracz.rysuj()
        gracz.ruch(dy)
        napisz("Score: " + str(punkty), 50, 50, 20)

    elif copokazuje == "koniec":
        if punkty not in tablica:
            tablica.append(punkty)
        grafika = pygame.image.load(os.path.join('p5koniec.png'))
        screen.blit(grafika, (0, 0))
        napisz("Shrek Cie dopadł !!!", 425, 490, 50)
        napisz("Nacisnij spacje, aby zagrac ponownie", 440, 600, 25)
        napisz("Gra wlaczy sie 3s po nacisnieciu spacji", 480, 630, 16)
        grafika2 = pygame.image.load(os.path.join('p6kosci.png'))
        screen.blit(grafika2, (0, 456))
        napisz("Twoj wynik = " + str(punkty), 16,370, 35)
        napisz("Rekord: [ " + str(max(tablica)) + " ]", 580,370, 35)
        sleep(3)
        
        


    pygame.display.update()                                       #wprowadzamy w zycie zmiany- odswiezamy okno gry
    
        
    

                                                                             ###TO DO###
               
                                                           # zwiekszyc poziom trudnosci
                                                           # spacja zeruje pkt



