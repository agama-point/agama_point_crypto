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
groups = shamir.generate_mnemonics( 1, [(1, 1)], secret, b"TREZOR", extendable=False, iteration_exponent=0 )
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
groups = shamir.generate_mnemonics( 1, [(1, 1)], secret, b"TREZOR", extendable=True, iteration_exponent=3 )
output(description.format(8 * n), groups[0], secret)

description = "Extendable basic sharing 2-of-3 ({} bits) groups  1, [(2, 3)]"
# secret = random_bytes(n)
groups = shamir.generate_mnemonics( 1, [(2, 3)], secret, b"TREZOR", extendable=True, iteration_exponent=0 )
output(description.format(8 * n), random.sample(groups[0], 2), secret)

print("="*50)

print("1",groups[0][0])
print("2",groups[0][1])
print("3",groups[0][2])

"""
==============================
sec: b'\x0c\x1e$\xe5\x91wy\xd2\x97\xe1ME\xf1N\x1a\x1a'
groups 2, [(1, 1), (1, 1), (3, 5), (2, 6)]

--- desc: Valid extendable mnemonic without sharing (128 bits) groups 1, [(1, 1)]
- mnem:
 senior example academic academic depict pharmacy both flexible script gross vanish literary element gross criminal glen faint born acne marathon
- secr: 0c1e24e5917779d297e14d45f14e1a1a
- xprv: xprv9s21ZrQH143K3Z2...jntWvUgeN144vdPYpgXgLxzYSSiJ71S
------------------------------
--- desc: Extendable basic sharing 2-of-3 (128 bits) groups 1, [(2, 3)]
- mnem: ..
- secr: 0c1e24e5917779d297e14d45f14e1a1a
- xprv: xprv9s21ZrQH143K3Z2...TDUWRqh9GjntWvUgeN144vdPYpgXgLxzYSSiJ71S
------------------------------
==================================================
1 juice else academic acid discuss evoke brother withdraw venture laden taxi usher bulb pharmacy nail task bolt scandal syndrome keyboard
2 juice else academic agency blanket solution kidney ocean group axle clinic prevent rumor review rival exclude method enforce hand phantom
3 juice else academic always clay hearing speak depict suitable pile hawk forget herald merchant plan wireless bulb vitamins language hawk

"""