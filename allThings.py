# -*- coding: utf-8 -*-
"""
Created on Sun May 27 06:13:35 2018

@author: Henry
"""

import pygame, sys, traceback
import math
import random
from pygame.locals import *
from constants import *


class tile:
    x = 0
    y = 0
    z = 0
    disX = 0       
    disy = 0
    size = 35
    color = GREEN
    borderColor = BLACK
    contents = list()
    pointArray = list()
    selected = False
    possible = False
    moveTo = False
    team = None
    bonus = 0

    def __init__(self, tx, ty, tz, tdisX = None, tdisY = None, tcolor = None, tborderColor = None, tcontents = None):
        self.x = tx
        self.y = ty
        self.z = tz
        tempy, tempx = cube_to_offset(self)
        if tdisX == None:
            if tempx % 2 == 0:
                self.disX =  tempx * (self.size*3) /2
                self.disY = tempy  * (self.size*math.cos(math.radians(30)))*2
            else:
                self.disX = tempx * (self.size*3) /2 
                self.disY = tempy * (self.size*math.cos(math.radians(30))*2) +self.size*math.cos(math.radians(30)) 
            self.contents = list()
        else:
            self.disX = tdisX
            self.disY = tdisY
            self.color = tcolor
            self.borderColor = tborderColor
            self.contents= tcontents
            
        self.pointArray = getPointArray(self.disX, self.disY, self.size)
        self.team= self.color

        
class city:
    level = 0
    owner = None
    production = 0
    name = "city"
    team = ""
    
    def __init__ (self, towner, tteam, tlevel = 1, tproduction = 10):
        self.owner = towner
        self.level = tlevel
        self.production = tproduction
        self.team = tteam
class fort:
    level = 0
    owner = None
    production = 0
    name = "fort"
    team = ""
    
    def __init__ (self, towner, tteam, tlevel = 1, tproduction = 10):
        self.owner = towner
        self.level = tlevel
        self.production = tproduction
        self.team = tteam

class mountain:
    team = ""
    name = "mountain"
    def __init__(self):
        pass
        
class army:
    pop = 0
    fight = 0
    morale = 0
    heroes = []
    supplies = 0
    team = ""
    name = "army"
    movable = 0
    def calcFight(self):
        if self.morale > self.pop:
            self.morale = float(self.pop)
        if self.supplies > self.pop:
            self.supplies = float(self.pop)
        self.fight =float( self.morale+self.supplies)
        for x in self.heroes:
            self.fight += x
    
    def __init__ (self, tpop, tteam, tmorale = None, theroes = None, tsupplies = None):
        self.pop = tpop
        self.movable = self.pop
        self.team = tteam
        if tmorale == None:
            self.morale = float(self.pop)/2
            self.heroes = []
            self.supplies = float(self.pop)
        else:
            self.morale = float(tmorale)
            self.heroes = theroes
            self.supplies = float(tsupplies)
            
        self.calcFight()
    
    def update(self, tmorale, theroes, tsupplies):
        self.morale += float(tmorale)
        self.heroes=theroes
        self.supplies += float(tsupplies)
        self.calcFight()
        
        


