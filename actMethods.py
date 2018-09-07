# -*- coding: utf-8 -*-
"""
Created on SatMay 26 17:03:53 2018

@author: Henry
"""
from methods import *
from objects import *
import pygame, sys
from pygame.locals import *
import random

def updateTroops(tiles, team):
    income = 0
    for a in tiles:
        for b in a:
            b.selected = False
            b.possible = False
            b.moveTo = False
            if b.color == team:
                income += 5
            for x in b.contents:
                if x.name == "army" and x.team == team:
                    x.movable = x.pop
                    x.morale = float(x.morale) * 0.95
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
    for x in tile1.contents:
        if x.name == "army":
            troops = x.pop

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
    
    