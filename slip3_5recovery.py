#!/usr/bin/env python3
import json
import random
from dataclasses import astuple
from bip32utils import BIP32Key
from shamir_mnemonic import constants, rs1024, shamir, wordlist
from shamir_mnemonic.share import Share


def random_bytes(n):
    return bytes(random.randrange(256) for _ in range(n))

def generate_mnemonics_random(group_threshold, groups):
    secret = random_bytes(16)
    return shamir.generate_mnemonics( group_threshold, groups, secret, extendable=False, iteration_exponent=0 )

def encode_mnemonic(*args):
    return Share(*args).mnemonic()

def decode_mnemonic(mnemonic):
    return list(astuple(Share.from_mnemonic(mnemonic)))

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


# output.i = 0
# output.data = []

random_bytesA = bytes.fromhex("0c1e24e5917779d297e14d45f14e1a1a")
# shamir.RANDOM_BYTES = random_bytesA
random.seed(1337)

#for n in [16, 32]: # 128 / 256 b
n = 16
secret = random_bytesA # random_bytes(n)

description = "Valid mnemonic without sharing ({} bits) groups 1, [(1, 1)] TREZOR"
groups = shamir.generate_mnemonics(1, [(1, 1)], secret, b"TREZOR", extendable=False, iteration_exponent=0 )
output(description.format(8 * n), groups[0], secret)

description = "Valid mnemonic without sharing ({} bits) groups 1, [(1, 1)] agama"
mnemonics = shamir.generate_mnemonics(1, [(1, 1)], secret, b"agama", extendable=False, iteration_exponent=0)
output(description.format(8 * n), mnemonics[0], secret)

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
# Generování mnemonik pro dvě skupiny
mnemonics = shamir.generate_mnemonics(
    2,                    # Počet skupin potřebných k obnově
    [(2, 3), (3, 5)],     # Skupiny: (2 ze 3) a (3 z 5)
    secret,               # Tajemství
    b"agama",             # Identifikátor (ID)
    extendable=False, 
    iteration_exponent=0
)

print("Mnemoniky pro první skupinu (2 ze 3):")
for mnemonic in mnemonics[0]:
    print(mnemonic)

print("\nMnemoniky pro druhou skupinu (3 z 5):")
for mnemonic in mnemonics[1]:
    print(mnemonic)

first_group_mnemonics = mnemonics[0]
second_group_mnemonics = mnemonics[1]
test_mnemonics = [first_group_mnemonics[0], first_group_mnemonics[2]] # 1: 1-3

print("\nTestované mnemoniky (indexy 1 a 3):")
for mnemonic in test_mnemonics:
    print(mnemonic)

# Dekódování mnemonik a obnova tajemství
shares = shamir.decode_mnemonics(test_mnemonics)
print("shares: ",shares)
"""
encrypted_master_secret = shamir.recover_ems(shares)
recovered_secret = encrypted_master_secret.decrypt(b"agama")

print("\nObnovené tajemství:")
print(recovered_secret.hex())
"""

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

recovered = encrypted_master_secret.decrypt(b"agamax")
print("Recoveredx:",recovered.hex())

