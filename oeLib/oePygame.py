# octopusemgine.org - 2013-2017 --
# ------- matrix, font, images ---
# --------------------------------
# 0.1 - 2013/10 - testing pygame
# 0.2 - 2015/03 - 3DWARF
# 0.3 - 2016/09 - chceckbox and button
# 0.5 - 2017 - gr and crypto
#
# honza.copak@gmail.com
# --------------------------------

import pygame, random, sys, os, time
from pygame.locals import * # MOUSEBUTTONDOWN...
from datetime import datetime 
import pyqrcode #+pip install pypng

myDir = "data/"
myFont = pygame.font.SysFont("arial", 15) # monospace

colYel = (255,255,0)
colWhi = (255,255,255)
colRed = (255,0,0)
colBlu = (0,0,255)
colSil = (128,128,128)
colBla = (0,0,0) 
font={}  

hBod = 2
hA=300 #matice
hB=180
hW=hA*hBod #velikost
hH=hB*hBod
hX = hY = 0


def mxW(): return hA 	   
def mxH(): return hB 
def mxP(): return hBod       
##-----------------------------------------
def createQR(qrdata, qrscale):
   qr = pyqrcode.create(str(qrdata))
   qr.png(myDir+'tempqr.png', scale=qrscale) 

def nacist_font(jmenosouboru):
  #fontfile=file(jmenosouboru,"r")
  f = open(jmenosouboru, "r")
  fontfile= f.read()

  adresafontu=0
  for radka in fontfile:
    rozlozeno = radka.split(",")
    for bajt in range(5):
      font[adresafontu] = int(rozlozeno[bajt][-4:],0) # ulozeni kazdeho  bajtu do seznamu
      adresafontu = adresafontu + 1
  fontfile.close()

# myMatrix = [[0 for x in xrange(hA)] for x in xrange(hB)] 

def doHriste(window):
   # nacist_font("src/font.txt")
   pygame.draw.line(window,colRed,(hX,hY),(hX,hY+hH),hBod)
   pygame.draw.line(window,colRed,(hX,hY+hH),(hX+hW,hY+hH),hBod)
   pygame.draw.line(window,colRed,(hX+hW,hY+hH),(hX+hW,hY),hBod)
   pygame.draw.line(window,colRed,(hX+hW,hY),(hX,hY),hBod)
   pygame.display.flip()

##-----------------------------------------
def setMat(myMatrix,how): # 0 for clear, 7 for black
  for x in range(hA):
    for y in range(hB):
      myMatrix[x,y]= how

def copyMat(myMatrix,myMatrix2):
  for x in range(hA):
    for y in range(hB):
      myMatrix2[x,y]= myMatrix[x,y]

def restoreMat(myMatrix,myMatrix2):
  for x in range(hA):
    for y in range(hB):
      myMatrix[x,y]= myMatrix2[x,y]

def invertMat(myMatrix):
  for x in range(hA):
    for y in range(hB):
      if (myMatrix[x,y]):
         myMatrix[x,y]= 0                  
      else:
         myMatrix[x,y]= 7  

def noiseMat(myMatrix):
  for x in range(hA):
    for y in range(hB):
      if (int(random.random()+0.5)):
         myMatrix[x,y]= 0                  
      else:
         myMatrix[x,y]= 7   
         
def addnoiseMat(myMatrix):
  for x in range(hA):
    for y in range(hB):
      #if (int(random.random())):   # dvoubarevna windowsovska bitmapa ma opacne nastavene bity nez displej:
      if (int(random.random()+0.5)):
         myMatrix[x,y]= myMatrix[x,y]                  
      else:
         myMatrix[x,y]= 7
  
def creaMatSil(myMatrix):
  for x in range(hA/2):
    for y in range(hB/2):
      suma = myMatrix[x*2,y*2]+myMatrix[x*2+1,y*2]+myMatrix[x*2,y*2+1]+myMatrix[x*2+1,y*2+1]
      sil = 3
      if suma > 20:
        sil = 7
      if suma <8:
        sil = 0
      myMatrix[x,y]= sil

