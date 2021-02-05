#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crypto_agama.transform import seed_words


print("-"*30)
bip39 = seed_words()
testBip = bip39[777],bip39[333]
print("testBip: ", testBip)


lenArr = [0,0,0,0,0,0,0,0,0,0,0]
a1Dict = {}
anDict = {}
an = 3

print("-"*32) 

for word in bip39:
    lenw = len(word)
    ##    print(word, lenw)
    lenArr[lenw] += 1

    #if a1Dict[word[0]] in a1Dict.keys():
    if a1Dict.get(word[0])==None:
        a1Dict[word[0]] = 1
    else:       
        a1Dict[word[0]] += 1

    if anDict.get(word[0:an])==None:
        anDict[word[0:an]] = 1
    else:       
        anDict[word[0:an]] += 1
        
    

i = 0
for lenIt in lenArr:
    print(i, lenIt)
    i += 1

print("-"*32)    

for a1 in a1Dict:
    print(a1, a1Dict[a1])
  

print("-"*32)    

for ani in anDict:
    if anDict[ani]>1:
       print(ani, anDict[ani])
