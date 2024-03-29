#!/usr/bin/env python
# -*- coding: utf-8 -*-
from crypto_agama.seed_tools import seed_words, mnemonic_info, words_to_4ch

print("-"*30)
bip39 = seed_words()
testBip = bip39[777],bip39[333]
print("testBip: ", testBip)

from data import test
print("test.pk1: ",test.pk1)

from lib.tools import addLog
# addLog(test.pk1)

from crypto_agama.transform import *

passPhrase = "test 123"
hashStr = hashString(passPhrase)
print("hashStr:", hashStr)
num = int(hashStr,16)
print("num: ",num)


privateKey = numToWIF(num,"EF")
print("privateKey: ",privateKey)


# print(isValidWIF(privateKey))
##address = numToAddress(num)
