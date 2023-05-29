#!/usr/bin/env python
"""
basic tools 
$ pip install python-dotenv
"""
import os, sys
import time, datetime
from dotenv import load_dotenv
from datetime import *


DEBUG = True
WIDTH = 39


def get_env_key(key):
    load_dotenv()  # take environment variables from .env.

    if not os.environ.get(key):
        print("You need to set KEYs in .env file")
        sys.exit(1)
    return os.environ.get(key)


# ----log file---
logFile = "log/"+datetime.now().strftime("%Y%m%d_%H%M%Slog.txt")
def log_to_file(co):
    fLog = open(logFile,"a") #a
    fLog.write(co+"\n")
    fLog.close()


# ----json tx-----
def oeJTxSumVal(j):
  sumsat = 0
  for uval in j:
    sumsat =sumsat + uval["value"]
  return float(sumsat)/100000000
