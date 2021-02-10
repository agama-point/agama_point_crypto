# ECC:  y^2 = x^3 + a*x + b
# "Bitcoin curve" secp256k1 takes the form: (y^2 ≡ x^3 + 7) mod p
# (y^2 -x^3 + 3*x) mod p = 0


"""
https://github.com/tlsfuzzer/python-ecdsa/blob/master/src/ecdsa/ellipticcurve.py
http://hyperelliptic.org/EFD/g1p/auto-shortw-jacobian.html#doubling-mdbl-2007-bl
https://stackoverflow.com/questions/31074172/elliptic-curve-point-addition-over-a-finite-field-in-python
https://github.com/tlsfuzzer/python-ecdsa/blob/master/src/ecdsa/ellipticcurve.py
https://github.com/alexmgr/tinyec/blob/master/tinyec/ec.py
https://github.com/qubd/mini_ecdsa/blob/master/mini_ecdsa.py
"""

import time, math, pygame, ecdsa
from ecdsa import SECP256k1
from pygame.locals import * # MOUSEBUTTONDOWN...
from datetime import datetime 
from ecdsa.ecdsa import Public_key
from crypto_agama.ecc import point_adding, point_doubling
from tinyec.ec import SubGroup, Curve


# Set up some variables containing the screeen size
size = 600
sizeWinX=900
sizeWinY=size

hW=640
hH=320
x0, y0 = 39, hH*2 - 90


colYel = (255,255,0)
colWhi = (255,255,255)
colRed = (255,0,0)
colBlu = (0,0,255)
colSil = (80,80,80)
colSilD = (32,32,32)
colSilL = (128,128,128)
colBla = (0,0,0)

print("--- simple test ---")
pygame.init()
startTime = time.time()

win = pygame.display.set_mode([sizeWinX,sizeWinY]) # Create the pygame window
pygame.display.set_caption("eliptic")
myFont = pygame.font.SysFont("monospace", 16)

# prime 281
"""
print(" --- prime # mod ---")
# 211 | 223 | 227 | 229 | 233 | 239 | 241 | 251 | 257 | 263 | 269 | 271 | 277 | 281 | 283 | 293
p = 281

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
# SECP256k1_GEN = SECP256k1.generator # "p1707" ?
# example of elliptic curve having cofactor = 1 is secp256k1 / cofactor = 8 is Curve25519 / cofactor = 4 is Curve448


print("---ecc---")
# (5,1) px = 5 / py = 1
# # y^2 = x^3 + a*x + b
# curve: "p1707" => y^2 = x^3 + 0x + 7 (mod 17)
# =======================================================================================================
a = 0 # 0 / 1 / / 2 / 3
b = 7 # 7 / 3
p = 17 # 17 / 11

dx0, dy0 = 15,13 # 6, 3 # 15, 13

scale = 30 # 30
print("a,b,g: ", a, b, p)


# grid
for y in range(p+1):
   pygame.draw.line(win,colSil,(x0+0,y0-y*scale),(x0+sizeWinX,y0-y*scale),2)
   label = myFont.render(str(y), 1, colSilL)
   win.blit(label, (x0-25, y0-y*scale-8))

for x in range(p+1):
   pygame.draw.line(win,colSil,(x0+x*scale,y0),(x0+x*scale,y0-p*scale),2)
   label = myFont.render(str(x), 1, colSilL)
   win.blit(label, (x0+x*scale-5, y0+10))

for i in range(p+2):
   pygame.draw.line(win,colWhi,(x0+i*scale,y0-p/2*scale),(x0+i*scale+scale/2,y0-p/2*scale),1)
   pygame.display.flip()


for x in range(p+5):
   for y in range(p+5):
      temp = (y*y - x*x*x - a*x- b)

      if(temp % p == 0):
         print(x, y, temp, temp % p)
         pygame.draw.circle(win,colYel,(x0+x*scale,y0-y*scale),3)
         pygame.display.flip()


print("---doubling---")

# x0, yo = 8, 3
print(a, dx0, dy0, "---start---")
oldx, oldy = dx0, dy0

lines = True

for gi in range(1,17): #(1,20)
   if (gi == 1):
      pygame.draw.circle(win,colBlu,(x0+dx0*scale,y0-dy0*scale),3)
      dx, dy = point_doubling(dx0, dy0, a=a, p=p) # 5,1
   else:
      #dx, dy = doubling_d(dx, dy, a=a, p=p)
      dx, dy = point_adding(dx0, dy0, dx, dy, p=p)
      # dy = rellect_on_x(dy,p)
      pygame.draw.circle(win,colRed,(x0+dx*scale,y0-dy*scale),3)

   if lines: pygame.draw.line(win,colSilL,(x0+oldx*scale,y0-oldy*scale),(x0+dx*scale,y0-dy*scale),1)
   oldx, oldy = dx,dy


   temp = (dy*dy - dx*dx*dx - a*dx - b)
   if(temp % p == 0):
      ok = "="
   else:
      ok = "!"

   # ry = rellect_on_x(dy,p)
   print(gi, ". ", dx , dy, ok)


   xp, yp = x0+dx*scale+5, y0-dy*scale+5
   label = myFont.render(str(gi+1), 1, colWhi)
   win.blit(label, (xp, yp))
   pygame.display.flip()


"""
curve: "p1707" => y^2 = x^3 + 0x + 7 (mod 17)
0 * G = (None, None)
1 * G = (15, 13) ok
2 * G = (2, 10) ok
3 * G = (8, 3) ?
4 * G = (12, 1)
5 * G = (6, 6)
6 * G = (5, 8)
7 * G = (10, 15)
8 * G = (1, 12)
9 * G = (3, 0)

---doubling---
0 15 13 ---start---
1 .  2 10 =
2 .  12 1 =
3 .  1 12 =
4 .  2 7 =
5 .  12 16 =
6 .  1 5 =

while True:
   time.sleep(1)
"""

print("-"*50)
print("--- tiny-ec ---")

field = SubGroup(p=p, g=(dx0, dy0), n=18, h=1)
curve = Curve(a=a, b=b, field=field, name='p1707')
print('curve:', curve)

for k in range(0, 10):
    p = k * curve.g
    print(f"{k} * G' = ({p.x}, {p.y})")


print("="*50)


time.sleep(60)

"""
y^2 = x^3 + 2x + 2 (mod 17)
(5,1) -> 6,3
"""
