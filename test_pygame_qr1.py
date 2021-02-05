# -*- coding: cp1250 -*-
#-----------------------
# 2017/11/14 - v01.ok
# 2021/01 - fork: virtual_coin
ver="2021-01" # show w+pk

from crypto_agama.agama_cryptos import create_wallet
from crypto_agama.transform import short_str

from priv_data import get_words # words
import sys, os, time, random
import pygame, pyqrcode 
from pygame.locals import * # MOUSEBUTTONDOWN...
from json import *
from datetime import datetime 


coin = "tBTC" #LTC,NMC,VTC
words = get_words()
words_arr = words.split()
note = words_arr[0] + "|" + words_arr[11]

# words = "..."
print(words)
wnum = 0

startTime = time.time()

from oeLib.oePygame import *
pygame.init()

myMatrix={}     # main
font={}             # font from extern file
myMatSil={}     # 
myMatFilt={}    # filt   

myDir = "data/"
notePrefix="B.test:"
logTime = datetime.now().strftime("%Y%m%d_%H%M%S") 
logFile = myDir+logTime+"log.txt"
fileJpg = myDir+logTime+".jpg"
filePng = myDir+logTime+".png"
filetPng = myDir+"temp.png"

myFont = pygame.font.SysFont("monospace", 15)

# Set up some variables containing the screeen size
sizeWinX=900
sizeWinY=500

colYel = (255,255,0)
colWhi = (255,255,255)
colRed = (255,0,0)
colBlu = (0,0,255)
colSil = (128,128,128)
colBla = (0,0,0)

hA= mxW() #main matrix width
hB= mxH() #main matrix height
hBod = mxP()
hW=hA*hBod #velikost
hH=hB*hBod
hX=0   #pozice
hY=0
mxx = 7 #matrix offset
mxy = 128

winMat = pygame.display.set_mode([hA,hB]) # Create the pygame matrix window
win = pygame.display.set_mode([sizeWinX,sizeWinY]) # Create the pygame window
pygame.display.set_caption("oeVirtualCoin")

##==================================================================
cisloCrypto = 123456789

butty = 35
bty = 10
btx1 = 660
btx2 = btx1+100
chy = 390
chyc = chy+35
ch1 = CheckBox(win,200,chy);ch1.initChBox("select 0")
ch2 = CheckBox(win,330,chy);ch2.initChBox("select 1")
ch3 = CheckBox(win,460,chy);ch3.initChBox("select 2")

ch1c = CheckBox(win,200,chyc);ch1c.initChBox("LTC")
ch2c = CheckBox(win,330,chyc);ch2c.initChBox("tLTC")
ch3c = CheckBox(win,460,chyc);ch3c.initChBox("BTC")
ch4c = CheckBox(win,590,chyc);ch4c.initChBox("tBTC")

bt1 = ButtBox(win,btx1,bty);bt1.labelButt("clear")
bt3 = ButtBox(win,btx1,bty+butty);bt3.labelButt("invert")
bt5 = ButtBox(win,btx1,bty+butty*2);bt5.labelButt("noise")

bt7 = ButtBox(win,btx1,bty+butty*3);bt7.labelButt("octop")
bt9 = ButtBox(win,btx1,bty+butty*4);bt9.labelButt("world")
bt11 = ButtBox(win,btx1,bty+butty*5);bt11.labelButt(">info1")
bt13 = ButtBox(win,btx1,bty+butty*6);bt13.labelButt("info2")
bt15 = ButtBox(win,btx1,bty+butty*7);bt15.labelButt(">qr1")
bt17 = ButtBox(win,btx1,bty+butty*8);bt17.labelButt("qr2")

bt2 = ButtBox(win,btx2,bty);bt2.labelButt("save")
bt4 = ButtBox(win,btx2,bty+butty);bt4.labelButt("load")
bt6 = ButtBox(win,btx2,bty+butty*2);bt6.labelButt("> gen1 <")
bt8 = ButtBox(win,btx2,bty+butty*3);bt8.labelButt("gen2")
bt10 = ButtBox(win,btx2,bty+butty*4);bt10.labelButt("test")
bt12 = ButtBox(win,btx2,bty+butty*5);bt12.labelButt("quit")

def clickOctop():
  doBmp2Mat(myMatrix,"src/o128i.bmp",10,0)
  print("time>" + str(time.time()-startTime))
  print("printMat>")
  plotMat(win,myMatrix)
  print("time plot>" + str(time.time()-startTime))