def draw(dis, tiles, font):
    dis.fill(BLUE)
    for a in tiles:
        for x in a:
            pygame.draw.polygon(dis, x.color, x.pointArray)
            pygame.draw.polygon(dis, x.borderColor, x.pointArray, 2)            
            #textsurface = font.render( str(x.x) + " " +str(x.y) + "  "+ str(x.z), False, (0, 0, 0))
            #dis.blit(textsurface,(x.disX-x.size+8, x.disY))
            
            for n in x.contents:
                if n.name == "city":
                    temp = Rect(x.disX-15, x.disY-23, 30, 40)
                    pygame.draw.rect(dis, GRAY, temp)
                    pygame.draw.rect(dis, BLACK, temp, 1)            
                    textsurface = font.render( "Lvl. " + str(n.level), False, (0, 0, 0))
                    dis.blit(textsurface,(x.disX-13, x.disY ))
                    
                if n.name == "fort":
                    temp = Rect(x.disX-15, x.disY-23, 30, 40)
                    pygame.draw.rect(dis, BROWN, temp)
                    pygame.draw.rect(dis, BLACK, temp, 1)            
                    textsurface = font.render( "Lvl. " + str(n.level), False, (0, 0, 0))
                    dis.blit(textsurface,(x.disX-13, x.disY ))
                
                if n.name == "mountain":
                    pygame.draw.polygon(dis, GRAY, [[x.disX, x.disY-20],[x.disX+20, x.disY+17],[x.disX-20, x.disY+17]])
                    pygame.draw.polygon(dis, BLACK, [[x.disX, x.disY-20],[x.disX+20, x.disY+17],[x.disX-20, x.disY+17]], 1)
                
                if n.name == "army":
                    pygame.draw.circle(dis, n.team, [int(x.disX), int(x.disY)], 15)
                    pygame.draw.circle(dis, BLACK, [int(x.disX), int(x.disY)], 15, 1)
                    textsurface = font.render( str(n.pop), False, (0, 0, 0))
                    if n.pop < 100:
                        dis.blit(textsurface,(x.disX-5, x.disY - 12 ))
                    elif n.pop < 1000:
                        dis.blit(textsurface,(x.disX-9, x.disY - 12 ))
                    else:
                        dis.blit(textsurface,(x.disX-12, x.disY - 12 ))
                    textsurface2 = font.render( str(int(n.fight)), False, (0, 0, 0))
                    
                    n.calcFight()
                    
                    if n.pop < 100:
                        dis.blit(textsurface2,(x.disX-5, x.disY + 0))
                    elif n.pop < 1000:
                        dis.blit(textsurface2,(x.disX-9, x.disY + 0 ))
                    else:
                        dis.blit(textsurface2,(x.disX-12, x.disY + 0 ))          
    for a in tiles:
        for x in a:
            for n in x.contents:
                if n.name == "army":
                    pygame.draw.circle(dis, n.team, [int(x.disX), int(x.disY)], 15)
                    pygame.draw.circle(dis, BLACK, [int(x.disX), int(x.disY)], 15, 1)
                    textsurface = font.render( str(n.pop), False, (0, 0, 0))
                    if n.pop < 100:
                        dis.blit(textsurface,(x.disX-5, x.disY - 12 ))
                    elif n.pop < 1000:
                        dis.blit(textsurface,(x.disX-9, x.disY - 12 ))
                    else:
                        dis.blit(textsurface,(x.disX-12, x.disY - 12 ))
                    textsurface2 = font.render( str(int(n.fight)), False, (0, 0, 0))
                    
                    n.calcFight()
                    
                    if n.pop < 100:
                        dis.blit(textsurface2,(x.disX-5, x.disY + 0))
                    elif n.pop < 1000:
                        dis.blit(textsurface2,(x.disX-9, x.disY + 0 ))
                    else:
                        dis.blit(textsurface2,(x.disX-12, x.disY + 0 ))       
    for a in tiles:
        for x in a:
            if x.possible:
                pygame.draw.polygon(dis, YELLOW, x.pointArray, 2)  
    for a in tiles:
        for x in a:
            if x.selected:
                pygame.draw.polygon(dis, WHITE, x.pointArray, 2)  
                
    for a in tiles:
        for x in a:
            if x.moveTo:
                pygame.draw.polygon(dis, RED, x.pointArray, 2)       

def shift(tiles, moveX, moveY):
    for a in tiles:
        for x in a:
            x.disX += moveX
            x.disY += moveY
            x.pointArray = getPointArray(x.disX, x.disY, x.size)

def getPointArray(disX, disY, size):
    pointArray = list()
    pointArray.append([disX + size, disY])
    pointArray.append([disX + size*math.sin(math.radians(30)), disY + size*math.cos(math.radians(30))])
    pointArray.append([disX - size*math.sin(math.radians(30)), disY + size*math.cos(math.radians(30))])
    pointArray.append([disX - size, disY])
    pointArray.append([disX - size*math.sin(math.radians(30)), disY - size*math.cos(math.radians(30))])
    pointArray.append([disX + size*math.sin(math.radians(30)), disY - size*math.cos(math.radians(30))])
    
    return pointArray
    
