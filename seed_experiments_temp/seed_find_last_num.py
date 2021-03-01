#!/usr/bin/env python
# -*- coding: utf-8 -*-
# agama_point: find last word from seed (around 128 validated)
"""

1230123 > 123 01 23 (nula se nevypaří, je prefixem jednočíselného) 
vakantní jsou 10-199?

poslední slovo =/ nejblišší vyšší
? 123>122ok ale když 122 i 124 vyhrává 124

"""

from crypto_agama.tools import octopus_debug
from cryptos import * # pip install wheel, pbkdf2, cryptos
from crypto_agama.seed_tools import seed_words, mnemonic_info, words_to_4ch, generate_seed11_num_list
# from priv_data import get_words # words

start = time.time()
bip39 = seed_words()
words_test11 = "major easy ignore body rule stay gorilla eager arch actor scan "

# words_test11 = ""

num_str ="123 456 789 01 234 567 890 123 456 ..."
num_str ="123 456 789 012 345 678 901 234 ..."
last_num =123



num_arr = num_str.split()
print(num_arr)
# num_list = list([123,0,123,0,123,0])
num_list = list(num_arr)

words_test11 = generate_seed11_num_list(num_list)
print("words from num list: ", words_test11)



print("-"*30)
mnemonic_info(words_test11)
print("last: ", last_num, bip39[last_num])
print("check sum valid:")

num = 0
for word in bip39:
    words = words_test11 + word
    # print(words)
    if (keystore.bip39_is_checksum_valid(words)[0]):
        wi = bip39.index(word)
        print(num, wi, word, keystore.bip39_is_checksum_valid(words))
        num += 1

end = time.time() - start
print("=== duration (sec./min) --->", str(end), str(end/60))
