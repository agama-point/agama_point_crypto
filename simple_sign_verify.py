from hashlib import sha256
from crypto_agama.diffie_hellman import DiffieHellmanKeys
from crypto_agama.cipher_cbc_xor import CBC_XOR

print("\n[ --- KEY GENERATION --- ]")
# Parameters for Diffie-Hellman
g = 123  # Generátor 2, 123
p = 170141183460469231731687303715884105727  # Modulo prvočíslo 17, 9973, 1000009999, 123456789011, M61=2305843009213693951, M127

# Alice and Bob choose their private keys 
a = 555555555555
b = 333333333333 

# Create an instance of the DiffieHellmanKeys class
dh_a = DiffieHellmanKeys(p, g)
dh_b = DiffieHellmanKeys(p, g)

print("--- Alice:")
alice_private_key = a
alice_public_key = dh_a.generate_public_key(alice_private_key)
print(f'Private key: {(alice_private_key)} | {hex(alice_private_key)}\nPublic key: {hex(alice_public_key)} :. {len(str(alice_public_key))}')

print("--- Bob:")
bob_private_key = b
bob_public_key = dh_b.generate_public_key(bob_private_key)
print(f'Private key: {bob_private_key} | {hex(bob_private_key)}\nPublic key: {hex(bob_public_key)} :. {len(str(bob_public_key))}')

shared_secret = dh_a.generate_shared_secret(alice_private_key, bob_public_key)
shared_secret_hex32 = dh_a.get_hex_shared32()
print(f"{shared_secret_hex32}  ({len(shared_secret_hex32)})")

print("\n[  --- SIGN ---  ]")
cbc_iv = bytes.fromhex("0c1e24e5917779d297e14d45f14e1a1a") # andreas
cbc_key = bytes.fromhex(shared_secret_hex32) 

message_plaintext_bytes = b'a short text for signing and subsequent verification | Agama 123'
print("message_plaintext_bytes:", message_plaintext_bytes)
cbc = CBC_XOR(cbc_key, cbc_iv)

hash_message = sha256(message_plaintext_bytes).digest()  # Hash the message and get the digest

print("cbc_key: ", cbc_key.hex() ," :.. ",len(str(cbc_key.hex())))
print("cbc_iv_: ", cbc_iv.hex()) # hex_str.zfill(16)[:16]
print("cbc_block_size:", cbc.block_size)

print("Encryption ->")
ciphertext = cbc.encrypt(hash_message)  # Encryption
print(f'Ciphertext: {ciphertext.hex()}')

print("\n[ --- VERIFY --- ]")
decrypted_hash = cbc.decrypt(ciphertext)  # Decryption
print(f'Decrypted hash: {decrypted_hash.hex()}')

# Bob computes the hash of the original message
bob_computed_hash = sha256(message_plaintext_bytes).digest()

# Verification
if decrypted_hash == bob_computed_hash:
    print("Verification successful: The decrypted hash matches the original hash.")
    print("Hash:", bob_computed_hash.hex(), ":.", len(str(bob_computed_hash.hex())))
else:
    print("Verification failed: The decrypted hash does not match the original hash.")


"""
[ --- KEY GENERATION --- ]
--- Alice:
Private key: 555555555555 | 0x8159b108e3
Public key: 0x67043bb183b169e8d9dd533e68a21d00 :. 39
--- Bob:
Private key: 333333333333 | 0x4d9c370555
Public key: 0x45de70dbe50d0d9546c78999bd7b14a7 :. 38
568a721168e50d5665cf5cd889c52235  (32)

[  --- SIGN ---  ]
message_plaintext_bytes: b'a short text for signing and subsequent verification | Agama 123'
cbc_key:  568a721168e50d5665cf5cd889c52235  :..  32
cbc_iv_:  0c1e24e5917779d297e14d45f14e1a1a
cbc_block_size: 16
Encryption ->
Ciphertext: be572caac7fb955a96f16b28f759ded7094668dff975431b7a777be4d1a1c2004fdc0ade81805e5d0fa8372c4874f025

[ --- VERIFY --- ]
Decrypted hash: e4c37a5e3e69e1de64df7ab58fd2e6f8e19b3664566bdb1789494c14af3d3ee2
Verification successful: The decrypted hash matches the original hash.
Hash: e4c37a5e3e69e1de64df7ab58fd2e6f8e19b3664566bdb1789494c14af3d3ee2 :. 64
"""
