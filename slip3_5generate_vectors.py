#!/usr/bin/env python3
import json
import random
from dataclasses import astuple

from bip32utils import BIP32Key

from shamir_mnemonic import constants, rs1024, shamir, wordlist
from shamir_mnemonic.share import Share


def random_bytes(n):
    return bytes(random.randrange(256) for _ in range(n))


def output(description, mnemonics, secret):
    # output.i += 1
    xprv = BIP32Key.fromEntropy(secret).ExtendedKey() if secret else ""
    # output.data.append((f"{output.i}. {description}", mnemonics, secret.hex(), xprv))
    print("--- desc:",description)
    mnemonics_string = ', '.join(mnemonics)
    mnemonics = mnemonics_string.replace(', ', '\n')
    print("- mnem:\n",mnemonics)
    print("- secr:",secret.hex())
    print("- xprv:",xprv)
    print("-"*30)

def encode_mnemonic(*args):
    return Share(*args).mnemonic()

def decode_mnemonic(mnemonic):
    return list(astuple(Share.from_mnemonic(mnemonic)))

def generate_mnemonics_random(group_threshold, groups):
    secret = random_bytes(16)
    return shamir.generate_mnemonics( group_threshold, groups, secret, extendable=False, iteration_exponent=0 )


output.i = 0
output.data = []

random_bytesA = bytes.fromhex("0c1e24e5917779d297e14d45f14e1a1a")

# shamir.RANDOM_BYTES = random_bytesA
# random.seed(1337)

#for n in [16, 32]: # 128 / 256 b
n = 16
description = "Valid mnemonic without sharing ({} bits) groups 1, [(1, 1)]"
secret = random_bytesA # random_bytes(n)
groups = shamir.generate_mnemonics( 1, [(1, 1)], secret, b"agama", extendable=False, iteration_exponent=0 )
output(description.format(8 * n), groups[0], secret)


data = decode_mnemonic(groups[0][0])
print(data)
mnemonics = [encode_mnemonic(*data), groups[0][0]]
print(mnemonics)
print()
indices = wordlist.mnemonic_to_indices(groups[0][0])
print("1 indicies for groups[0][0]:")
print(indices)
print()





print("="*50)
MS = random_bytesA
print("Master Seed:",MS.hex())
mnemonics = shamir.generate_mnemonics(1, [(3, 5)], MS, b"agama")[0]

for i in range(0,5):
    print(i+1,mnemonics[i])


print("-"*50,":3")
groups = shamir.decode_mnemonics(mnemonics[:3])
print(groups)
encrypted_master_secret = shamir.recover_ems(groups)
recovered = encrypted_master_secret.decrypt(b"agama")
print("Recovered: ",recovered.hex())

print("-"*50,"1:4")
groups = shamir.decode_mnemonics(mnemonics[1:4])
print(groups)
encrypted_master_secret = shamir.recover_ems(groups)
recovered = encrypted_master_secret.decrypt(b"agama")
print("Recovered: ",recovered.hex())

print("="*39, "recovery 5 3 1")
m = [None] * 5
m[1]=mnemonics[5-1]
m[2]=mnemonics[3-1]
m[3]=mnemonics[1-1]

for j in range(1,4):
    print(j,m[j])

groups = shamir.decode_mnemonics(m[1:4])
print(groups)
encrypted_master_secret = shamir.recover_ems(groups)
recovered = encrypted_master_secret.decrypt(b"agama")
print("Recovered: ",recovered.hex())



"""
--- desc: Valid mnemonic without sharing (128 bits) groups 1, [(1, 1)]
- mnem:
 bulb necklace academic academic ceiling failure envy dismiss warn exchange drove mouse grasp relate dryer omit network impact pumps dance
- secr: 0c1e24e5917779d297e14d45f14e1a1a
- xprv: xprv9s21ZrQH143K3Z2jgAJ6XzQYPdsiJqPHJkdTrxm5NwYyJW8o3e9uJCtVwpLuXVBHgyFTDUWRqh9GjntWvUgeN144vdPYpgXgLxzYSSiJ71S
------------------------------
[3411, False, 0, 0, 1, 1, 0, 1, b'\x82QR3\x93\xe2MOYU\x93\xb9\x0fy\xc6c']
['bulb necklace academic academic ceiling failure envy dismiss warn exchange drove mouse grasp relate dryer omit network impact pumps dance', 'bulb necklace academic academic ceiling failure envy dismiss warn exchange drove mouse grasp relate dryer omit network impact pumps dance']

1 indicies for groups[0][0]:
[106, 608, 0, 0, 130, 325, 291, 228, 994, 309, 245, 597, 403, 740, 247, 625, 611, 456, 709, 187]

==================================================
Master Seed: 0c1e24e5917779d297e14d45f14e1a1a
1 location evoke academic acne busy capture spirit declare therapy minister together sugar traffic software climate velvet pregnant predator dominant easy
2 location evoke academic agree decrease pancake package deadline flash staff client pleasure trash organize pink laden unhappy costume email install
3 location evoke academic amazing credit taught grin humidity prevent western modify mason taste bike evil hazard arcade iris relate painting
4 location evoke academic arcade already furl crystal idea carbon rocky fake wrap tadpole game royal thorn exotic veteran script multiple
5 location evoke academic axle bracelet predator deal empty nervous tracks alarm slow benefit drove unfair criminal raspy blanket aviation always
-------------------------------------------------- :3
{0: <shamir_mnemonic.shamir.ShareGroup object at 0x000001367A845130>}
Recovered:  0c1e24e5917779d297e14d45f14e1a1a
-------------------------------------------------- 1:4
{0: <shamir_mnemonic.shamir.ShareGroup object at 0x000001367A838580>}
Recovered:  0c1e24e5917779d297e14d45f14e1a1a
======================================= recovery 5 3 1
1 location evoke academic axle bracelet predator deal empty nervous tracks alarm slow benefit drove unfair criminal raspy blanket aviation always
2 location evoke academic amazing credit taught grin humidity prevent western modify mason taste bike evil hazard arcade iris relate painting
3 location evoke academic acne busy capture spirit declare therapy minister together sugar traffic software climate velvet pregnant predator dominant easy
{0: <shamir_mnemonic.shamir.ShareGroup object at 0x000001367A3FCBB0>}
Recovered:  0c1e24e5917779d297e14d45f14e1a1a
"""
