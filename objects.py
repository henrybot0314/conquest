# -*- coding: utf-8 -*-
"""
Created on Sat May 26 12:35:16 2018

@author: Henry
"""
import pygame, sys
from pygame.locals import *
from init import *
from objects import *
from methods import *
from constants import *
import math

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
        
        

    
