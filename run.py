# -*- coding: utf-8 -*-
"""
Created on Sat May 26 12:29:50 2018

@author: Henry
"""
import pygame, sys, traceback
import math
import random
from pygame.locals import *
from allThings import *
from constants import *
import time

#Start pygame
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 10)
fontDisplayAttack = pygame.font.SysFont('Comic Sans MS', 30)
pygame.mixer.init()
seed = int(random.random()*1000)
random.seed(seed)
#Set FPS
FPS = 48 # frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
winHeight = 720
winWidth = 1280
dis = pygame.display.set_mode((winWidth, winHeight), 0)
pygame.display.set_caption("Conquest")  
 
finalFont = pygame.font.SysFont('Comic Sans MS', 100)

#variables
dragging = False
tiles = []
ui = []

for x in range(-10, 10):
    temp = []
    for y in range (-10, 10):
        if (x < 8 or x > 8 or y < 8 or y > 8) and random.random() < 0.2:
            continue
        else:
            temp.append(tile(x, y, 0-x-y)) 
        
    tiles.append(temp)

def addCity(depth, n, m):
    d = int((depth - 1 ) /n)
    if d < 1:
        team = MAGENTA
    elif d < 2:
        team = CYAN
    elif d < 3:
        team = LIME
    else:
        team = OLIVE
    works = True
    if depth == 0:
        return 0
    x = int(random.random()*2*m-m)
    y = int(random.random()*2*m-m)
    a = getTile(tiles, x,y)
    if not a:
        works = False
    elif len(a.contents) > 0:
        works = False
    else:
        for b in neighbors(tiles, a):
            if len(b.contents) > 0:
                works = False
    if works:
        a.color = team
        a.contents.append(city(a, team))
        a.contents.append(army(50, team))
        a.bonus += 0.5
        addCity(depth - 1, n, m)
    else:
        addCity(depth, n, m)
        
addCity(12, 3, 10)

def addMountain(tiles, x, y):
    a = getTile(tiles, x, y)
    if not a or len(a.contents) > 0:
        return 0
    else:
        a.contents.append(mountain())
        a.bonus = 0.2
        dx = 1
        dy = 1
        while(dx * dy == 1):
            dx = int(random.random()*3)-1
            dy = int(random.random()*3)-1
            addMountain(tiles, x+dx, y+dy)
        
def addMountains(tiles, n, m):
    for x in range (n):
        x = int(random.random()*2*m-m)
        y = int(random.random()*2*m-m)
        addMountain(tiles, x, y)
        
addMountains(tiles, 8, 8)
#getting mouse offset
prevX = -1
prevY = -1

#Turn Start
turnStart = True
currentPlayer = MAGENTA
scale = 1
left = False
right = False
up = False
down = False
troops = 0
attacking = False
menu = False
done = False
selection = 0
ticker = 0


#MAGENTA, CYAN, LIME, OLIVE
monies = [10000,0,0,0]
ais = [0, 0, 0, 0]
introTest = True


