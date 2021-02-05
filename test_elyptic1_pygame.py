import time, math, ecdsa
from ecdsa import SECP256k1
from ecdsa.ecdsa import Public_key
SECP256k1_GEN = SECP256k1.generator

import pygame, pyqrcode 
from pygame.locals import * # MOUSEBUTTONDOWN...
from json import *
from datetime import datetime 
# from oeLib.oePygame import *

pygame.init()
startTime = time.time()

myFont = pygame.font.SysFont("monospace", 15)

# Set up some variables containing the screeen size
size = 600
sizeWinX=900
sizeWinY=size

colYel = (255,255,0)
colWhi = (255,255,255)
colRed = (255,0,0)
colBlu = (0,0,255)
colSil = (128,128,128)
colBla = (0,0,0)

hW=600 #velikost
hH=300
scale = 0.5

win = pygame.display.set_mode([sizeWinX,sizeWinY]) # Create the pygame window
pygame.display.set_caption("eliptic")

print("--- simple test ---")

# y^2 = x^3 + a*x + b

a = 1
b = 1
for x in range(-10,10):
   temp = x*x*x + a*x + b
   y = math.sqrt(abs(temp))
   print(x, y, temp)

print()


# prime 281
# (y^2 -x^3 + 3*x) mod p = 0

print(" --- prime # mod ---")
# 211 | 223 | 227 | 229 | 233 | 239 | 241 | 251 | 257 | 263 | 269 | 271 | 277 | 281 | 283 | 293
p = 281
"""
# osy
# pygame.draw.line(win,colRed,(0,sizeWinX),((p+1)/2,sizeWinX),2)
pygame.draw.line(win,colWhi,(0,p/2*scale),(sizeWinX,p/2*scale),2)
pygame.display.flip()

for x in range(int(size/scale)):
   for y in range(int(size/scale)):
      temp = (y*y - x*x*x + 3*x)

      if(temp % p == 0):
         print(x, y, temp, temp % p)
         pygame.draw.line(win,colWhi,(x*scale,y*scale),(x*scale+2,y*scale),2)
         pygame.display.flip()
print()
"""
p = 1009 # 593

# osy
# pygame.draw.line(win,colRed,(0,sizeWinX),((p+1)/2,sizeWinX),2)
pygame.draw.line(win,colSil,(0,p/2*scale-100),(sizeWinX,p/2*scale-100),2)
pygame.draw.line(win,colYel,(0,p/2*scale),(sizeWinX,p/2*scale),2)
pygame.draw.line(win,colSil,(0,p/2*scale+100),(sizeWinX,p/2*scale+100),2)
pygame.display.flip()

for x in range(int(size/scale)):
   for y in range(int(size/scale)):
      temp = (y*y - x*x*x + 3*x)

      if(temp % p == 0):
         print(x, y, temp, temp % p)
         pygame.draw.line(win,colYel,(x*scale,y*scale),(x*scale+2,y*scale),2)
         pygame.display.flip()
print()


time.sleep(15)