def cube_to_offset(cube):
    col = cube.x
    row = cube.z + (cube.x - (cube.x&1)) / 2
    return row, col

def neighbors(tiles, tile):
    temp = list()
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == -1 and dy == -1:
                continue
            if dx == 1 and dy == 1:
                continue                
            if getTile(tiles, tile.x+dx, tile.y+dy):
                temp.append (getTile(tiles, tile.x+dx, tile.y+dy))
    return temp

def getTile(tiles, x, y):
    for a in tiles:
        for b in a:
            if b.x == x and b.y == y:
                return b
    return False

def worth(tiles, teamColor, monies):
    count = 0
    for a in tiles:
        for b in a:
           for c in b.contents:
               if c.team == teamColor:
                   if c.name == "army":
                       count += c.pop * 10
                   if c.name == "fort":
                       count += 500
                   if c.name == "city":
                       count += 1000
    if teamColor == MAGENTA:
        count += monies[0]
    elif teamColor == CYAN:
        count += monies[1]
    elif teamColor == LIME:
        count += monies[2]
    elif teamColor == OLIVE:
        count += monies[3]
    return count
        

def heuristic(tiles, monies, currentPlayer):
    Scores = [worth(tiles, MAGENTA, monies), worth(tiles, CYAN, monies), worth(tiles, LIME, monies), worth(tiles, OLIVE, monies)]
    if currentPlayer == MAGENTA:
        return Scores[0] > (Scores[1] + Scores[2] + Scores[3]) / 3
    elif currentPlayer == CYAN:
        return Scores[1] > (Scores[0] + Scores[2] + Scores[3]) / 3
    elif currentPlayer == LIME:
        return Scores[2] > (Scores[1] + Scores[0] + Scores[3]) / 3
    elif currentPlayer == OLIVE:
        return Scores[3] > (Scores[1] + Scores[2] + Scores[0]) / 3
    
def think(tiles, tile, team):
    for item in tile.contents:
        if item.name == "army":
            temp = item.pop
    result = []
    moves = dispMoves(tiles, tile, team)
    for a in moves:
        if a.color != team:
            city = False
            fort = False
            for x in a.contents:
                if x.name == "army":
                    if x.pop * 1.2 >= temp:
                        continue
                    elif fort and x.pop * 1.7 >= temp:
                        continue
                    elif city and x.pop * 2.2 >= temp:
                        continue
                if x.name == "city":
                    city = True
                if x.name == "fort":
                    fort = True
        result.append(a)
    return result


def makeMoves(tiles, monies, team, playerIndex):
    winning = heuristic(tiles, monies, team)
    armies = []
    armies_pop = []
    forts = 0
    for a in tiles:
        for b in a:
            for c in b.contents:
                if b.color == team and c.name == "army":
                    armies.append(b)
                    armies_pop.append(c.pop)
                if b.color == team and c.name == "fort":
                    forts +=1
                
    if len(armies) < 1:
        return 0
    
    if forts > 20:
        pass
    elif winning:
        ticker = 0
        while(monies[playerIndex] > 500 and ticker < 2000):
            rand = armies[int(random.random()*len(armies))]
            if len(rand.contents) == 1:
                for a in tiles:
                    for b in a:
                        if b.x == rand.x and b.y == rand.y:
                            monies[playerIndex] -= 500
                            b.contents.append(fort(b, team))
                            b.bonus = 0.25
            ticker+=1 
    else:
        troops =int( monies[playerIndex]/10 )
        cost = troops * 10
        monies[playerIndex] -= cost
        rand = armies[int(random.random()*len(armies))]
        for a in tiles:
            for b in a:
                if b.x == rand.x and b.y == rand.y:        
                    b.contents.append(army(troops, team))
                    b.contents = combat(tiles, b, team)
    
    for i,x in enumerate(armies):
        print("--")
        moves = think(tiles, x, team)
        for y in moves:
            troops = 5
            if troops > armies_pop[i]:
                troops = armies_pop[i]
            if troops > 0 and not (y.x == x.x and y.y == x.y):
                for a in x.contents:
                    if a.name == "army":
                        pop = a.pop
                        morale = a.morale
                        supplies = a.supplies
                if pop < 1:
                    continue
                y.contents.append(army(troops, team, float(morale)/(pop)*troops, [], supplies /pop * troops))
                y.contents[-1].movable = 0
                y.contents = combat(tiles, y, team)
                for a in x.contents:
                    if a.name == "army":
                        a.update(-1 * float(morale)/pop*troops, [], -1*float(supplies) / pop * troops)
                        a.pop = pop - troops
                        a.movable = pop - troops
    for a in tiles:
        for b in a:
            for c in b.contents:
                if c.name == "army":
                    if c.pop < 1:
                        b.contents.remove(c)