"""
BIP32 Root Key:
xprv9s21ZrQH143K3t4UZrNgeA3w861fwjYLaGwmPtQyPMmzshV2owVpfBSd2Q7YsHZ9j6i6ddYjb5PLtUdMZn8LhvuCVhGcQntq5rn7JVMqnie
BIP32 Extended Private Key:
xprv9vD6P73Kk5gLexAk8oz7D2Ph1WGebCU6bBLdkNBUfoTbeWFGzewEg7wwTBuqsfu6QHyKs55mVsVaMQHGhh6uwiMFL9juVH3DH9GThQE7UWH

--- desc: Valid mnemonic without sharing (128 bits) groups 1, [(1, 1)] TREZOR
- mnem:
 tackle pink academic academic client strike speak sunlight pipeline thumb unusual body drink making shadow item junction laser submit aluminum
- secr: 0c1e24e5917779d297e14d45f14e1a1a
- xprv: xprv9s21ZrQH143K3Z2jgAJ6XzQYPdsiJqPHJkdTrxm5NwYyJW8o3e9uJCtVwpLuXVBHgyFTDUWRqh9GjntWvUgeN144vdPYpgXgLxzYSSiJ71S
------------------------------
--- desc: Valid mnemonic without sharing (128 bits) groups 1, [(1, 1)] agama
- mnem:
 sugar painting academic academic briefing smell infant intend retreat superior juice tricycle software bulge funding strategy laser type forget transfer
- secr: 0c1e24e5917779d297e14d45f14e1a1a
- xprv: xprv9s21ZrQH143K3Z2jgAJ6XzQYPdsiJqPHJkdTrxm5NwYyJW8o3e9uJCtVwpLuXVBHgyFTDUWRqh9GjntWvUgeN144vdPYpgXgLxzYSSiJ71S
------------------------------
[28501, False, 0, 0, 1, 1, 0, 1, b'\x92\xd9\xf4\xdd\xb6\xa1\xe4\xfb\xe1d\xf4\x8a\xf2\x17\x85\xea']
['tackle pink academic academic client strike speak sunlight pipeline thumb unusual body drink making shadow item junction laser submit aluminum', 'tackle pink academic academic client strike speak sunlight pipeline thumb unusual body drink making shadow item junction laser submit aluminum']

1 indicies for groups[0][0]:
[890, 672, 0, 0, 146, 871, 845, 877, 673, 915, 958, 89, 244, 555, 801, 481, 490, 509, 874, 32]

==================================================
Mnemoniky pro první skupinu (2 ze 3):
graduate walnut acrobat echo daisy often scared revenue civil fragment browser loan bulge calcium trash acid teaspoon rich home large
graduate walnut acrobat email ancient tofu infant bracelet perfect item decorate gums simple exhaust item include violence teaspoon fragment deal
graduate walnut acrobat entrance ceiling general petition weapon union bishop equip erode jacket recover sheriff together senior ocean that knife

Mnemoniky pro druhou skupinu (3 z 5):
graduate walnut beard eclipse clinic paper home terminal lamp lend rebound render browser lyrics timber crucial veteran cowboy acquire salt
graduate walnut beard emerald decrease orange born depart smart average join taste royal payment tackle eyebrow admit axle elder drift
graduate walnut beard envelope carbon pitch scene lily saver alcohol golden extend pumps society guest remove replace rebound subject union
graduate walnut beard exact ancient mouse reward filter index mandate plot device guest western fantasy salon evoke medal network axle
graduate walnut beard eyebrow budget golden floral olympic plastic quantity typical trash teaspoon activity ancient sunlight prospect finger pacific graduate

Testované mnemoniky (indexy 1 a 3):
graduate walnut acrobat echo daisy often scared revenue civil fragment browser loan bulge calcium trash acid teaspoon rich home large
graduate walnut acrobat entrance ceiling general petition weapon union bishop equip erode jacket recover sheriff together senior ocean that knife
shares:  {0: <shamir_mnemonic.shamir.ShareGroup object at 0x00000223654DB8B0>}
==================================================
Master Seed: 0c1e24e5917779d297e14d45f14e1a1a
1 become graduate academic acne blanket wine lizard starting pleasure glad rebuild thunder coding saver short weapon blessing watch install raspy
2 become graduate academic agree dress elder have else axis science calcium greatest minister mountain blanket prisoner merchant ecology improve overall
3 become graduate academic amazing database spew disaster senior hormone inform amazing hairy airline slavery epidemic transfer losing promise python laser
4 become graduate academic arcade alien holiday starting founder spew spark payroll trend prospect often mule river advocate bracelet rapids flash
5 become graduate academic axle black photo pulse numerous impact forbid bracelet obtain oral general cultural snake eyebrow spend bulge album
-------------------------------------------------- :3
{0: <shamir_mnemonic.shamir.ShareGroup object at 0x00000223658FBCD0>}
Recovered:  0c1e24e5917779d297e14d45f14e1a1a
-------------------------------------------------- 1:4
{0: <shamir_mnemonic.shamir.ShareGroup object at 0x0000022365931640>}
Recovered:  0c1e24e5917779d297e14d45f14e1a1a
======================================= recovery 5 3 1
1 become graduate academic axle black photo pulse numerous impact forbid bracelet obtain oral general cultural snake eyebrow spend bulge album
2 become graduate academic amazing database spew disaster senior hormone inform amazing hairy airline slavery epidemic transfer losing promise python laser
3 become graduate academic acne blanket wine lizard starting pleasure glad rebuild thunder coding saver short weapon blessing watch install raspy
{0: <shamir_mnemonic.shamir.ShareGroup object at 0x0000022365354220>}
Recovered:  0c1e24e5917779d297e14d45f14e1a1a
Recoveredx: 5fc3e797b65aeccb1ccad98914a8e81c
"""
