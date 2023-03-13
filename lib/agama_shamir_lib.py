# single shamir: 1-58f87a22d7aa12358e93a81e53217cb681bb4ec36b
# num-hexa (num max 9)

from lib.agama_transform_tools import hex_to_bin, num_to_bin, short_str
from lib.seed_english_words import english_words_bip39

__version__ = "0.2.3"

DEBUG = False
bip39 = english_words_bip39.split(",")


def single_shamir_to_words(s): # index and seed
    try:
        i = int(s[:1])
        if DEBUG: print("index", i)
    except:
        i = 99 

    s_hex = s[2:]    
    s_len = len(s_hex)
    if DEBUG: print("s_short", short_str(s_hex,6), s_len)
    
    s_bin_str = str(hex_to_bin(s_hex))[2:]
    if DEBUG: 
        print("s_bin_str:")
        print(s_bin_str)

    #prepare 11-bits
    len_bin = len(s_bin_str)
    num = int(len_bin/11)
    rest = len_bin-num*11

    if rest>0:
        print("rest / change")
        print(rest)
        num = num+1
        s_bin_str = s_bin_str + "0"*(11-rest)


    if DEBUG: print("len_bin, num, rest:",len_bin, num,rest)
    words = ""
    
    for i in range(int(num)): 
        bists11 = s_bin_str[i*11:i*11+11]
        num3 = int(bists11, 2)
        if DEBUG: print(i, bists11, num3)
  
        try:
            word = bip39[num3]
            words +=  word + " "
        except:
            word = "err"
        # print(i+1, num3, word)
  


    return i, rest, words   



def words_to_single_shamir(w, rest=0):
    s_bin_str = ""
    w_arr = w.split()
    for _w in w_arr:
        num = bip39.index(_w)
        bin_str = num_to_bin(num, True).rjust(11,"0")  

        if DEBUG: print(bin_str)
        s_bin_str += bin_str
        
    s_bin_str = s_bin_str[:len(s_bin_str)-11+rest]
    if DEBUG: print(s_bin_str)
    
    hex_str = hex(int(s_bin_str, 2)).lstrip("0x")

    return hex_str

"""
# test
s = "1-58f87a22d7aa12358e93a81e53217cb681bb4ec36b"
#      58f87a22d7aa12358e93a81e53217cb681bb4ec36b

print("-"*55)
print(s)
print("-"*55)
print(single_shamir_to_words(s))

words = 'rapid marble badge gadget drastic culture innocent tube device craft salad sure danger excite brave scale'

print(words_to_single_shamir(words,2))
"""
