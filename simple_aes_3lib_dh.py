from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from crypto_agama.diffie_hellman import DiffieHellmanKeys

# from Crypto.Random import get_random_bytes
### pip install pycryptodome -> Crypto

# Parameters for Diffie-Hellman
g = 123  # Generátor
p = 170141183460469231731687303715884105727  # Modulo prvočíslo
print("M127:", 2**127-1, " :.",len(str(2**127-1))) #  Mersenne prime M127 :. 39 digits

a = 555555555555  # Soukromý klíč Alice 12x5
b = 333333333333  # Soukromý klíč Bob

# Create an instance of the DiffieHellmanKeys class
dh_a = DiffieHellmanKeys(p, g)
dh_b = DiffieHellmanKeys(p, g)


print("[ Parameters ]")
print("prime/modulo: ", dh_a.p)
print("--- genrator: ", dh_a.g)

print("[ Private keys ] a, b :")
print(a,b)

print("[ --- Alice --- ]")
alice_private_key = a
alice_public_key = dh_a.generate_public_key(alice_private_key)
print(f'Private key: {(alice_private_key)} | {hex(alice_private_key)}\nPublic key: {hex(alice_public_key)}')

print("[ --- Bob --- ]")
bob_private_key = b
bob_public_key = dh_b.generate_public_key(bob_private_key)
print(f'Private key: {bob_private_key} | {hex(bob_private_key)}\nPublic key: {hex(bob_public_key)}')

# print("Confirm")
alice_shared_secret = dh_a.generate_shared_secret(alice_private_key, bob_public_key)
bob_shared_secret = dh_b.generate_shared_secret(bob_private_key, alice_public_key)

print("[ Shared secrets ]")
print(f'A:  {alice_shared_secret}')
print(f'B:  {bob_shared_secret}')

assert alice_shared_secret == bob_shared_secret, "Shared secrets do not match!"
print("Shared secrets match.")

hex32 = dh_a.get_hex_shared32()
print(f"{hex32}  ({len(hex32)})")


"""
...
print("A, B",A, B)
# shared secret 
s_Alice = (B ** a) % n
s_Bob = (A ** b) % n
...
assert s_Alice == s_Bob
"""

# Symmetric cipher
def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return ciphertext

def decrypt_message(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode()

# Creating a symmetric key from the shared key
symmetric_key = str(alice_shared_secret).zfill(16)[:16].encode()
print("symmetric_key:", symmetric_key, symmetric_key.hex())
print("===========================================")


# Zpráva od Alice pro Boba
message = "agama test"

# Zašifrování zprávy
encrypted_message = encrypt_message(message, symmetric_key)
print("encrypted_message:", encrypted_message.hex())

# Dešifrování zprávy Bobem
decrypted_message = decrypt_message(encrypted_message, symmetric_key)
print("decrypted_message:", decrypted_message)

"""
M127: 170141183460469231731687303715884105727  :. 39
[ Parameters ]
prime/modulo:  170141183460469231731687303715884105727
--- genrator:  123
[ Private keys ] a, b :
555555555555 333333333333
[ --- Alice --- ]
Private key: 555555555555 | 0x8159b108e3
Public key: 0x67043bb183b169e8d9dd533e68a21d00
[ --- Bob --- ]
Private key: 333333333333 | 0x4d9c370555
Public key: 0x45de70dbe50d0d9546c78999bd7b14a7
[ Shared secrets ]
A:  115032458178017498334018774030333846069
B:  115032458178017498334018774030333846069
Shared secrets match.
568a721168e50d5665cf5cd889c52235  (32)
symmetric_key: b'1150324581780174' 31313530333234353831373830313734
===========================================
encrypted_message: 3ab9ac40f6653f0651e222da80938628
decrypted_message: agama test
"""
