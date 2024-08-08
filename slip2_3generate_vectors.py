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


print("="*30)
# Group sharing.
# secret = random_bytes(n)
groups = shamir.generate_mnemonics(
    2,
    [(1, 1), (1, 1), (3, 5), (2, 6)],
    secret,
    b"TREZOR",
    extendable=False,
    iteration_exponent=0,
)
print("sec:",secret)
print("groups 2, [(1, 1), (1, 1), (3, 5), (2, 6)]")
print()


# for n in [16, 32]:
description = "Valid extendable mnemonic without sharing ({} bits) groups 1, [(1, 1)]"
# secret = random_bytes(n)
groups = shamir.generate_mnemonics( 1, [(1, 1)], secret, b"agama", extendable=True, iteration_exponent=3 )
output(description.format(8 * n), groups[0], secret)

description = "Extendable basic sharing 2-of-3 ({} bits) groups  1, [(2, 3)]"
# secret = random_bytes(n)
groups = shamir.generate_mnemonics( 1, [(2, 3)], secret, b"agama", extendable=True, iteration_exponent=0 )
output(description.format(8 * n), random.sample(groups[0], 2), secret)

print("="*50)
data = decode_mnemonic(groups[0][0])
print(data)
mnemonics = [encode_mnemonic(*data), groups[0][0]]
print(mnemonics)
print()
indices = wordlist.mnemonic_to_indices(groups[0][0])
print("1 indicies for groups[0][0]:")
print(indices)
print()
for i in range(0,3):
    print(i+1,groups[0][i])

"""
--- desc: Valid mnemonic without sharing (128 bits) groups 1, [(1, 1)]
- mnem:
 makeup romp academic academic counter retreat chew legs syndrome envy change grill numerous clinic blessing acrobat unknown skin numerous memory
- secr: 0c1e24e5917779d297e14d45f14e1a1a
- xprv: xprv9s21ZrQH143K3Z2jgAJ6XzQYPdsiJqPHJkdTrxm5NwYyJW8o3e9uJCtVwpLuXVBHgyFTDUWRqh9GjntWvUgeN144vdPYpgXgLxzYSSiJ71S
------------------------------
==============================
sec: b'\x0c\x1e$\xe5\x91wy\xd2\x97\xe1ME\xf1N\x1a\x1a'
groups 2, [(1, 1), (1, 1), (3, 5), (2, 6)]

--- desc: Valid extendable mnemonic without sharing (128 bits) groups 1, [(1, 1)]
- mnem:
 umbrella skunk academic academic airline example ancient obtain exhaust boundary lunar retreat advance salt snake unfold careful snake medal review
- secr: 0c1e24e5917779d297e14d45f14e1a1a
- xprv: xprv9s21ZrQH143K3Z2jgAJ6XzQYPdsiJqPHJkdTrxm5NwYyJW8o3e9uJCtVwpLuXVBHgyFTDUWRqh9GjntWvUgeN144vdPYpgXgLxzYSSiJ71S
------------------------------
--- desc: Extendable basic sharing 2-of-3 (128 bits) groups  1, [(2, 3)]
- mnem:
 cricket biology academic always criminal numerous plot thank believe shaped execute grin dining payment fatal holiday beam failure welfare keyboard
cricket biology academic acid angel equation junk forecast adapt verdict pregnant peasant artist peanut execute laundry coal marvel holiday trend
- secr: 0c1e24e5917779d297e14d45f14e1a1a
- xprv: xprv9s21ZrQH143K3Z2jgAJ6XzQYPdsiJqPHJkdTrxm5NwYyJW8o3e9uJCtVwpLuXVBHgyFTDUWRqh9GjntWvUgeN144vdPYpgXgLxzYSSiJ71S
------------------------------
==================================================
[5442, True, 0, 0, 1, 1, 0, 2, b'*I\x9e\xc5\xa4\x07\xf3k\n<6\xa3\x93\x87\xf8\x9b']
['cricket biology academic acid angel equation junk forecast adapt verdict pregnant peasant artist peanut execute laundry coal marvel holiday trend', 'cricket biology academic acid angel equation junk forecast adapt verdict pregnant peasant artist peanut execute laundry coal marvel holiday trend']

1 indicies for groups[0][0]:
[170, 80, 0, 1, 42, 294, 492, 361, 7, 973, 688, 655, 54, 654, 312, 510, 155, 564, 438, 934]

1 cricket biology academic acid angel equation junk forecast adapt verdict pregnant peasant artist peanut execute laundry coal marvel holiday trend
2 cricket biology academic agency dive change mineral tactics practice unhappy fridge ruin axle cylinder video prize dryer indicate language alien
3 cricket biology academic always criminal numerous plot thank believe shaped execute grin dining payment fatal holiday beam failure welfare keyboard

"""