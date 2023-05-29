#!/usr/bin/env python3
#$ pip install cryptography

from cryptography.fernet import Fernet
from crypto_agama.tools import get_env_key
import base64


input_file = "data/nostr1.txt"

key = Fernet.generate_key()
print("key:",key)
print("key_hex:",key.hex())

"""
key: b'9kZwyLuh49uumNusqelD4FSdpYUCkS0-ywDBp_17lio='
key_hex: 396b5a77794c756.....f31376c696f3d
seve key_hex to .env

new pub.key: npub17sq7mhhl.....6rv7qzjccqvwezd28jsu3eqpx
NOSTR_SEC => 039467ebec344.....50a187d3226d22a4b

"""
try:
    print("-"*39)
    ekey_hex = get_env_key("KFH") # key fernet hexa
    print("env key_hex KFH:",ekey_hex)
    ekey = bytes.fromhex(ekey_hex)
    print("env key:",ekey)

    print("-"*39)
    bkey_hex = get_env_key("ANDREAS1") # andreas BTC - seed1 hexa
    print("seed1 key_hex ANDREAS1:",bkey_hex)
    bkey = base64.urlsafe_b64encode(bytes.fromhex(bkey_hex))
    print("bkey base64:",bkey)
    
    print("-"*39)
    nkey_hex = get_env_key("KNH") # key nostr hexa
    print("nostr key_hex KNH:",nkey_hex)
    # Fernet key must be 32 url-safe base64-encoded bytes
    nkey = base64.urlsafe_b64encode(bytes.fromhex(nkey_hex))
    print("nkey base64:",nkey)
except:
    print("Err. .env keys: KFH/KNH/...")


key = nkey
# key = bkey

cipher_suite = Fernet(key)

# plaintext = "This is the text I want to encrypt."
with open(input_file, "r", encoding="utf-8") as file:
    #text = file.read().replace("\n", " ")
    plaintext = file.read()

ciphertext = cipher_suite.encrypt(plaintext.encode())
encrypted_text = ciphertext.decode()

print("-"*39)
print("Encrypted text:", encrypted_text)
print(len(encrypted_text))

print("-"*39)
decrypted_text = cipher_suite.decrypt(ciphertext).decode()
print("Original text:", decrypted_text)
print(len(decrypted_text))
