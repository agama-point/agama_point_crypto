from crypto_agama.agama_transform_tools import decimal_to_base, base_to_decimal, hex_to_num
from crypto_agama.agama_seed_tools import seed_words, mnemonic_info

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

Raw Binary
00100001101 11011011101 11111000011 01111111101 01000001001 01001010001 10001011001 00100100001 10011001011 00110011011 01001111001 0011000
Binary Checksum
0101
*
01011010001 01011000100 00001000111 00111110001 00100001101 11011011101 11111000011 01111111101 01000001001 01001010001 10001011001 0110111
Binary Checksum
1101

Word Indexes
                    269, 1757, 1987, 1021, 521, 593, 1113, 289, 1227, 411, 633, 389
*721, 708, 71, 497, 269, 1757, 1987, 1021, 521, 593, 152, 1857

"""
en_hex = "5a2b10239f121bb77e1bfd4129462cb7"
print(en_hex)
print(hex_to_num(en_hex))

#w12 = "canvas sweet wear leisure donkey enforce menu category offer cricket execute cost"
w12 = "focus flat angry dilemma canvas sweet wear leisure donkey enforce basic trial"
mnemonic_info(w12)



# nums12 = [269, 1757, 1987, 1021, 521, 593, 1113, 289, 1227, 411, 633, 389]
nums12 = [721, 708, 71, 497, 269, 1757, 1987, 1021, 521, 593, 152, 1857]

print("--- 5 ---")
base = 5
for number in nums12: 
    #decimal_number = base_to_decimal(str(number), base)
    cislo_petkova = decimal_to_base(number,base)
    print(cislo_petkova, end=" ")

print("\n--- DICE ---")
base = 5
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
21452 21424 11352 14553 13145 35123 41533 24152 15152 15444 12213 35523
--- 6 ---
03201 03140 00155 02145 01125 12045 13111 04421 02225 02425 00412 12333

"""

print("\n --- DICE 2 num ---")

dice12 = "21452 21424 11352 14553 13145 35123 41533 24152 15152 15444 12213 35523"
number_list = [int(num) for num in dice12.split()]
print(number_list)

for number in number_list:
    dice_num = number-11111 # 1->0, ...6->5
    decimal_number = base_to_decimal(str(dice_num), 5)
    # print(number,dice_num,decimal_number)
    print(f"{number}  |  {str(dice_num).ljust(5)}  =  {decimal_number}")

"""
 --- DICE 2 num ---
[21452, 21424, 11352, 14553, 13145, 35123, 41533, 24152, 15152, 15444, 12213, 35523]
21452  |  10341  =  721
21424  |  10313  =  708
11352  |  241    =  71
14553  |  3442   =  497
13145  |  2034   =  269
...
"""