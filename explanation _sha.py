from crypto_agama.agama_transform_tools import hex_to_bin, num_to_bin

ks = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
        0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
        0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
        0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
        0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
    ]

hs = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
    ]

ks5 = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b]

abc = [2,3,5,7,11,13,17,19] # a-h / abc -> hs 
abc5 = [2,3,5,7,11]

M32 = 0xFFFFFFFF
BITs = 32


def norm_sqr(n, r=2, info_print=False):
    number = n ** (1/r)
    decimal_part = round(number - int(number), 12)
    fin_num = int(decimal_part * (2 ** 32))
    if info_print:
        print(f'{n} \t {decimal_part:.10f} \t {fin_num} \t {hex(fin_num)} \t {num_to_bin(fin_num, True, 32)}')
    return fin_num


def pad(mlen):
    mdi = mlen & 0x3F
    length = (mlen << 3).to_bytes(8, 'big')
    padlen = 55 - mdi if mdi < 56 else 119 - mdi
    return b'\x80' + b'\x00' * padlen + length

def ror(x, y):
    return ((x >> y) | (x << (32 - y))) & M32

def maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)

def ch(x, y, z):
    return (x & y) ^ ((~x) & z)

print("-"*20, "[ abcdefgh vector ] abc -> hs ")
for n in abc:
    number = n ** (1/2)
    decimal_part = round(number - int(number), 12)
    fin_num = int(decimal_part * (2 ** 32))
    print(f'{decimal_part:.10f} \t {fin_num} \t {num_to_bin(fin_num, True, 32)}')

print("-"*20, "[ test ]")

for h in hs:
    #print(hex(h), hex_to_bin(str(hex(h))))
    print(hex(h), hex_to_bin(hex(h),True,BITs))


print("-"*20, "[ ks vector ] first 5 norm_sqr()")
for n in abc5:
    """
    number = n ** (1/3)
    decimal_part = round(number - int(number), 12)
    fin_num = int(decimal_part * (2 ** 32))
    print(f'{decimal_part:.10f} \t {fin_num} \t {num_to_bin(fin_num, True, 32)}')
    """
    norm_sqr(n, 3, True)

for h in ks5:
    #print(hex(h), hex_to_bin(str(hex(h))))
    print(hex(h), hex_to_bin(hex(h),True,BITs))



print()
print("-"*20, "[ maj ]")
x, y, z = hs[0], hs[1], hs[2]
print("x",hex(x), hex_to_bin(hex(x),True,BITs))
print("y",hex(y), hex_to_bin(hex(y),True,BITs))
print("z",hex(z), hex_to_bin(hex(z),True,BITs))
print("="*50)
print(">",hex(maj(x, y, z)), hex_to_bin(hex(maj(x, y, z)),True,BITs))

print()
print("-"*20, "[ ch ]")
x, y, z = hs[0], hs[1], hs[2]
print("x",hex(x), hex_to_bin(hex(x),True,BITs))
print("y",hex(y), hex_to_bin(hex(y),True,BITs))
print("z",hex(z), hex_to_bin(hex(z),True,BITs))
print("="*50)
print(">",hex(ch(x, y, z)), hex_to_bin(hex(ch(x, y, z)),True,BITs))

print()
print("-"*20, "[ ror ]")
x, y, z = hs[0], hs[1], hs[2]
print("x",hex(x), hex_to_bin(hex(x),True,BITs))
print("="*50)
print("1",hex(ror(x, 1)), hex_to_bin(hex(ror(x, 1)),True,BITs))
print("2",hex(ror(x, 2)), hex_to_bin(hex(ror(x, 2)),True,BITs))
print("5",hex(ror(x, 5)), hex_to_bin(hex(ror(x, 5)),True,BITs))
print("7",hex(ror(x, 7)), hex_to_bin(hex(ror(x, 7)),True,BITs))


"""
-------------------- [ abcdefgh vector ] abc -> hs 
0.4142135624     1779033703      01101010000010011110011001100111
0.7320508076     3144134277      10111011011001111010111010000101
0.2360679775     1013904242      00111100011011101111001101110010
0.6457513111     2773480762      10100101010011111111010100111010
0.3166247904     1359893119      01010001000011100101001001111111
0.6055512755     2600822924      10011011000001010110100010001100
0.1231056256     528734635       00011111100000111101100110101011
0.3588989435     1541459225      01011011111000001100110100011001
-------------------- [ test ]
0x6a09e667 01101010000010011110011001100111
0xbb67ae85 10111011011001111010111010000101
0x3c6ef372 00111100011011101111001101110010
0xa54ff53a 10100101010011111111010100111010
0x510e527f 01010001000011100101001001111111
0x9b05688c 10011011000001010110100010001100
0x1f83d9ab 00011111100000111101100110101011
0x5be0cd19 01011011111000001100110100011001
-------------------- [ ks vector ] first 5 norm_sqr()
2        0.2599210499    1116352408      0x428a2f98      01000010100010100010111110011000
3        0.4422495703    1899447441      0x71374491      01110001001101110100010010010001
5        0.7099759467    3049323471      0xb5c0fbcf      10110101110000001111101111001111
7        0.9129311828    3921009573      0xe9b5dba5      11101001101101011101101110100101
11       0.2239800906    961987163       0x3956c25b      00111001010101101100001001011011
0x428a2f98 01000010100010100010111110011000
0x71374491 01110001001101110100010010010001
0xb5c0fbcf 10110101110000001111101111001111
0xe9b5dba5 11101001101101011101101110100101
0x3956c25b 00111001010101101100001001011011

-------------------- [ maj ]
x 0x6a09e667 01101010000010011110011001100111
y 0xbb67ae85 10111011011001111010111010000101
z 0x3c6ef372 00111100011011101111001101110010
==================================================
> 0x3a6fe667 00111010011011111110011001100111

-------------------- [ ch ]
x 0x6a09e667 01101010000010011110011001100111
y 0xbb67ae85 10111011011001111010111010000101
z 0x3c6ef372 00111100011011101111001101110010
==================================================
> 0x3e67b715 00111110011001111011011100010101

-------------------- [ ror ]
x 0x6a09e667 01101010000010011110011001100111
==================================================
1 0xb504f333 10110101000001001111001100110011
2 0xda827999 11011010100000100111100110011001
5 0x3b504f33 00111011010100000100111100110011
7 0xced413cc 11001110110101000001001111001100
"""