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
    print("----- ",description)
    mnemonics_string = ', '.join(mnemonics)
    mnemonics = mnemonics_string.replace(', ', '\n')
    print("- mnem:\n",mnemonics)
    # print("- secr:",secret.hex())
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
"""
for j in range(1,4):
    print(j,m[j])
"""
groups = shamir.decode_mnemonics(m[1:4])
print(groups)
encrypted_master_secret = shamir.recover_ems(groups)
recovered = encrypted_master_secret.decrypt(b"agama")
print("Recovered:",recovered.hex())

recovered = encrypted_master_secret.decrypt(b"agamax")
print("Recover_x:",recovered.hex())
print()

mt = [None] * 5  # mnemonics test
mt[1] = "become graduate academic axle black photo pulse numerous impact forbid bracelet obtain oral general cultural snake eyebrow spend bulge album"
mt[2] = "become graduate academic amazing database spew disaster senior hormone inform amazing hairy airline slavery epidemic transfer losing promise python laser"
mt[3] = "become graduate academic acne blanket wine lizard starting pleasure glad rebuild thunder coding saver short weapon blessing watch install raspy"
for j in range(1,4):
    print(j,mt[j])

groups = shamir.decode_mnemonics(mt[1:4])
encrypted_master_secret = shamir.recover_ems(groups)
recovered = encrypted_master_secret.decrypt(b"agama")
print("Recovered - final test: ",recovered.hex())


mt = [None] * 5  # mnemonics test
mt[1] = "become graduate academic axle black photo pulse numerous impact forbid bracelet obtain oral general cultural snake eyebrow spend bulge album"
mt[2] = "become graduate academic amazing database spew disaster senior hormone inform amazing hairy airline slavery epidemic transfer losing promise python laser"
mt[3] = "become graduate academic acne blanket wine lizard starting pleasure glad rebuild thunder coding saver short weapon blessing watch install raspy"
for j in range(1,4):
    print(j,mt[j])

"""
shamir_mnemonic.utils.MnemonicError: 
mt[1] = "becomex graduate academic ...   Invalid mnemonic word 'becomex'.
mt[1] = "becomex          academic ...   Invalid mnemonic length. The length of each mnemonic must be at least 20 words.
...
"""

groups = shamir.decode_mnemonics(mt[1:4])
encrypted_master_secret = shamir.recover_ems(groups)
recovered = encrypted_master_secret.decrypt(b"agamax")
print("Recover_x- final test: ",recovered.hex())


