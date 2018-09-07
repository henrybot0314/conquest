# -*- coding: utf-8 -*-
"""
Created on Sat May 26 12:35:30 2018

@author: Henry
"""
import pygame, sys
from pygame.locals import *
from init import *
from constants import *
import math
import random
from objects import *
from actMethods import 

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
    
def think(tile, team):
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
    for a in tiles:
        for b in a:
            for c in b.contents:
                if c.name == "army":
                    armies.append(b)
    if winning or 1==1:
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
                    combat(tiles, b, team)
    
    for x in armies:
        moves = think(x, team)
        for y in moves:
            moves.contents.append(army(troops, team))
            combat(tiles, b, team)

