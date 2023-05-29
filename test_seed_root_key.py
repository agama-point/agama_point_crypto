from mnemonic import Mnemonic
from crypto_agama.transform import *
from crypto_agama.seed_tools import mnemo_to_seed, create_root_key
from priv_data import get_seeds, get_words # words
from crypto_agama.agama_cryptos import create_wallet
import base58, hmac

TW = 80 # terminal width


def _create_root_key(seed_bytes,version_BYTES = "mainnet_private"):
   print("--- _create_root_key: running ---")
   # the HMAC-SHA512 `key` and `data` must be bytes:
   I = hmac.new(b'Bitcoin seed', seed_bytes, hashlib.sha512).digest()
   L, R = I[:32], I[32:]
   master_private_key = int.from_bytes(L, 'big')
   master_chain_code = R
   print("hmac-sha512 (B2x): ", I.hex())
   print("master_private_key ", master_private_key)
   print("master_chain_code (B2x)", master_chain_code.hex())



   VERSION_BYTES = {
      'mainnet_public': binascii.unhexlify('0488b21e'), 
      'mainnet_private': binascii.unhexlify('0488ade4'),
      'testnet_public': binascii.unhexlify('043587cf'), 
      'testnet_private': binascii.unhexlify('04358394'),
   }

   print("version_BYTES: ", version_BYTES)

   version_bytes = VERSION_BYTES[version_BYTES] #  testnet_public
   depth_byte = b'\x00'
   parent_fingerprint = b'\x00' * 4
   child_number_bytes = b'\x00' * 4
   key_bytes = b'\x00' + L
   all_parts = (
      version_bytes,       #  4 bytes  
      depth_byte,          #  1 byte
      parent_fingerprint,  #  4 bytes
      child_number_bytes,  #  4 bytes
      master_chain_code,   # 32 bytes
      key_bytes,           # 33 bytes
   )
   all_bytes = b''.join(all_parts)
   print("all_bytes: ", all_bytes)
   print("all_bytes (b2x): ", all_bytes.hex())
   root_key = base58.b58encode_check(all_bytes).decode('utf8')
   print("root_key: ",root_key)
   return root_key

"""
def mnemo_to_seed_old(mnemonic):
    PBKDF2_ROUNDS = 2048
    # passphrase = "mnemonic" + passphrase
    mnemonic_bytes = mnemonic.encode("utf-8")
    passphrase_bytes = passphrase.encode("utf-8")
    stretched = hashlib.pbkdf2_hmac("sha512", mnemonic_bytes, passphrase_bytes, PBKDF2_ROUNDS)
    return stretched[:64]
"""

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
print("create_root_key(): ", root_key)


root_key = _create_root_key(seed_bytes)

print("_create_root_key(): ", root_key)

print("prefix: ",base58.b58encode_check(b'0488ade4').decode('utf8'))
print("b58: ", convert_to_base58(int(b'0488ade4', 16)))
print("b58: ", convert_to_base58(int('0x0488ade4', 16)))