#!/usr/bin/env python3
#$ pip install cryptography

from cryptography.fernet import Fernet
from crypto_agama.tools import get_env_key
import base64

from crypto_agama.agama_cipher_fernet import Agama_fernet

input_file_fernet = "data/nostr1_fernet.txt"

try:
    print("-"*39)
    nkey_hex = get_env_key("KNH") # key nostr hexa
    # print("nostr key_hex KNH:",nkey_hex)
    
    # Fernet key must be 32 url-safe base64-encoded bytes
    # nkey = base64.urlsafe_b64encode(bytes.fromhex(nkey_hex))
    # print("nkey base64:",nkey)
except:
    print("Err. .env key KFH")


af = Agama_fernet()
# af.set_key(nkey) # ok
af.set_key(nkey_hex, True)


with open(input_file_fernet, "r", encoding="utf-8") as file:
    ciphertext_f = file.read()

print("="*39)
decrypted_text = af.decrypt(ciphertext_f)
print("Original text from enrypted file:", decrypted_text)
print(len(decrypted_text))
