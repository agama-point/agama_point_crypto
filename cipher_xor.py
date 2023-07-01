#!/usr/bin/env python
from crypto_agama.agama_transform_tools import hex_to_bin, bin_to_hex
from crypto_agama.agama_cipher import xor_crypt


print("XOR","-"*39)
d_hex = "FF0abc0FF"
k_hex = "F0F0F0F0F"
print(d_hex)
print(k_hex)
x_hex = xor_crypt(d_hex,k_hex)
print(x_hex, len(x_hex))
lenb = len(x_hex)*4
xb = hex_to_bin(x_hex,True).zfill(lenb)
print(xb, len(xb))
print(bin_to_hex(xb,to_string=True,length=len(x_hex)))
print()

print("XOR","-"*39)
d_hex = "aFF0abc0FF"
k_hex = "bF0F0F0F0F"
print(d_hex)
print(k_hex)
x_hex = xor_crypt(d_hex,k_hex)
print(x_hex, len(x_hex))
lenb = len(x_hex)*4
xb = hex_to_bin(x_hex,True).zfill(lenb)
print(xb, len(xb))
hex2 = bin_to_hex(xb,to_string=True)
print(hex2)
print(hex_to_bin(hex2,to_string=True).zfill(lenb))
"""
XOR ---------------------------------------
aFF0abc0FF
bF0F0F0F0F
10ffa4cff0 10
0001000011111111101001001100111111110000 40
10ffa4cff0
0001000011111111101001001100111111110000
"""