from crypto_agama.diffie_hellman import DiffieHellmanKeys

# Alice a Bob si zvolí své soukromé klíče
a = 555555555555  # Soukromý klíč Alice 12x5
b = 333333333333  # Soukromý klíč Bob

# Create an instance of the DiffieHellmanKeys class
"""
dh_a = DiffieHellmanKeys(3,17) # test small g, p
print(dh_a) # basic info
print("is_primitive_root:",dh_a.is_primitive_root(3, 17 )) # True
"""

dh_a = DiffieHellmanKeys()
dh_b = DiffieHellmanKeys()

print("[ Parameters ]")
print("prime/modulo: ", dh_a.p)
print("---generator: ", dh_a.g)

print("[ Private keys ] a, b :")
print(a,b)

print("=" * 30)
print("[ --- Alice --- ]")
alice_private_key = a
alice_public_key = dh_a.generate_public_key(alice_private_key)
print(f'Private key: {(alice_private_key)} | {hex(alice_private_key)}\nPublic key: {hex(alice_public_key)}')

print()
print("[ --- Bob --- ]")
bob_private_key = b
bob_public_key = dh_b.generate_public_key(bob_private_key)
print(f'Private key: {bob_private_key} | {hex(bob_private_key)}\nPublic key: {hex(bob_public_key)}')

print("-" * 30)
print("Confirm")
alice_shared_secret = dh_a.generate_shared_secret(alice_private_key, bob_public_key)
bob_shared_secret = dh_b.generate_shared_secret(bob_private_key, alice_public_key)

print()
print("-" * 30)
print("[ Shared secrets ]")
print(f'A:  {alice_shared_secret}')
print(f'B:  {bob_shared_secret}')

assert alice_shared_secret == bob_shared_secret, "Shared secrets do not match!"
print("Shared secrets match.")

hex32 = dh_a.get_hex_shared32()
print(f"{hex32}  ({len(hex32)})")


"""
[ Parameters ]
prime/modulo:  170141183460469231731687303715884105727 # M127
---generator:  3
[ Private keys ] a, b :
555555555555 333333333333
==============================
[ --- Alice --- ]
Private key: 555555555555 | 0x8159b108e3
Public key: 0x236d61d241c8deec988b449371ef59fb

[ --- Bob --- ]
Private key: 333333333333 | 0x4d9c370555
Public key: 0x20119b431bf77946dab17b2056cacf56
------------------------------
Confirm

------------------------------
[ Shared secrets ]
A:  145101968037071639412442679777990239948
B:  145101968037071639412442679777990239948
Shared secrets match.
6d299f5dae62c2e9c9f2806ae9ab66cc  (32)
"""

print("="*32)
dh = DiffieHellmanKeys()
sk = 555555555555
pk = dh.generate_public_key(sk)
ss = dh.generate_shared_secret(sk, bob_public_key) 
print(dh.get_hex_shared32())

"""
================================
568a721168e50d5665cf5cd889c52235
"""
