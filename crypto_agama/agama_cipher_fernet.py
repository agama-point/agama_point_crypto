#!/usr/bin/env python3
#$ pip install cryptography

from cryptography.fernet import Fernet
# from crypto_agama.tools import get_env_key
import base64


__version__ = "0.1.0" # 2023/05/29


class Agama_fernet():
    def __init__(self, debug=True):
        self.key = None


    def new_key_generate(self, print_out=True):
        self.key = Fernet.generate_key()

        if print_out:
            print("[New key generate]") 
            print("key_hex:",self.key.hex())
        return self.key


    def set_key(self, key, nostr=False):
        if nostr:
            self.key = base64.urlsafe_b64encode(bytes.fromhex(key))
        else:
            self.key = key
        self.cipher_suite = Fernet(self.key)


    def encrypt(self, plaintext):
        ciphertext = self.cipher_suite.encrypt(plaintext.encode())
        encrypted_text = ciphertext.decode()
        return encrypted_text


    def decrypt(self, ciphertext):
        decrypted_text = self.cipher_suite.decrypt(ciphertext).decode()
        return decrypted_text
