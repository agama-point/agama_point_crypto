from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


# Encryption and decryption key (must be 16, 24, or 32 bytes long)
# key = get_random_bytes(16) 
key_hex ="752f85035563adff915ac0c3ae1252ed" # dde.Trezor
key = bytes.fromhex(key_hex)

# Initialization vector (IV) for CBC mode (must be 16 bytes long)
#iv = get_random_bytes(16)
iv_hex = "0c1e24e5917779d297e14d45f14e1a1a" # dde.Andreas
iv = bytes.fromhex(iv_hex)

plaintext = b'This is a secret AgamaPoint message' # Text we want to encrypt

cipher = AES.new(key, AES.MODE_CBC, iv) # Create AES object for encryption
print("key_hex:")
print(key.hex())
print("*"*32)

print("AES.MODE_CBC:", AES.MODE_CBC)
print("iv_hex:", iv.hex())

padded_plaintext = pad(plaintext, AES.block_size) # Padding plaintext to the correct length (blocks of 16 bytes)
ciphertext = cipher.encrypt(padded_plaintext)     # Encryption
print("Encrypted text | hex", ciphertext.hex())

decipher = AES.new(key, AES.MODE_CBC, iv)    # Create AES object for decryption

decrypted_padded_plaintext = decipher.decrypt(ciphertext) # Decryption
decrypted_plaintext = unpad(decrypted_padded_plaintext, AES.block_size) # Removing padding
print(f'Decrypted text: {decrypted_plaintext}')


"""
key_hex:
752f85035563adff915ac0c3ae1252ed
********************************
AES.MODE_CBC: 2
iv_hex: 0c1e24e5917779d297e14d45f14e1a1a
Encrypted text | hex 108a6eacbc453432194c24595db2d62124ef3d0a5d311d5109947c62f0150e2a0aa3c0d90361db27bd434deaada1c387
Decrypted text: b'This is a secret AgamaPoint message'
"""