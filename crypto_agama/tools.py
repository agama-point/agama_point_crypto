from datetime import *


#----------------------log file--------------------------------
logFile = "log/"+datetime.now().strftime("%Y%m%d_%H%M%Slog.txt")
def log_to_file(co):
    fLog = open(logFile,"a") #a
    fLog.write(co+"\n")
    fLog.close()


#------------------------json tx---------------------------
def oeJTxSumVal(j):
  sumsat = 0
  for uval in j:
    sumsat =sumsat + uval["value"]
  return float(sumsat)/100000000