def creaMatFilt(myMatrix,myMatrixFilt):
  for x in range(hA/2):
    for y in range(hB/2):
      myMatFilt[x,y]= 0 
  for x in range(2,hA/2-1):
    for y in range(2,hB/2-1):
      suma = myMatrix[x*2,y*2]
      suma = suma + myMatrix[x*2+1,y*2]+myMatrix[x*2,y*2+1]+myMatrix[x*2+1,y*2+1]
      suma = suma + myMatrix[x*2-1,y*2]+myMatrix[x*2,y*2-1]+myMatrix[x*2-1,y*2-1]
      suma = suma + myMatrix[x*2-1,y*2+1]+ myMatrix[x*2+1,y*2-1]
      myMatFilt[x,y]= round(suma/9,1)

def plotMatSil(window,pozX,pozY):
  for x in range(hA/2):
    for y in range(hB/2):
      mem_plot(window,pozX+x,pozY+y,myMatSil[x,y])
  pygame.display.flip()        

def plotMatFilt(window,pozX,pozY):
  for x in range(hA/2):
    for y in range(hB/2):
      mem_plotCol(window,pozX+x,pozY+y,myMatFilt[x,y])
  pygame.display.flip()     
      
def mem_plot(window,x,y,co):
   colCase = colSil
   if co==0:
       colCase = colWhi
   if co==7:
       colCase = colBla       
   pygame.draw.line(window,colCase,(x*hBod+hX,y*hBod+hY),(x*hBod+1+hX,y*hBod+1+hY),hBod)

def mem_plotCol(window,x,y,co):
   colCase = colSil
   if co<3:
       colCase = colYel
   if co>3 and co<6:
       colCase = colBlu       
   if co>6:
       colCase = colRed       
   pygame.draw.line(window,colCase,(x*hBod+hX,y*hBod+hY),(x*hBod+1+hX,y*hBod+1+hY),hBod)
   
def plotMat(window,myMatrix):
  for x in range(hA):
    for y in range(hB):
      mem_plot(window,x,y,myMatrix[x,y])
  pygame.display.flip()     


# one character - position superx (0 - 119) rpw (0 - 7)
def mxChar(window,myMatrix,kod , superx , r , inverze=False):
    adr_fontu = (kod-32) * 5  # ukazatel na zacatek petice bajtu prislusneho znaku
    # nastaveni pozice leve strany znaku (prvniho prenaseneho bajtu) do prislusneho kvadrantu

    for f in range(5):       
        if (inverze == False): # podle inverze bud prekopirovat na displej bajt z fontu, nebo ten bajt jeste invertovat
          bajt = font[adr_fontu + f]          
        else:
          bajt = ~(font[adr_fontu + f])
         #print "b" + str(adr_fontu) +" B:" +str(bajt)+ " f " + str(f)

        for b in range(8):
            zx = superx+f       # s = osmibodovy sloupec na displeji (0 az 14) , b = bit v kazdem bajtu 0 az 7
            zy = r - b+8              # r = mikroradka na displeji 0 az 63
            maska = (1 << (7-b))   
            #kazdy bit z grafickych dat se na prislusne pozici na displeji (resp. v promenne mapa[]) bud rozsviti, nebo zhasne
            if ((bajt & maska) != 0):   # dvoubarevna windowsovska bitmapa ma opacne nastavene bity nez displej:
              myMatrix[zx,zy]= 7 
              mem_plot(window,zx,zy,1)          # jednickove bity jsou bile body             
            else:
              myMatrix[zx,zy]= 0  
              mem_plot(window,zx,zy,0)          # nulove bity jsou cerne body        
    
# vytisknuti nekolika pismen za sebou oddelenych nastavitelnou mezerou 
def mxStr(window,myMatrix,text, superx , radka, mezera=1 , inverze=False):
  global stara_lr
  #if (isinstance(text, unicode) == False):  # pokud text neni v unicode, tak ho preved
  #  text=  unicode(text, "utf-8")           # prevod textu z UTF-8 na unicode

  for zn in range (len(text)):
    if (ord(text[zn:zn + 1]) > 127):   # pokud jde o neASCII znak, provest prekodovani podle tabulky
      try:                    # pokud neni specialni kod nadefinovany v tabulce, ...
        mxChar(window,myMatrix,cz[ord(text[zn:zn + 1])], superx, radka, inverze)
      except:                 # ... cz[] index.
        mxChar(window,myMatrix,177, superx, radka, inverze)  #   
    else:
      mxChar(window,myMatrix,ord(text[zn:zn + 1]), superx, radka, inverze) # ASCII 32-127 normal 
    # za kazdym znakem vytisknout patricny pocet mezer (sirka mezery 1 bod)
    for m in range(mezera):
      if (superx + m + 5 < 300):  # < 120 matrix width?
          superx= superx + 5 + mezera   # dalsi znak se tiskne az za mezerou 
  pygame.display.flip() 


