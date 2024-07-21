from crypto_agama.diffie_hellman import DiffieHellmanKeys

# Parameters for Diffie-Hellman
g = 123  # Generátor 2, 123
p = 170141183460469231731687303715884105727  # Modulo prvočíslo 17, 9973, 1000009999, 123456789011, M61=2305843009213693951, M127
print("M127:", 2**127-1, " :.",len(str(2**127-1))) #  Mersenne prime M127 :. 39 digits
# https://cs.wikipedia.org/wiki/Mersennovo_prvo%C4%8D%C3%ADslo

# Alice a Bob si zvolí své soukromé klíče
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
M127: 170141183460469231731687303715884105727 :. 39
[ Parameters ]
prime/modulo:  170141183460469231731687303715884105727
--- genrator:  123
[ Private keys ] a, b :
555555555555 333333333333
==============================
[ --- Alice --- ]
Private key: 555555555555 | 0x8159b108e3
Public key: 0x67043bb183b169e8d9dd533e68a21d00

[ --- Bob --- ]
Private key: 333333333333 | 0x4d9c370555
Public key: 0x45de70dbe50d0d9546c78999bd7b14a7
------------------------------
Confirm

------------------------------
[ Shared secrets ]
A:  115032458178017498334018774030333846069
B:  115032458178017498334018774030333846069
Shared secrets match.
568a721168e50d5665cf5cd889c52235  (32)
"""

print("="*32)
dh = DiffieHellmanKeys(p, g)
sk = 555555555555
pk = dh.generate_public_key(sk)
ss = dh.generate_shared_secret(sk, bob_public_key)
print(dh.get_hex_shared32())

"""
================================
568a721168e50d5665cf5cd889c52235
"""
