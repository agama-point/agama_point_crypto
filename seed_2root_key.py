from mnemonic import Mnemonic
from crypto_agama.transform import *
from crypto_agama.agama_seed_tools import mnemo_to_seed, create_root_key, create_root_key2
from priv_data import get_seeds, get_words # words
from crypto_agama.agama_cryptos import create_wallet
import base58, hmac

TW = 80 # terminal width

print("-"*TW)
print("agama_point - test_converter.py - iancoleman.io/bip39")
print("-"*TW)

mnemo = Mnemonic("english")
print("Mnemonic Language: english")

words = "army van defense carry jealous true garbage claim echo media make crunch" # book
passphrase = ""

print("BIP39 Mnemonic: ", words)

print("-"*TW)
print("--- BIP39 Seed ---")

mnemo_seed = mnemo_to_seed(words)
print("mnemo_to_seed_hex (B2x) ANDREAS1_215a3d: ", mnemo_seed.hex())

print("BIP39 Passphrase (optional): ", passphrase)
seed_bytes = mnemo.to_seed(words, passphrase)
#seed_bytes = mnemo.to_seed(words, passphrase="")
# print("mnemo.to_seed = seed_bytes: ", seed_bytes)

print(seed_bytes.hex()) # hexadecimal_string = some_bytes.hex()
print()

print("--- BIP32 Root Key ---")
root_key = create_root_key(seed_bytes)
print("= create_root_key: ", root_key)


root_key = create_root_key2(seed_bytes)

print("= create_root_key2: ", root_key)

print("prefix: ",base58.b58encode_check(b'0488ade4').decode('utf8'))
print("b58: ", convert_to_base58(int(b'0488ade4', 16)))
print("b58: ", convert_to_base58(int('0x0488ade4', 16)))


"""
...
= create_root_key:  
xprv9s21ZrQH143K3t4UZrNgeA3w861fwjYLaGwmPtQyPMmzshV2owVpfBSd2Q7YsHZ9j6i6ddYjb5PLtUdMZn8LhvuCVhGcQntq5rn7JVMqnie

=================================
https://iancoleman.io/bip39/

BIP39 seed:
5b56c417303faa3fcba7e57400e120a0ca83ec5a4fc9ffba757fbe63fbd77a89a1a3be4c67196f57c39a88b76373733891bfaba16ed27a813ceed498804c0570

BIP32 root key:
xprv9s21ZrQH143K3t4UZrNgeA3w861fwjYLaGwmPtQyPMmzshV2owVpfBSd2Q7YsHZ9j6i6ddYjb5PLtUdMZn8LhvuCVhGcQntq5rn7JVMqnie

"""