def saveImg(window,sizeX, sizeY):   
   timeStamp=datetime.now().strftime("%Y/%m/%d_%H:%M:%S")
   #label = myFont.render(timeStamp, 1, (255,255,255))
   #window.blit(label, (sizeX-200, sizeY-50))
   fileName = myDir+datetime.now().strftime("%Y%m%d_%H%M%S") +'.png'
   pygame.image.save(window,fileName)
   
def saveJpg(window,fileJpg,sizeX, sizeY):   
   #timeStamp=datetime.now().strftime("%Y/%m/%d_%H:%M:%S")
   #fileName = myDir+datetime.now().strftime("%Y%m%d_%H%M%S") +'.jpg'
   pygame.image.save(window,fileJpg)   

def saveMat(window,filePng,myMatrix):
   for y in range(hB):
    for x in range(hA):
         co = myMatrix[x,y]
         colCase = colSil
         if (co==0):
           colCase = colWhi
         if co==7:
           colCase = colBla       
         pygame.draw.line(window,colCase,(x,y),(x+1,y+1),1)
   #fileName = myDir+datetime.now().strftime("%Y%m%d_%H%M%S") +'.png'
   pygame.image.save(window,filePng)
   
def infoMat(myMatrix,sel,how): # 0 for clear, 7 for black
  nlines = 3 
  # 7 lines init noise
  for y in range(nlines+3):
    for x in range(hA): 
         if (int(random.random()+0.5)):  
              myMatrix[x,y]= 0                  
         else:
              myMatrix[x,y]= 7
               
  # main data (max nlines lines) 
  ih=0
  ihmax = len(str(how))
  print("ihmax:"+str(ihmax))
  for y in range(nlines):
    for x in range(hA):
      ih=ih+1
      if (sel==3):
         if (x%2):    
            myMatrix[x,y]= 0
         else:    
            myMatrix[x,y]= 7      
      else:
       if (ih<ihmax+3):  
        try:
          if (str(how)[ih+2]=="0"):
             myMatrix[x,y]= 0
          else:    
             myMatrix[x,y]= 7
        except:
          err=True
       
def loadMat(window,filePng,myMatrix,sel):
   expBin = "000" ##"0b"
   ib=0
   obr = pygame.image.load(filePng)
   obrRect = obr.get_rect()
   window.blit(obr, obrRect)    
   #pygame.display.flip()
   for y in range(hB):  
    for x in range(hA):  
       cR = window.get_at((x,y))[0] # get RGB of one pixel from camera-image 
       cG = window.get_at((x,y))[1]
       cB = window.get_at((x,y))[2]
       getRGB=cR+cG+cB

       if (getRGB <399):  # 765/384
          myMatrix[x,y]= 7
          expBin = expBin+"1"
       else:      
          myMatrix[x,y]= 0
          expBin = expBin+"0"
       ib=ib+1
       if (ib>1024): ib=1024
   return expBin          
        
def loadMatQR(window,filePng,myMatrix,dx,dy): #  invert
   obr = pygame.image.load(filePng)
   obrRect = obr.get_rect()
   iw = obr.get_width()
   ih = obr.get_height()
   window.blit(obr, obrRect)    
   #pygame.display.flip()
   for y in range(ih):
    for x in range(iw):  #hB
       cR = window.get_at((x,y))[0] # get RGB of one pixel from camera-image 
       cG = window.get_at((x,y))[1]
       cB = window.get_at((x,y))[2]
       getRGB=cR+cG+cB

       if (getRGB <399):  # 765/384
          myMatrix[x+dx,y+dy]= 7          
       else:      
          myMatrix[x+dx,y+dy]= 0          
                 
