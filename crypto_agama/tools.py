from datetime import *


def oeN2Wtest(num):
	print("---")
	print(num)
	print(hex(num))
	print(numtowif(num))
  
  
#----------------------log file--------------------------------
logFile = "log/"+datetime.now().strftime("%Y%m%d_%H%M%Slog.txt")
def addLog(co):
    fLog = open(logFile,"a") #a
    fLog.write(co+"\n")
    fLog.close()  


#------------------------substr----------------------------
def oeShort(s,l=12):
  return str(s[:l])+"..."+str(s[-l:])


#------------------------json tx---------------------------
def oeJTxSumVal(j):
  sumsat = 0
  for uval in j:
    sumsat =sumsat + uval["value"]
  return float(sumsat)/100000000