def updateTroops(tiles, team):
    income = 0
    for a in tiles:
        for b in a:
            b.selected = False
            b.possible = False
            b.moveTo = False
            if b.color == team:
                income += 2
            for x in b.contents:
                if x.name == "army" and x.team == team:
                    x.movable = x.pop
                    x.morale = float(x.morale) * 0.95
                    surround = neighbors(tiles, b)
                    allied = -1
                    for n in surround:
                        if n.color == team:
                            allied += 1
                    if allied == 0:
                        x.supplies = x.supplies *  0.6
                    if allied > 2:
                        x.supplies = x.supplies * 1.2
                        if x.supplies > x.pop:
                            x.supplies = x.pop
                    income -= int(x.pop / 100)
                    
                elif x.name == "city" and x.team == team:
                    b.contents.append(army(10, team))
                    b.contents= combat(tiles, b, team)
                    income += 50
                elif x.name == "fort" and x.team == team:
                    b.contents.append(army(5, team))
                    b.contents= combat(tiles, b, team)
                    income += 20
    effect = pygame.mixer.Sound('Sounds\\ready.wav')
    effect.set_volume(10000)
    effect.play()
    return income

def dispMoves(tiles, tile, team):
    result = []
    for x in neighbors(tiles, tile):
        if x not in result:
            result.append(x)
        out = False
        for y in x.contents:
            if y.name == "army" and not y.team == team:
                out = True
            if y.name == "mountain":
                out = True
        if out:
            continue
        for a in neighbors(tiles, x):
            if a not in result and (len(a.contents ) == 0 or not a.contents[0].name == "mountain"):
                result.append(a)
    return result
        
def displayAttack(tiles, tile1, tile2, dis, font, scale):
    troops = 0
    for x in tile1.contents:
        if x.name == "army":
            troops = x.pop
    if troops == 0:
        return 0

    rect = Rect(779, 1, 500, 200)
    pygame.draw.rect(dis, BROWN, rect, 0)
    pygame.draw.rect(dis, BLACK, rect, 1) 
    border = Rect(799, 30, 100, 32)
    #pygame.draw.rect(dis, BLACK, border, 1)
    textsurface = font.render( "Troops", False, (0, 0, 0))
    dis.blit(textsurface,(800, 22))
    amount = Rect(950, 30, 100, 32)
    pygame.draw.rect(dis, BLACK, amount, 1)
    troopCount = font.render(str(int(troops * scale)), False, (0, 0, 0))
    dis.blit(troopCount,(951, 22))
    
    slider = Rect(800, 80, 460, 32)
    pygame.draw.rect(dis, BLACK, slider, 1)
    sliderBar = Rect(800 + (scale * 450), 80, 10, 32 )
    pygame.draw.rect(dis, BLACK, sliderBar)
    
    confirmText = font.render("Press 'Enter' to Commit", False, (0, 0, 0))
    dis.blit(confirmText,(800, 150))
    return int(troops*scale)

def moveTroops(tiles, tile1, tile2, troops):
    for a, x in enumerate(tile1.contents):
        if x.name == "army":
            temp = a
    tile2.contents.append(army(troops, tile1.contents[temp].team, float(tile1.contents[temp].morale)/tile1.contents[temp].pop*troops, tile1.contents[temp].heroes, float(tile1.contents[temp].supplies) /tile1.contents[temp].pop * troops))
    tile2.contents[-1].movable = 0
    tile1.contents[temp].update(-1 * float(tile1.contents[temp].morale)/tile1.contents[temp].pop*troops, [], -1*float(tile1.contents[temp].supplies) /tile1.contents[temp].pop * troops)
    tile1.contents[temp].pop -= troops
    tile1.contents[temp].movable -= troops
    print("--2")
    print(tile1.contents[temp].pop)
    print(troops)
    
    
    if tile1.contents[temp].pop < 1:
        tile1.contents.pop(temp)
        