def doBmp128x128(co):
    jmeno_obrazku=co
    soubor=open(jmeno_obrazku, "rb")  # nacteni obrazku do promenne data[]
    data = soubor.read()  
    soubor.close()                    # uzavreni souboru

    # http://www.root.cz/clanky/graficky-format-bmp-pouzivany-a-pritom-neoblibeny
    # zacatek obrazovych dat urcuji 4 bajty v souboru na pozicich 10 az 13 (desitkove) od zacatku souboru
    zacatekdat = ord(data[10]) + (ord(data[11]) * 256) + (ord(data[12]) * 65536) + (ord(data[13]) * 16777216)
    bajt=zacatekdat
    for r in range (127,-1,-1):     # cteni promenne data[] bajt po bajtu a prevod na souradnice superx,supery
                                # 0 az 127 (128 radku)
        for s in range (16):
          for b in range(8):
            zx = (s*8) + b      # s = osmibodovy sloupec na displeji (0 az 14) , b = bit v kazdem bajtu 0 az 7
            zy = r              # r = mikroradka na displeji 0 az 63
            maska = (1 << (7-b))   
            #kazdy bit z grafickych dat se na prislusne pozici na displeji (resp. v promenne mapa[]) bud rozsviti, nebo zhasne
            if (ord(data[bajt]) & maska != 0):   # dvoubarevna windowsovska bitmapa ma opacne nastavene bity nez displej:
              #myMatrix[zx,zy]= 0 
              mem_plot(zx,zy,0)          # jednickove bity jsou bile body             
            else:
              #myMatrix[zx,zy]= 1  
              mem_plot(zx,zy,1)          # nulove bity jsou cerne body
          bajt = bajt +1
    pygame.display.flip()

def doBmp2Mat(myMatrix,co,pozx,pozy):
    jmeno_obrazku=co
    soubor=open(jmeno_obrazku, "rb")  # nacteni obrazku do promenne data[]
    data = soubor.read()  
    soubor.close()                    # uzavreni souboru

    # http://www.root.cz/clanky/graficky-format-bmp-pouzivany-a-pritom-neoblibeny
    # zacatek obrazovych dat urcuji 4 bajty v souboru na pozicich 10 az 13 (desitkove) od zacatku souboru
    zacatekdat = ord(data[10]) + (ord(data[11]) * 256) + (ord(data[12]) * 65536) + (ord(data[13]) * 16777216)
    bajt=zacatekdat
    for r in range (127,-1,-1):     # cteni promenne data[] bajt po bajtu a prevod na souradnice superx,supery
                                # 0 az 127 (128 radku)
        for s in range (16):
          for b in range(8):
            zx = pozx+(s*8) + b      # s = osmibodovy sloupec na displeji (0 az 14) , b = bit v kazdem bajtu 0 az 7
            zy = pozy+r              # r = mikroradka na displeji 0 az 63
            maska = (1 << (7-b))   
            #kazdy bit z grafickych dat se na prislusne pozici na displeji (resp. v promenne mapa[]) bud rozsviti, nebo zhasne
            if (ord(data[bajt]) & maska != 0):   # dvoubarevna windowsovska bitmapa ma opacne nastavene bity nez displej:
              myMatrix[zx,zy]= 0 
               #mem_plot(zx,zy,0)          # jednickove bity jsou bile body             
            else:
              myMatrix[zx,zy]= 7  
               #mem_plot(zx,zy,1)          # nulove bity jsou cerne body
          bajt = bajt +1
     #pygame.display.flip()
     
# noise
def doNoise2Mat(myMatrix,pozx,pozy):
  #x= int(random.random() * 84)
  for r in range (127,-1,-1):     # cteni promenne data[] bajt po bajtu a prevod na souradnice superx,supery
      for s in range (16):
          for b in range(8):
            zx = pozx+(s*8) + b      # s = osmibodovy sloupec na displeji (0 az 14) , b = bit v kazdem bajtu 0 az 7
            zy = pozy+r              # r = mikroradka na displeji 0 az 63
            maska = (1 << (7-b))   
            #kazdy bit z grafickych dat se na prislusne pozici na displeji (resp. v promenne mapa[]) bud rozsviti, nebo zhasne
            if (int(random.random())):   # dvoubarevna windowsovska bitmapa ma opacne nastavene bity nez displej:
              myMatrix[zx,zy]= 0                  
            else:
              myMatrix[zx,zy]= 7              
          #bajt = bajt +1  

