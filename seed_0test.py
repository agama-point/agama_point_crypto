#!/usr/bin/env python3
# 2021-02 / 2023-06

from crypto_agama.agama_seed_tools import seed_words, mnemonic_info, words_to_4ch, mnemo_to_seed
from crypto_agama.agama_transform_tools import num_to_bin, bin_to_hex
from crypto_agama.tools import get_env_key
from lib.logger import logger_init


# debug logging 
log = logger_init(log_file='data/debug_seed.log')
log_msg = "[seet] test"
log.debug(log_msg)

bip39 = seed_words()


def word_test(w):
    print("-"*50)
    wnum = bip39.index(w)
    wbits = num_to_bin(wnum, True)
    print(wbits, w,wnum)
    w_hex = bin_to_hex(wbits)
    w_index = int(w_hex,16)
    print(wbits,w_index, bip39[w_index])


word_test("abandon")
word_test("name")
word_test("zoo")

"""
00000000000 abandon 0
--------------------------------------------------
10010010110 name 1174
--------------------------------------------------
11111111111 zoo 2047
"""

print("="*50)

try:
    print("-"*39)
    nkey_hex = get_env_key("KNH") # key nostr hexa
    print(nkey_hex)
except:
    print("Err. - set .env")

"""
Warning!
It's very important to know exactly what you're doing.
If possible, NEVER save seeds to your computer disk 
in a similar way. 
This is just a development and testing tool.
"""
print("--- test_seed_tools ---")
words_andreas = "army van defense carry jealous true garbage claim echo media make crunch"
log.debug("words_andreas")

mnemonic_info(words_andreas)

print(words_to_4ch(words_andreas, c=0))
print(words_to_4ch(words_andreas, c=13)) # caesar13
print(mnemo_to_seed(words_andreas).hex())

"""
--- test_seed_tools ---
--------------------------------------------------------------------------------
[mnemonic_info]
army van def... make crunch ( 12 )
96 1929 459 279 956 1866 764 333 559 1107 1076 423 
validate:  (True, True)
--------------------------------------------------------------------------------
army van defe carr jeal true garb clai echo medi make crun 
NEZL INA QRSR PNEE WRNY GEHR TNEO PYNV RPUB ZRQV ZNXR PEHA 
army van defe carr jeal true garb clai echo medi make crun 
NEZL INA QRSR PNEE WRNY GEHR TNEO PYNV RPUB ZRQV ZNXR PEHA 
4f2c76795aafb17902d7a3d8ff6db6c4158415e4ad996dec1b9d201f4285590ac0fa32ff057720e1a1dd087d6031e5cd37d67720da929869bf76118bb7215a3d

4f2c76795aafb17902d7a3d8ff6db6c4158415e4ad996dec1b9d201f4285590a Flat Felidae
c0fa32ff057720e1a1dd087d6031e5cd37d67720da929869bf76118bb7215a3d Cooing Gazelle
"""