def clickGen1(coin):
        passphrase = ""
        global pcoin,wcoin
        print("---gen1--- cioin: ", coin, wnum)
        
        print("time info>" + str(time.time()-startTime))
        
        # w = create_wallet(words,coin,wnum)
        w = create_wallet(words, passphrase=passphrase, c=coin, wnum=wnum)
        print("root_key: ", w[3]) # create_root_key(seed_bytes)

        wcoin = w[0]
        pcoin = w[1]
        print("wallet-pubk: ",wcoin, w[2])
        print("wallet-priv: ", wcoin)

def clickQr1():
        setMat(myMatrix,0)
        ## mxStr(win, myMatrix,coin,mxx,mxy)
        """
        mxStr(win, myMatrix,coin+".test: "+logTime,mxx,mxy)
        mxStr(win, myMatrix,wcoin,mxx,mxy+10)
        mxStr(win, myMatrix,ver,mxx,mxy+20)
        #mxStr(win, myMatrix,(wbtc+wbtc),5,161)
        mxStr(win, myMatrix,oeShort(pcoin,17),mxx,mxy+30)
        mxStr(win, myMatrix,"octopusEngine",mxx,mxy+40)
        """
        filetPng = myDir+"tempqr.png" 
        qrx=5
        qry=3

        time.sleep(2)

        createQR(wcoin,2) # size 2/3
        ## addLog(logFile,wcoin)
        loadMatQR(win,filetPng,myMatrix,100,qry)
        obr = pygame.image.load(filetPng) 
        obrRect = obr.get_rect()
        obrRect = obrRect.move(200,0) #hX*2+100
        win.blit(obr, obrRect)
        
        ## addLog(logFile,pcoin)
        createQR(pcoin,2)
        loadMatQR(win,filetPng,myMatrix,qrx,qry)
        obr = pygame.image.load(filetPng)
        obrRect = obr.get_rect()
        obrRect = obrRect.move(10,0)
        win.blit(obr, obrRect)

        plotMat(win,myMatrix)

        laby = 200
        label = myFont.render(coin + " ("+ str(wnum) +")  | " + note + " | " + logTime, 1, colBla)
        win.blit(label, (30, laby))
        label = myFont.render(wcoin, 1, colBla)
        win.blit(label, (30, laby+12))
        label = myFont.render(short_str(pcoin,16), 1, colBla)
        win.blit(label, (30, laby+25))
        doHriste(win) # ?

        createQR("123456789",1) #reset temp


def clickInfo():
        print("---save---info---")
        
        print("wallet-pubk: ",wcoin, w[2])
        print("wallet-priv: ", wcoin)
        
        if (ch1.getChBox()): #sel1=test	
                #infoMat(myMatrix,sel,"0b01010100110011001100000111110101010101")
                infoMat(myMatrix,sel,strtobin7(teststr))
                print(teststr)
                print(trtobin7(teststr)[:100])	
        else:
                infoMat(myMatrix,sel,testbPrefix+strtobin7(strsave))
                #print(cisloCrypto)
                print(strsave)
                print(testbPrefix+strtobin7(strsave)[:100])
        plotMat(win,myMatrix)
        print("time info save>" + str(time.time()-startTime))

def startWin():
        print("clrMat>")
        setMat(myMatrix,0)
        print("time>" + str(time.time()-startTime))
        print("printMat>")
        plotMat(win,myMatrix)
        print("time>" + str(time.time()-startTime))

        label = myFont.render("test Virtual Coin", 1, colYel)
        win.blit(label, (chy, 10))

        ## hriste
        print("hriste>")
        doHriste(win)
"""
        print("test znak a slovo>")
        mxChar(win, myMatrix,51,220,10,inverze=False)
        mxStr(win, myMatrix,"IMAGE text TEST",5,135)
        co = "size:" + str(hA)+"x"+str(hB)
        mxStr(win, myMatrix,co,5,145)
        mxStr(win, myMatrix,wbtc,5,155)  
        clickOctop()
"""

#hBod=2
#creaMatSil()
#plotMatSil(300,70)

#pygame.quit()
#----------------------------------------------------------------------------

startWin()
clickGen1(coin)