def uncontested(tiles, tile, team):
    for x in tile.contents:
        if x.name == "army":
            return -1
    temp = neighbors(tiles, tile)
    for y in temp:
        for z in y.contents:
            if z.name == "army" and not z.team == team and not tile.color == GREEN:
                return 0
    return 1

def openActionMenu(dis, font, currentPlayer, currentMoney, selection, scale):
    menu = Rect(320, 30, 640, 570)
    pygame.draw.rect(dis, WHITE, menu)
    playerBar = Rect(320, 30, 640, 30)
    pygame.draw.rect(dis, currentPlayer, playerBar)
    coin = pygame.image.load('Images//goldCoin.jpg')
    coin = pygame.transform.scale(coin, (50, 40))
    dis.blit(coin, (321, 60))
    moneyText = font.render(str(currentMoney), False, (0, 0, 0))
    dis.blit(moneyText,(371,60))
    
    soldier = pygame.image.load('Images//soldier.jpg') #Soldier
    soldier = pygame.transform.scale(soldier, (100, 100))
    dis.blit(soldier, (321, 125))
    
    fort = pygame.image.load('Images//fort.jpg') #Fort
    fort = pygame.transform.scale(fort, (100, 100))
    dis.blit(fort, (321, 250))
    costFort = font.render("Cost: 500", False, (0, 0, 0))
    dis.blit(costFort, (640, 160 + 125))
    
    sabotage = pygame.image.load('Images//Sabotage.jpg') #Sabotage
    sabotage = pygame.transform.scale(sabotage, (100, 100))
    dis.blit(sabotage, (321, 375))
    costSabotage = font.render("Cost: 1500", False, (0, 0, 0))
    dis.blit(costSabotage, (640, 160 + 250))
    
    check = 3
    
    if currentMoney > 10000:
        bomb = pygame.image.load('Images//atomicBomb.jpg') #Atomic Bomb
        bomb = pygame.transform.scale(bomb, (100, 100))
        dis.blit(bomb, (321, 500))
        check = 4
        costBomb = font.render("Cost: 10000", False, (0, 0, 0))
        dis.blit(costBomb, (640, 160 + 375))

    
    for i in range(check):
        if i == 0:
            miniSlider = Rect(640, 125, 300, 32)
            pygame.draw.rect(dis, BLACK, miniSlider, 1)
            miniSliderBar = Rect(640 + (scale * 290), 125, 10, 32 )
            pygame.draw.rect(dis, BLACK, miniSliderBar)
            
            costSoldier = font.render("Cost: " + str(int(int((currentMoney * scale / 10) * 10) /10) * 10), False, (0, 0, 0))
            dis.blit(costSoldier, (640, 160))
        if i == selection: 
            choice = Rect(320, 100 + (124 * i), 640, 125)
            pygame.draw.rect(dis, currentPlayer, choice, 5)
        else:
            choice = Rect(320, 100 + (124 * i), 640, 125)
            pygame.draw.rect(dis, BLACK, choice, 1)
        
    pygame.draw.rect(dis, BLACK, menu, 1)

