import ecdsa

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