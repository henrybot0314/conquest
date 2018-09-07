# -*- coding: utf-8 -*-
"""
Created on Sat May 26 13:00:11 2018

@author: Henry
"""

#Colors
BLACK=(0,0,0)
WHITE=(255,255,255)
RED	=(255,0,0)
LIME=(0,255,0)
BLUE=(0,0,255)
YELLOW	=(255,255,0)
CYAN=(0,255,255)
MAGENTA=(255,0,255)
SILVER	=(192,192,192)
GRAY=(128,128,128)
OLIVE=(128,128,0)
GREEN=(0,128,0)
PURPLE	=(128,0,128)
TEAL=(0,128,128)
NAVY=(0,0,128)
BROWN = (139, 69, 19)


#Methods
def printl(msg):
    if isinstance(msg, Exception):
        print("Exception --> " + str(msg))
    else:
        print("--> " + str(msg))