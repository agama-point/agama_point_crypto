from crypto_agama.agama_transform_tools import decimal_to_base, base_to_decimal, hex_to_num, hex_to_bin
from crypto_agama.agama_seed_tools import seed_words, mnemonic_info
# from cryptos.mnemonic import mnemonic_int_to_words, entropy_to_words
from crypto_agama.agama_seed_tools import BIP39Functions, entropy_normalize, seed_words


"""
https://iancoleman.io/bip39/ test

 *Binary [0-1] 101010011
 *Base 6 [0-5] 123434014
 *Dice [1-6] 62535634
 *Base 10 [0-9] 90834528
 *Hex [0-9A-F] 4187a8bfd9
 **Card [A2-9TJQK][CDHS] ahqs9dtc

iancoleman vs. agama DICE > num to base5 + 11111
msg:=CEIAVPGIREVPR
>>> print(base_to_decimal(str(11112-11111), 5))
1
"""

print("-"*32)
print("[ --- test entropy --- ]")

"""
Use Raw Entropy (3 words per 32 bits) / PBKDF2 rounds: 2048 compatib.
generate ->
canvas sweet wear leisure donkey enforce menu category offer cricket execute cost
*focus flat angry dilemma canvas sweet wear leisure donkey enforce basic trial

Filtered Entropy Hex [0-9A-F]
21bb77e1bfd4129462c92199666d3c98
*5a2b10239f121bb77e1bfd4129444c74

fe10 (base10)?
44837914865895653720085525775973694616
*119854115726328780690431313048557202615

*
Raw Binary
01011010001 01011000100 00001000111 00111110001 00100001101 11011011101 11111000011 01111111101 01000001001 01001010001 00010011000 1110100
Binary Checksum
0001

Word Indexes
                    269, 1757, 1987, 1021, 521, 593, 1113, 289, 1227, 411, 633, 389
*721, 708, 71, 497, 269, 1757, 1987, 1021, 521, 593, 152, 1857

bip39 vectors: https://github.com/trezor/python-mnemonic/blob/master/vectors.json

"80808080808080808080808080808080"
"letter advice cage absurd amount doctor acoustic avoid letter advice cage above"

"""
def seed_test(entropy, passphrase=""):
    print()
    print("="*50, len(entropy))

    entropy = entropy_normalize(entropy)
    bin_entropy = hex_to_bin(entropy)
    
    print("input entropy:", entropy)
    print("binary:", bin_entropy)

    hashes = BIP39Functions()
    phrase = hashes.entropy_to_phrase(entropy)
    print("BIP39Functions - phrase:",phrase)
    print("is_valid | reverese_entropy:", hashes.is_checksum_valid(phrase, reverse_entropy=True))
    mnemonic_info(phrase)
    return phrase

bip39 = bip39 = seed_words()

def mnemo_to_nums(words):
    print("[mnemo_to_nums]")
    num_list = [] 
    w_arr = words.split() # words_to_array
    print("(",len(w_arr),")")

    for _w in w_arr:
        _wnum = bip39.index(_w)
        print(_w, _wnum, end=" | ")
        num_list.append(_wnum)
    
    return num_list


# ============================================================================================
en_hex = "5a2b10239f121bb77e1bfd4129444c74"
# en_hex = "80808080808080808080808080808080"

# words = entropy_to_words(en_hex)
words = seed_test(en_hex)

# print("hex_to_num",hex_to_num(en_hex)) # = binary
w12 = words # "focus flat angry dilemma canvas sweet wear leisure donkey enforce basic trial"

nums12 = mnemo_to_nums(words) # [721, 708, 71, 497, 269, 1757, 1987, 1021, 521, 593, 152, 1857]

print("--- 5 ---")
base = 5
for number in nums12: 
    #decimal_number = base_to_decimal(str(number), base)
    cislo_petkova = decimal_to_base(number,base)
    print(cislo_petkova, end=" ")

print("\n--- DICE ---")
base = 6
for number in nums12: 
    #decimal_number = base_to_decimal(str(number), base)
    cislo_petkova = int(decimal_to_base(number,base)) + 11111 # 0->1, ...5->6
    print(cislo_petkova, end=" ")

print("\n--- 6 --- ")
base = 6
for number in nums12: 
    #decimal_number = base_to_decimal(str(number), base)
    cislo_sestkova = decimal_to_base(number,base)
    print(cislo_sestkova, end=" ")

"""
[mnemonic_info]
focus flat a... basic trial ( 12 )
721 708 71 497 269 1757 1987 1021 521 593 152 1857
validate:  (True, True)
--------------------------------------------------------------------------------
 --- 5 ---
10341 10313 00241 03442 02034 24012 30422 13041 04041 04333 01102 24412
--- DICE ---
14312 14251 11266 13256 12236 23156 24222 15532 13336 13536 11523 23444
--- 6 ---
03201 03140 00155 02145 01125 12045 13111 04421 02225 02425 00412 12333

"""

print("\n --- DICE to num ---")

dice12 = "14312 14251 11266 13256 12236 23156 24222 15532 13336 13536 11523 23444"
number_list = [int(num) for num in dice12.split()]
print(number_list)

for number in number_list:
    dice_num = number-11111 # 1->0, ...6->5
    decimal_number = base_to_decimal(str(dice_num), 6)
    print(f"{number}  |  {str(dice_num).ljust(5)}  =  {decimal_number}")


"""
 --- DICE to num ---
[14312, 14251, 11266, 13256, 12236, 23156, 24222, 15532, 13336, 13536, 11523, 23444]
14312  |  3201   =  721
14251  |  3140   =  708
11266  |  155    =  71
13256  |  2145   =  497
12236  |  1125   =  269
...
"""