"""
BIP32 Root Key:
xprv9s21ZrQH143K3t4UZrNgeA3w861fwjYLaGwmPtQyPMmzshV2owVpfBSd2Q7YsHZ9j6i6ddYjb5PLtUdMZn8LhvuCVhGcQntq5rn7JVMqnie
BIP32 Extended Private Key:
xprv9vD6P73Kk5gLexAk8oz7D2Ph1WGebCU6bBLdkNBUfoTbeWFGzewEg7wwTBuqsfu6QHyKs55mVsVaMQHGhh6uwiMFL9juVH3DH9GThQE7UWH

-----  Valid mnemonic without sharing (128 bits) groups 1, [(1, 1)] TREZOR
- mnem:
 easel guest academic academic bundle warmth species says veteran vocal prune large indicate curly brother valuable mild debris loud black
- xprv: xprv9s21ZrQH143K3Z2jgAJ6XzQYPdsiJqPHJkdTrxm5NwYyJW8o3e9uJCtVwpLuXVBHgyFTDUWRqh9GjntWvUgeN144vdPYpgXgLxzYSSiJ71S
------------------------------
-----  Valid mnemonic without sharing (128 bits) groups 1, [(1, 1)] agama
- mnem:
 skin taught academic academic bucket float dominant acid gravity spill vampire thorn example soul volume wealthy level deploy cultural theater
- xprv: xprv9s21ZrQH143K3Z2jgAJ6XzQYPdsiJqPHJkdTrxm5NwYyJW8o3e9uJCtVwpLuXVBHgyFTDUWRqh9GjntWvUgeN144vdPYpgXgLxzYSSiJ71S
------------------------------
[8173, False, 0, 0, 1, 1, 0, 1, b"m\xf8t\xec?\xd0\xf6\xec'\xf1\xd0-\x86_\x1aE"]
['easel guest academic academic bundle warmth species says veteran vocal prune large indicate curly brother valuable mild debris loud black', 'easel guest academic academic bundle warmth species says veteran vocal prune large indicate curly brother valuable mild debris loud black']

1 indicies for groups[0][0]:
[255, 416, 0, 0, 109, 993, 846, 783, 976, 987, 706, 508, 464, 182, 101, 966, 581, 193, 540, 83]

==================================================
Mnemoniky pro první skupinu (2 ze 3):
fangs lunch acrobat echo deadline grumpy axle center necklace patrol best helpful employer hybrid island starting width stay penalty short
fangs lunch acrobat email aquatic capacity engage glasses speak gravity aircraft phantom playoff either wisdom main formal rhythm axle midst
fangs lunch acrobat entrance cylinder mobile replace both august dining flavor funding buyer believe golden slice dramatic package repair install

Mnemoniky pro druhou skupinu (3 z 5):
fangs lunch beard eclipse dough science crush image ounce center space burden destroy epidemic bucket purple tricycle heat helpful clock
fangs lunch beard emerald critical steady blue bike orbit terminal fragment exchange prospect triumph cinema ecology educate sympathy dive example
fangs lunch beard envelope density index inmate railroad blind include merchant exercise phrase crowd shaft havoc dynamic knife decorate smell
fangs lunch beard exact chest hour express stadium boring punish cards breathe civil lunch vanish network mortgage skunk golden physics
fangs lunch beard eyebrow adjust racism manager medical rich obtain diploma species python idle duration being spark fluff recover alive

Testované mnemoniky (indexy 1 a 3):
fangs lunch acrobat echo deadline grumpy axle center necklace patrol best helpful employer hybrid island starting width stay penalty short
fangs lunch acrobat entrance cylinder mobile replace both august dining flavor funding buyer believe golden slice dramatic package repair install
shares:  {0: <shamir_mnemonic.shamir.ShareGroup object at 0x0000020D13C37550>}

==================================================
Master Seed: 0c1e24e5917779d297e14d45f14e1a1a
1 chemical desert academic acne brother health reaction talent lawsuit filter peaceful keyboard admit metric involve scramble stadium slavery quick imply
2 chemical desert academic agree budget grant physics devote episode failure ecology arcade race junior custody boring wrote float friendly aide
3 chemical desert academic amazing check research tackle birthday oven burning canyon scared profile sweater idle morning herd birthday predator document
4 chemical desert academic arcade champion radar smart woman pitch carpet wrist railroad bucket dictate crisis enforce emerald legs emperor example
5 chemical desert academic axle blessing scramble empty fraction mobile shrimp email obesity enjoy deny ruler analysis breathe terminal theory sister
-------------------------------------------------- :3
{0: <shamir_mnemonic.shamir.ShareGroup object at 0x0000020D13674250>}
Recovered:  0c1e24e5917779d297e14d45f14e1a1a
-------------------------------------------------- 1:4
{0: <shamir_mnemonic.shamir.ShareGroup object at 0x0000020D13C73220>}
Recovered:  0c1e24e5917779d297e14d45f14e1a1a

======================================= recovery 5 3 1
{0: <shamir_mnemonic.shamir.ShareGroup object at 0x0000020D137CFDC0>}
Recovered: 0c1e24e5917779d297e14d45f14e1a1a
Recover_x: 5fc3e797b65aeccb1ccad98914a8e81c

1 become graduate academic axle black photo pulse numerous impact forbid bracelet obtain oral general cultural snake eyebrow spend bulge album
2 become graduate academic amazing database spew disaster senior hormone inform amazing hairy airline slavery epidemic transfer losing promise python laser
3 become graduate academic acne blanket wine lizard starting pleasure glad rebuild thunder coding saver short weapon blessing watch install raspy
Recovered - final test:  0c1e24e5917779d297e14d45f14e1a1a

1 become graduate academic axle black photo pulse numerous impact forbid bracelet obtain oral general cultural snake eyebrow spend bulge album
2 become graduate academic amazing database spew disaster senior hormone inform amazing hairy airline slavery epidemic transfer losing promise python laser
3 become graduate academic acne blanket wine lizard starting pleasure glad rebuild thunder coding saver short weapon blessing watch install raspy
Recover_x- final test:  5fc3e797b65aeccb1ccad98914a8e81c
"""
