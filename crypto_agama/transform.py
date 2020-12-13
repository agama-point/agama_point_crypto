"""
crypto_agama.transform
"""

import hashlib, binascii
from hashlib import sha256
# import ecdsa

"""
#Main Net (int dec prefix)
128	80	Private key (WIF, compressed pubkey)
# Test Net (int dec prefix)
111	6F	Testnet pubkey hash
196	C4	Testnet script hash
239	EF	Testnet Private key (WIF, uncompressed pubkey)

# secp256k1 T = (p, a, b, G, n, h)
p = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1 # The proven prime

gX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798 # generator point
gY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8 # generator point
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141  # Number of points in the field
a = 0; b = 7 # from elliptic curve equation y^2 = x^3 + a*x + b

secp256k1curve = ecdsa.ellipticcurve.CurveFp(p, a, b)
secp256k1point = ecdsa.ellipticcurve.Point(secp256k1curve, gX,	gY, n)
CURVE_TYPE = ecdsa.curves.Curve('secp256k1', secp256k1curve, secp256k1point, (1, 3, 132, 0, 10))
#"""


DEBUG = True

# CURVE_TYPE = ecdsa.curves.SECP256k1

BASE_58_CHARS = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
BASE_58_CHARS_LEN = len(BASE_58_CHARS)

MAINNET_PREFIX = '80'
TESTNET_PREFIX = 'EF'


def hashString(string):
    """
    Return a SHA-256 hash of the given string
    """
    return sha256(string.encode('utf-8')).hexdigest()


def convertToBase58(num):
    sb = ''

    while (num > 0):
        r = num % 58   # divide by 58 and gives the remainder
        sb = sb + BASE_58_CHARS[r]
        num = num // 58
    return sb[::-1]


def numToWIF(numPriv,prefix=MAINNET_PREFIX,leading="1"):
  privKeyHex = prefix+hex(numPriv)[2:].strip('L').zfill(64)
  privKeySHA256Hash = sha256(binascii.unhexlify(privKeyHex)).hexdigest()
  privKeyDoubleSHA256Hash = sha256(binascii.unhexlify(privKeySHA256Hash)).hexdigest()
  checksum = privKeyDoubleSHA256Hash[:8]
  wifNum = int(privKeyHex + checksum, 16)
  if DEBUG: print("DEBUG-wifNum: ", wifNum)
  wifNum58 = convertToBase58(wifNum)
  if DEBUG: print("DEBUG-wifNum58: ", wifNum58)
  return leading + wifNum58


def WIFToNum(wifPriv):
    numPriv = 0
    for i in range(len(wifPriv)):
      numPriv += BASE_58_CHARS.index(wifPriv[::-1][i])*(BASE_58_CHARS_LEN**i)

    numPriv = numPriv/(2**32)%(2**256)
    return numPriv


def isValidWIF(wifPriv):
  return numToWIF(WIFToNum(wifPriv)) == wifPriv


def numToAddress(numPriv):
    pko = ecdsa.SigningKey.from_secret_exponent(numPriv, CURVE_TYPE)
    pubkey = binascii.hexlify(pko.get_verifying_key().to_string())
    pubkeySHA256Hash = sha256(binascii.unhexlify('04' + pubkey)).hexdigest()
    pubkeySHA256RIPEMD160Hash = hashlib.new('ripemd160', binascii.unhexlify(pubkeySHA256Hash)).hexdigest()

    hash1 = sha256(binascii.unhexlify('00' + pubkeySHA256RIPEMD160Hash)).hexdigest()
    hash2 = sha256(binascii.unhexlify(hash1)).hexdigest()
    checksum = hash2[:8]

    encodedPubKeyHex = pubkeySHA256RIPEMD160Hash + checksum
    encodedPubKeyNum = int(encodedPubKeyHex, 16)

    base58CharIndexList = []
    while encodedPubKeyNum != 0:
      base58CharIndexList.append(encodedPubKeyNum % BASE_58_CHARS_LEN)
      encodedPubKeyNum /= BASE_58_CHARS_LEN

    m = 0
    while encodedPubKeyHex[0 + m : 2 + m] == '00':
        base58CharIndexList.append(0)
        m = m + 2

    address = ''
    for i in base58CharIndexList:
      address = BASE_58_CHARS[i] + address
    
    return '1' + address


def seedWords():
    from crypto_agama.seed_english_words import english_words_bip39
    return english_words_bip39.split(",")


def hexToBin(hexn):
  #bin(private_key1.to_bin())
  return (bin(int(hexn, base=16)))


def binToHex(binx):
   return hex(int(binx, 2))


def bin8tohex(strh):	
   tB = []
   tBs ="0x"	
   #print("len:"+str(len(strh)))
   try:
     for ib in range (0,160):
       Bapp = binToHex("0b"+str(strh)[2+ib*8:2+ib*8+8])	 
       tB.append(Bapp)
       print(Bapp,end="")
       tBs = tBs+tB[ib][2:4]
       #print ib,tB[ib]
   except: 
     err=True
     print(ib,end="")

   return tBs


def strToBin(str):
  return bin(reduce(lambda x, y: 256*x+y, (ord(c) for c in str), 0))


def binToStr(bin):
  n = int(bin, 2)
  return binascii.unhexlify('%x' % n)


def textToBits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def textFromBits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)


def intToBytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))  