##==================================================================
class CheckBox(object): 
  def __init__(self, window,x, y, a=20):
    self.stav = False      
    self.window = window
    self.a = a
    self.x = x
    self.y = y
    
    self.myFont = pygame.font.SysFont("monospace", 15)
    self.colYel = (255,255,0)
    self.colWhi = (255,255,255)
    self.colRed = (255,0,0)
    self.colBlu = (0,0,255)
    self.colSil = (128,128,128)
    self.colBla = (0,0,0) 
    
    self.backgroundcolor = 0, 128, 0
    self.clickedcolor = 0, 255, 255
    self.unclickedcolor = 255,255,255
    self.GRID_SQUARE_SIZE = (a, a)
    self.drawChBox()
    
  def initChBox(self, text):
    label = self.myFont.render(text, 1, self.colWhi)
    self.window.blit(label, (self.x+self.a+7, self.y+3))
    self.drawChBox()
       
  def drawChBox(self):
    colYel = (255,255,0)
    colWhi = (255,255,255)
    colRed = (255,0,0)
    colBlu = (0,0,255)
    colSil = (128,128,128)
    colBla = (0,0,0) 
    if self.stav:
      pygame.draw.rect(self.window, self.colWhi, (self.x,self.y,self.a,self.a), 2)
      pygame.draw.line(self.window, self.colWhi,(self.x,self.y),(self.x+self.a-1,self.y+self.a),2)
      pygame.draw.line(self.window, self.colWhi,(self.x,self.y+self.a),(self.x+self.a-1,self.y),2)
    else:
      pygame.draw.line(self.window, self.colBla,(self.x,self.y),(self.x+self.a-1,self.y+self.a),2)
      pygame.draw.line(self.window, self.colBla,(self.x,self.y+self.a),(self.x+self.a-1,self.y),2)
      pygame.draw.rect(self.window, self.colSil, (self.x,self.y,self.a,self.a), 2)
    pygame.display.flip()  

  def setChBox(self, x, y): #this is going to be the clicked class or maybe the clicked class will call this
    if x>self.x and x<self.x+self.a:
       if y>self.y and y<self.y+self.a:
          self.stav = not self.stav
          self.drawChBox()
          
  def getChBox(self): 
      return self.stav

##==================================================================
class ButtBox(object):
  def __init__(self, window,x, y, a=22,b=80):
    self.stav = False 
    self.window = window     
    self.a = a
    self.b = b
    self.x = x
    self.y = y
    
    #self.myFont = pygame.font.SysFont("monospace", 15)
    # pygame.font.SysFont('arial', size)
    self.myFont = pygame.font.SysFont("arial", 15)
    self.colYel = (255,255,0)
    self.colWhi = (255,255,255)
    self.colRed = (255,0,0)
    self.colBlu = (0,0,255)
    self.colSil = (128,128,128)
    self.colBla = (0,0,0) 
      
    self.drawButt()
    
  def labelButt(self, text):
    label = self.myFont.render(text, 1, self.colWhi)
    self.window.blit(label, (self.x+5, self.y+3))
    self.drawButt()
       
  def drawButt(self):      
    pygame.draw.rect(self.window, self.colSil, (self.x,self.y,self.b,self.a), 2)
    pygame.display.flip()  
   
  def drawButtClick(self):    
    pygame.draw.rect(self.window, self.colWhi, (self.x,self.y,self.b,self.a), 2)
    pygame.display.flip()  

  def testClickButt(self, x, y): #this is going to be the clicked class or maybe the clicked class will call this
    self.klik = False 
    if x>self.x and x<self.x+self.b:
       if y>self.y and y<self.y+self.a:          
          self.stav = not self.stav
          self.drawButtClick()
          time.sleep(0.2)
          self.drawButt()
          self.klik = True
    return self.klik          
              
##==================================================================  