def combat(tiles, tile, team):
    armies = []
    for x in tile.contents:
        if x.name == "army":
            armies.append(x)

    if len(armies) < 2:
        conquests = neighbors(tiles, tile)
        for a in conquests:
            if uncontested(tiles, a, team) == 1:
                a.color = team
                a.team = team
                for x in a.contents:
                    x.team = team
                for x in tile.contents:
                    if x.name == "army":
                        x.morale += 2.0
        tile.color = team
        tile.team = team
        for x in tile.contents:
            x.team = team  
        effect = pygame.mixer.Sound('Sounds\\ready.wav')
        effect.set_volume(10000)
        effect.play()
        return tile.contents
    
    if len(armies) > 1 and armies[0].team == armies[1].team:
        
        temp = armies[1]
        temp.pop += armies[0].pop
        temp.update(armies[0].morale, temp.heroes + armies[0].heroes, armies[0].supplies)
        temp.movable = 0
        
        conquests = neighbors(tiles, tile)
        for a in conquests:
            if uncontested(tiles, a, team) == 1:
                a.color = team
                a.team = team
                for x in a.contents:
                    x.team = team
                temp.morale += 2.0
        tile.color = team
        tile.team = team
        for x in tile.contents:
            x.team = team          
        result = []
        
        for i, x in enumerate(tile.contents):
            if not x.name == "army":
                result.append(x)
        result.append(temp)
        effect = pygame.mixer.Sound('Sounds\\ready.wav')
        effect.set_volume(10000)
        effect.play()
        return result
    
    elif len(armies) > 1 and armies[0].team == tile.color:
        attackers = armies[1].pop
        defenders = armies[0].pop
        
        atkRatio = float(armies[1].fight)/armies[1].pop
        defRatio = float(armies[0].fight)/float(armies[0].pop)*(1 + tile.bonus)
        
        print(atkRatio, defRatio)
        
        while attackers > 0 and defenders > 0:
            aroll = (atkRatio)*random.random()
            droll = (defRatio)*random.random()
            
            if aroll > droll:
                defenders -= 1
            else:
                attackers -= 1
        
        if attackers < 1:
            newPop = defenders
            newTeam = armies[0].team
            newMorale = armies[0].morale/armies[0].pop*defenders
            newHeroes = armies[0].heroes
            newSupplies = armies[0].supplies
            if armies[1].pop > armies[0].pop * (1 + tile.bonus):
                newMorale = newMorale * armies[1].pop / (armies[0].pop * (1+tile.bonus))
                
        else:
            newPop = attackers
            newTeam = armies[1].team
            newMorale = armies[1].morale/armies[1].pop*attackers
            newHeroes = armies[1].heroes
            newSupplies = armies[1].supplies
            
            for x in tile.contents:
                if x.name == "city":
                    newMorale *= 1.4
                if x.name == "fort":
                    newMorale *= 1.2
            if armies[0].pop > armies[1].pop:
                newMorale = newMorale * armies[0].pop / armies[1].pop
        
                    
        newMorale *= 1.1
        
        temp = army(newPop, newTeam, newMorale, newHeroes, newSupplies)
        temp.movable = 0
        result = []
        for i, x in enumerate(tile.contents):
            if not x.name == "army":
                result.append(x)
        result.append(temp)

        tile.content = result
        
        if attackers > 0:
            conquests = neighbors(tiles, tile)
            for a in conquests:
                if not uncontested(tiles, a, team) == -1:
                    a.color = team
                    a.team = team
                    for x in a.contents:
                        x.team = team
            tile.color = team
            tile.team = team
            for x in tile.contents:
                x.team = team           
        effect = pygame.mixer.Sound('Sounds\\battle.wav')
        effect.set_volume(10000)
        effect.play()
        
        return result
        
    else:
        raise Exception()
    
def winCheck(tiles, currentPlayer):
    count = 0
    for a in tiles:
        for b in a:
           for c in b.contents:
               if c.name == "army":
                   if c.team != currentPlayer:
                       return False
    return True
    
def winScreen(dis, currentPlayer, font, font2):
    endScreen = Rect(0, 0, 1280, 760)
    pygame.draw.rect(dis, currentPlayer, endScreen)
    final = font.render("CONQUEST", False, (0, 0, 0))
    dis.blit(final, (370, 290))
    cont = font2.render("Press Any Key for a New Game", False, (0,0,0))
    dis.blit(cont, (450,440))
    
def intro(dis, tiles, font, font2):
    dis.fill(BLUE)
    for a in tiles:
        for x in a:
            pygame.draw.polygon(dis, x.color, x.pointArray)
            pygame.draw.polygon(dis, x.borderColor, x.pointArray, 2)
    final = font.render("CONQUEST", False, (0, 0, 0))
    dis.blit(final, (370, 290))
    final = font2.render("Indicate Map Size (1-5)", False, (0, 0, 0))
    dis.blit(final, (450, 440))
    
def toString(tiles, monies, currentPlayer):
    pass