while True:
   #time.sleep(1)
   for event in pygame.event.get():
     if event.type == MOUSEBUTTONDOWN:
        x, y = event.pos
        ch1.setChBox(x,y)
        ch2.setChBox(x,y)
        ch3.setChBox(x,y)
        wnum = 0
        if (ch1.getChBox()): wnum = 0
        if (ch2.getChBox()): wnum = 1
        if (ch3.getChBox()): wnum = 2
        if (ch2.getChBox() and ch3.getChBox()): wnum = 3
        ch1c.setChBox(x,y)
        ch2c.setChBox(x,y)
        ch3c.setChBox(x,y)
        ch4c.setChBox(x,y)

        if (ch1c.getChBox()): coin = "LTC"
        if (ch2c.getChBox()): coin = "tLTC"
        if (ch3c.getChBox()): coin = "BTC"
        if (ch4c.getChBox()): coin = "tBTC"
        
        if bt1.testClickButt(x,y): #clear
                setMat(myMatrix,0)
                plotMat(win,myMatrix)
                print("time clear>" + str(time.time()-startTime)) 
        
        if bt3.testClickButt(x,y): #invert
                #mxStr(win, myMatrix,"invert",5,155)
                invertMat(myMatrix)
                plotMat(win,myMatrix)
                print("time inv>" + str(time.time()-startTime))

        if bt5.testClickButt(x,y): #noise
                addnoiseMat(myMatrix)
                #mxStr(win, myMatrix,"noise",5,155)
                plotMat(win,myMatrix)
                print("time noise>" + str(time.time()-startTime)) 

        if bt7.testClickButt(x,y): #octop
                clickOctop()

        if bt9.testClickButt(x,y): #world		
                doBmp2Mat(myMatrix,"src/world128x64i.bmp",10,0)
                plotMat(win,myMatrix)

        if bt11.testClickButt(x,y): #info save
                clickInfo() 

        if bt4.testClickButt(x,y): #info load
                print("---load---info---")
                myBin = loadMat(win,filetPng,myMatrix,sel)
                print("load bin: ")
                print(myBin[:256])
                #hexinfo=bin8tohex(myBin[:160])
                print("load > "+bin7tostr(myBin[:512]))
                #print("hex:"+hexinfo)
                #print("int:"+str(int(hexinfo, base=16)))
                plotMat(win,myMatrix)
                print("time info>" + str(time.time()-startTime))

        if bt6.testClickButt(x,y):
                clickGen1(coin)
                clickQr1()

        if bt15.testClickButt(x,y):  # qr1 test wallet 
                clickQr1()

        if bt17.testClickButt(x,y): #qr2
                setMat(myMatrix,0) #clear
                clickQr1()
                doBmp2Mat(myMatrix,"src/world128x64i.bmp",10,0)
                clickInfo() 
                plotMat(win,myMatrix)
        
        if bt10.testClickButt(x,y):
                print("---test unspent---")
                if (ch1.getChBox()):
                  h = history(wcoin)
                  print(h)
                  u = unspent(wcoin)
                  print(u)
                sumUnsp = str(oeJTxSumVal(unspent(wcoin)))
                print(oeShort(wcoin,8)+" > "+sumUnsp)
                #mxStr(win, myMatrix,"("+sumUnsp+")",5,mxy+20)
                clickQr1()
                mxStr(win, myMatrix,wcoin+" ("+sumUnsp+")",mxx,mxy+10)
                plotMat(win,myMatrix)

        if bt2.testClickButt(x,y):
                fileName = myDir+logTime+"_"+coin+str(wnum)
                fileJpg = fileName+".jpg"
                filePng = fileName+".png"
                print("filePng: ",filePng)
                saveJpg(win,fileJpg,sizeWinX, sizeWinY)
                print("save.ok")
                """
                if (ch1.getChBox()):
                  saveJpg(win,fileJpg,sizeWinX, sizeWinY)
                else: 
                  winMat = pygame.display.set_mode([hA,hB]) # Create the pygame matrix window
                  #plotMat(winMat,myMatrix)
                  saveMat(winMat,filePng,myMatrix)
                  saveMat(winMat,filetPng,myMatrix)
                  print("---ok-save: "+filePng)
                  win = pygame.display.set_mode([sizeWinX,sizeWinY]) # Create the pygame window
                  win.fill(colBla)
                  pygame.display.flip
                  startWin()
                  """

     if event.type == pygame.QUIT:
                  sys.exit()
