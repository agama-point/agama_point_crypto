"""
Agama Point - simple "AES"_XOR example
CBC (Cipher Block Chaining)
C1 = (IV ⊕ B1) ⊕ K
C2 = (B2 ⊕ C1) ⊕ K
...
"""
from crypto_agama.cipher_cbc_xor import CBC_XOR


key_hex = "0c1e24e5917779d297e14d45f14e1a1a" # andreas
key = bytes.fromhex(key_hex) 
iv = b'xyz_iv0987654321' # 16 B, len(hex) = 32, 32*4 bin == 128b
plaintext = b'agama test 567 - a neco navic? ...ale asi jen bez diakritiky :('  # Example plaintext (32 bytes)
cbc = CBC_XOR(key, iv)

print("key: ", key.hex() ," :",len(str(key.hex())))
print("_iv: ", iv.hex()) # hex_str.zfill(16)[:16]
print("block_size:", cbc.block_size)

print("-"*30)
ciphertext = cbc.encrypt(plaintext)  # Encryption
print(f'Ciphertext: {ciphertext.hex()}')

decrypted_text = cbc.decrypt(ciphertext)  # Decryption
print(f'Decrypted text: {decrypted_text.decode()}')

"""
key:  0c1e24e5917779d297e14d45f14e1a1a  : 32
_iv:  78797a5f697630393837363534333231
block_size: 16
------------------------------
Ciphertext: 15003fd799213d8edca25b45f34a0806397f3b5c6d352b7c25226069613b32321b4f7ed5996233dddbe34749fe554a4d6d713e59697e3866386b61752f217856
Decrypted text: agama test 567 - a neco navic? ...ale asi jen bez diakritiky :(
"""