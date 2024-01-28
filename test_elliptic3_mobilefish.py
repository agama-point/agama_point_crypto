# Super simple Elliptic Curve Presentation. No imported libraries, wrappers, nothing. 
# For educational purposes only. Remember to use Python 2.7.6 or lower. You'll need to make changes for Python 3.
# Original source: https://github.com/wobine/blackboard101/blob/master/EllipticCurvesPart4-PrivateKeyToPublicKey.py

DEBUG = True

# secp256k1 domain parameters
Pcurve = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 -1 # The proven prime
Acurve, Bcurve = 0, 7 # These two defines the elliptic curve. y^2 = x^3 + Acurve * x + Bcurve
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
GPoint = (Gx,Gy)   # This is our generator point.
N=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141 # Number of points in the field

# -------------- Replace with any private key -----------------------
privKey = 0x79FE45D61339181238E49424E905446A35497A8ADEA8B7D5241A1E7F2C95A04D


def modinv(a,n=Pcurve): #Extended Euclidean Algorithm/'division' in elliptic curves
    lm, hm = 1, 0
    low, high = a%n, n
    while low > 1:
        ratio = high/low
        nm, new = hm-lm*ratio, high-low*ratio
        lm, low, hm, high = nm, new, lm, low
    return lm % n


def ECadd(a,b): # EC Addition
    if DEBUG:
            print("ADD")
    LamAdd = ((b[1]-a[1]) * modinv(b[0]-a[0],Pcurve)) % Pcurve
    x = (LamAdd*LamAdd-a[0]-b[0]) % Pcurve
    y = (LamAdd*(a[0]-x)-a[1]) % Pcurve
    return (x,y)


def ECdouble(a): # EC Doubling
    if DEBUG:
            print("DUB")
    Lam = ((3*a[0]*a[0]+Acurve) * modinv((2*a[1]),Pcurve)) % Pcurve
    x = (Lam*Lam-2*a[0]) % Pcurve
    y = (Lam*(a[0]-x)-a[1]) % Pcurve
    return (x,y)


def EccMultiply(GenPoint,ScalarHex): # Doubling & Addition
    if ScalarHex == 0 or ScalarHex >= N: raise Exception("Invalid Scalar/Private Key")
    ScalarBin = str(bin(ScalarHex))[2:]
    print("_GenPoint: ",GenPoint)
    print("_ScalarBin: ",ScalarBin)
    print("_ScalarHex: ",ScalarHex)
    Q = GenPoint
    for i in range (1, len(ScalarBin)):
        if DEBUG:
            print(i, ScalarBin[i], Q)
        Q = ECdouble(Q)
        if ScalarBin[i] == "1":
            Q = ECadd(Q, GenPoint)
    return (Q)


print("******* Bitcoin Public Key Generation *********")
print("Pcurve: ",Pcurve)
print("(2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 -1)")
print("GPoint: ", GPoint)
print("-"*50)
print()

PublicKey = EccMultiply(GPoint,privKey)
print("--- the public key:")
print(PublicKey) #.hex())

"""
print("the public key x-value (Hex):")
#print("0x" + "%064x" + str(PublicKey[0]))
print(PublicKey[0])
print()

print("the public key y-value (Hex):")
#print("0x" + "%064x" % PublicKey[1])
print(PublicKey[1])
print()

print("the public key (Hex):")
# print("0x" + "%064x" % PublicKey[0] + "%064x" % PublicKey[1])
print()
"""

"""
******* Bitcoin Public Key Generation *********
Pcurve:  115792089237316195423570985008687907853269984665640564039457584007908834671663
(2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 -1)
GPoint:  (55066263022277343669578718895168534326250603453777594175500187360389116729240, 32670510020758816978083085130507043184471273380659243275938904335757337482424)
--------------------------------------------------

_GenPoint:  (55066263022277343669578718895168534326250603453777594175500187360389116729240, 32670510020758816978083085130507043184471273380659243275938904335757337482424)
_ScalarBin:  111100111111110010001011101011000010011001110010001100000010010001110001110010010010100001001001110100100000101010001000110101000110101010010010111101010001010110111101010100010110111110101010010010000011010000111100111111100101100100101011010000001001101
_ScalarHex:  55179115824979878594564946684576670362812219109178118526265814188406326272077
1 1 (55066263022277343669578718895168534326250603453777594175500187360389116729240, 32670510020758816978083085130507043184471273380659243275938904335757337482424)
DUB
ADD
2 1 (5.506626302227735e+76, 3.267051002075881e+76)
DUB
ADD
...
"""