pygame.mixer.music.load('Sounds\\bg-track.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

try:
    while(True):
        if turnStart:
            time.sleep(0.2)
            turnStart = False
            if currentPlayer == MAGENTA:
                playerIndex = 0
            if currentPlayer == CYAN:
                playerIndex = 1
            if currentPlayer == LIME:
                playerIndex = 2
            if currentPlayer == OLIVE:
                playerIndex = 3
            monies[playerIndex] += updateTroops(tiles, currentPlayer)
            if ais[playerIndex] and not done and not introTest:
                makeMoves(tiles, monies, currentPlayer, playerIndex)
                if monies[playerIndex] > 10000:
                    for a in tiles:
                        for b in a:
                            if not b.color == currentPlayer:
                                b.color = BROWN
                                b.contents = []
                    ticker = 500
                    effect = pygame.mixer.Sound('Sounds\\ready.wav')
                    effect.set_volume(10000)
                    effect.play()
                    done = True
                    continue
                
                if currentPlayer == MAGENTA:
                    currentPlayer = CYAN
                elif currentPlayer == CYAN:
                    currentPlayer = LIME
                elif currentPlayer == LIME:
                    currentPlayer = OLIVE
                elif currentPlayer == OLIVE:
                    currentPlayer = MAGENTA
                turnStart = True                    
        draw(dis, tiles, font)
        if attacking:
            a = 0
            b = 0
            for y in tiles:
                for x in y:
                    if x.selected:
                        a = x
                    if x.moveTo:
                        b = x
            troops = displayAttack(tiles, a, b, dis, fontDisplayAttack, scale)
        if menu:
            openActionMenu(dis, fontDisplayAttack, currentPlayer, monies[playerIndex], selection, scale)
        if not (scale <= 0) and left and ((selection == 0 and menu) or attacking):
            scale -= 0.02
        if not (scale >= 1) and right and ((selection == 0 and menu )or attacking):
            scale += 0.02
        if selection < 3 and up:
            selection += 1
        if selection > 0 and down:
            selection -= 1
        for event in pygame.event.get():
            if event.type == QUIT:
                raise Exception("UserExit")
                
            elif event.type == pygame.KEYDOWN:
                if introTest:
                    introTest = False
                    if event.key == pygame.K_1:
                        tiles = list()
                        for x in range(-6, 6):
                            temp = []
                            for y in range (-6, 6):
                                if random.random() < 0.2:
                                    continue
                                else:
                                    temp.append(tile(x, y, 0-x-y)) 
                            
                            tiles.append(temp)
                        addCity(8, 2, 6)
                        addMountains(tiles, 4, 6)
                        
                    elif event.key == pygame.K_2:
                        tiles = list()
                        for x in range(-8, 8):
                            temp = []
                            for y in range (-10, 10):
                                if random.random() < 0.2:
                                    continue
                                else:
                                    temp.append(tile(x, y, 0-x-y)) 
                                
                            tiles.append(temp)
                        addCity(12,3, 8)
                        addMountains(tiles, 6, 8)
                        
                    elif event.key == pygame.K_4:
                        tiles = list()
                        for x in range(-14, 14):
                            temp = []
                            for y in range (-10, 10):
                                if random.random() < 0.2:
                                    continue
                                else:
                                    temp.append(tile(x, y, 0-x-y)) 
                                
                            tiles.append(temp)
                        addCity(16, 4, 14)
                        addMountains(tiles, 12, 8)
                        
                    elif event.key == pygame.K_5:
                        tiles = list()
                        for x in range(-18, 18):
                            temp = []
                            for y in range (-20, 20):
                                if random.random() < 0.2:
                                    continue
                                else:
                                    temp.append(tile(x, y, 0-x-y)) 
                                
                            tiles.append(temp)
                        addCity(20,5, 18)
                        addMountains(tiles, 16, 8)
                if done:
                    seed = int(random.random()*1000)
                    random.seed(seed)
                    monies = [0,0,0,0]
                    tiles = list()
                    for x in range(-10, 10):
                        temp = []
                        for y in range (-10, 10):
                            if random.random() < 0.2:
                                continue
                            else:
                                temp.append(tile(x, y, 0-x-y)) 
                            
                        tiles.append(temp)
                    addCity(12, 3, 10)
                    addMountains(tiles, 8, 8)    
                    #getting mouse offset
                    prevX = -1
                    prevY = -1
                    
                    #Turn Start
                    turnStart = True
                    currentPlayer = MAGENTA
                    scale = 1
                    left = False
                    right = False
                    up = False
                    down = False
                    troops = 0
                    attacking = False
                    menu = False
                    done = False
                    selection = 0
                    introTest = True
                    ticker = 0
                    break;
                
                if event.key == pygame.K_u:
                    if ais[0]:
                        ais[0] = 0
                    else:
                        ais[0] = 1
                if event.key == pygame.K_i:
                    if ais[1]:
                        ais[1] = 0
                    else:
                        ais[1] = 1
                if event.key == pygame.K_o:
                    if ais[2]:
                        ais[2] = 0
                    else:
                        ais[2] = 1
                if event.key == pygame.K_p:
                    if ais[3]:
                        ais[3] = 0
                    else:
                        ais[3] = 1
                if event.key == pygame.K_LEFT:
                    left = True
                    
                elif event.key == pygame.K_RIGHT:
                    right = True
                elif event.key == pygame.K_DOWN:
                    up = True
                    
                elif event.key == pygame.K_UP:
                    down = True                
                elif event.key == pygame.K_ESCAPE:
                    if attacking:
                        attacking = False
                    if menu:
                        menu = False
                    scale = 1
                    for r in tiles:
                        for b in r:
                            b.selected = False
                            b.possible = False
                            b.moveTo = False
                elif event.key == pygame.K_RETURN:
                    if attacking:
                        attacking = False
                        if troops > 0:
                            moveTroops(tiles, a, b, troops)
                            b.contents = combat(tiles, b, currentPlayer)
                        scale = 1
                        for r in tiles:
                            for b in r:
                                b.selected = False
                                b.possible = False
                                b.moveTo = False
                    
                    if menu:
                        if selection == 0:
                            cost = int(int((monies[playerIndex] * scale / 10) * 10) /10) * 10
                            monies[playerIndex] -= cost
                            for r in tiles:
                                for b in r:
                                    if b.selected and b.color == currentPlayer:
                                       
                                        b.contents.append(army(int(cost/10), currentPlayer))
                                        b.contents[-1].movable=0
                                        b.contents = combat(tiles, b, currentPlayer)
                        elif selection == 1:
                            cost = 500
                            if monies[playerIndex] >= cost:
                                for r in tiles:
                                    for b in r:
                                        if b.selected and b.color == currentPlayer:
                                            aok = True
                                            for n in b.contents:
                                                if not n.name == "army":
                                                    aok = False
                                            if aok and monies[playerIndex] >= cost:
                                                monies[playerIndex] -= cost
                                                b.contents.append(fort(b, currentPlayer))
                                                b.bonus = 0.25
                        elif selection == 2:
                            cost = 1000
                            if monies[playerIndex] > cost:
                                monies[playerIndex] -= cost
                                for r in tiles:
                                    for b in r:
                                        if b.selected:
                                            for n in b.contents:
                                                if n.name == "army":
                                                    n.morale /= 2
                                                    if random.random() < 0.5:
                                                        n.heroes = []
                                                    
                        elif selection == 3 and monies[playerIndex] >= 10000:
                            for a in tiles:
                                for b in a:
                                    if not b.color == currentPlayer:
                                        b.color = BROWN
                                        b.contents = []
                                        
                            ticker = 500
                            effect = pygame.mixer.Sound('Sounds\\ready.wav')
                            effect.set_volume(10000)
                            effect.play()
                            
                        menu = False
                            
                elif event.key == pygame.K_m:
                    if menu:
                        menu = False
                        scale = 1
                        for r in tiles:
                            for b in r:
                                b.selected = False
                                b.possible = False
                                b.moveTo = False
                    else:
                        if not attacking:
                            scale = 1
                            menu = True
                elif event.key == pygame.K_e and not attacking and not menu:
                    if winCheck(tiles, currentPlayer):
                        done = True
                        endGame = True
                        break;
                    if currentPlayer == MAGENTA:
                        currentPlayer = CYAN
                    elif currentPlayer == CYAN:
                        currentPlayer = LIME
                    elif currentPlayer == LIME:
                        currentPlayer = OLIVE
                    elif currentPlayer == OLIVE:
                        currentPlayer = MAGENTA
                    turnStart = True
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left = False
                    
                elif event.key == pygame.K_RIGHT:
                    right = False
                elif event.key == pygame.K_DOWN:
                    up = False
                    
                elif event.key == pygame.K_UP:
                    down = False            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:  
                    dragging = True
                if event.button == 1 and not attacking and not menu and not introTest and not done:
                    mx, my= event.pos
                    for a in tiles:
                        for x in a:
                            if math.pow((mx-x.disX), 2) + math.pow((my-x.disY), 2) <= math.pow(x.size*math.sin(30), 2):
                                if x.selected:
                                    for r in tiles:
                                        for b in r:
                                            b.selected = False
                                            b.possible = False
                                            b.moveTo = False
                                            
                                elif x.possible:
                                    attacking = True
                                    x.possible = False
                                    x.moveTo = True
                                    
                                    
                                else:
                                    for r in tiles:
                                        for b in r:
                                            b.selected = False
                                            b.possible = False
                                            b.moveTo = False
                                    x.selected = True
                                    for n in x.contents:
                                        if n.name == "army" and n.team == currentPlayer and n.movable > 0:
                                            possibles = dispMoves(tiles, x, currentPlayer)
                                            for x in possibles:
                                                x.possible = True
                                            
                            
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:            
                    dragging = False
                    prevX=-1
                    prevY = -1
                
            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.pos
                if prevX >= 0:
                    moveX = mx - prevX
                    moveY = my - prevY
                else:
                    moveX = 0
                    movey = 0
                prevX = mx
                prevY = my
                
                if(dragging):
                    shift(tiles, moveX, moveY)
        if done:
            winScreen(dis, currentPlayer, finalFont, fontDisplayAttack)
        if introTest:
            intro(dis, tiles, finalFont, fontDisplayAttack)
        if ticker > 0:
            ticker -= 1
            s = pygame.Surface((1280,720))  
            s.set_alpha(ticker*ticker/(500*500)*255)                
            s.fill((255,255,255))
            dis.blit(s, (0,0))
        pygame.display.update()
        fpsClock.tick(FPS)
        
except Exception as e:
    
    printl(e)
    print()
    traceback.print_exc(file=sys.stdout)
    pygame.quit()
    sys.exit()
    
    
    
    
    