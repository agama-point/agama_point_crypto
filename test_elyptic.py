import math, ecdsa
from ecdsa import SECP256k1
from ecdsa.ecdsa import Public_key
SECP256k1_GEN = SECP256k1.generator


print("--- simple test ---")

# y^2 = x^3 + a*x + b

a = 1
b = 1
for x in range(-10,10):
   temp = x*x*x + a*x + b
   y = math.sqrt(abs(temp))
   print(x, y, temp)

print()


# prime 281
# (y^2 -x^3 + 3*x) mod p = 0

print(" --- prime # mod ---")
p = 281

for x in range(100):
   for y in range(100):
      temp = (y*y - x*x*x + 3*x)

      if(temp % p == 0):
         print(x, y, temp, temp % p)


print()

"""
#Main Net (int dec prefix)
128	80	Private key (WIF, compressed pubkey)
# Test Net (int dec prefix)
111	6F	Testnet pubkey hash
196	C4	Testnet script hash
239	EF	Testnet Private key (WIF, uncompressed pubkey)
"""

# secp256k1 T = (p, a, b, G, n, h)
p = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1 # The proven prime

gX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798 # generator point
gY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8 # generator point
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141  # Number of points in the field
a = 0
b = 7 
# from elliptic curve equation y^2 = x^3 + a*x + b
print(gX, gY, a, b)


secp256k1curve = ecdsa.ellipticcurve.CurveFp(p, a, b)
secp256k1point = ecdsa.ellipticcurve.Point(secp256k1curve, gX,	gY, n)
CURVE_TYPE = ecdsa.curves.Curve('secp256k1', secp256k1curve, secp256k1point, (1, 3, 132, 0, 10))
#"""

#CURVE_TYPE = ecdsa.curves.SECP256k1

print(CURVE_TYPE)

print("-"*50)


"""
def serialize_curve_point(p):
   x, y = K.x(), K.y()
   if y & 1:
      return b'\x03' + x.to_bytes(32, 'big')
   else:
      return b'\x02' + x.to_bytes(32, 'big')
"""

def curve_point_from_int(k):
   return Public_key(SECP256k1_GEN, SECP256k1_GEN * k).point

def fingerprint_from_private_key(k):
   K = curve_point_from_int(k)
   K_compressed = serialize_curve_point(K)
   identifier = hashlib.new(
      'ripemd160',
      hashlib.sha256(K_compressed).digest(),
   ).digest()
   return identifier[:4]



depth = 0
parent_fingerprint = None
child_number = None
"""
rivate_key = master_private_key
chain_code = master_chain_code

p = curve_point_from_int(private_key)

print("curve_point_from_int",p)
"""

"""
public_key_bytes = serialize_curve_point(p)
print(f'public key: 0x{public_key_bytes.hex()}')
"""