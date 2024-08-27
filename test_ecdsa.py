import hashlib
import ecdsa
from crypto_agama.agama_transform_tools import hex_to_wif, wif_to_private_key

def norm64(hex_str):
    # Normalize the input to a 64-character hexadecimal string
    return hex_str.zfill(64)

#key1 = "0000000000000000000000000000000000000000000000000000000000000111"
key1 = norm64("123")
print("key:", key1)
wif_key1 = hex_to_wif(key1)
print("--- hex_to_wif | Nekomprimovaný WIF klíč:", wif_key1)
wif_key = wif_key1

# Dekódování WIF na 256bitový privátní klíč
private_key_bytes = wif_to_private_key(wif_key)
print("--- private_key: ", private_key_bytes.hex(), len((str(private_key_bytes.hex()))))

# Generování veřejného klíče pomocí ecdsa (secp256k1)
sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
vk = sk.verifying_key
public_key_bytes = vk.to_string()

# Rozdělení veřejného klíče na souřadnice x a y

Kx_lib = int.from_bytes(public_key_bytes[:32], 'big')
Ky_lib = int.from_bytes(public_key_bytes[32:], 'big')
print(f"--- Veřejný klíč (x, y) pomocí knihovny ecdsa: \n({Kx_lib}, {Ky_lib})")

# ----- secp256k1 parametry -----
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F  # Modul
A = 0
B = 7

# ----- bod G -----
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

# ----- Point addition (sčítání bodů) -----
def point_addition(x1, y1, x2, y2, p):
    if x1 == x2 and y1 == y2:
        m = (3 * x1**2 + A) * pow(2 * y1, -1, p) % p  # Doubling the point
    else:
        m = (y2 - y1) * pow(x2 - x1, -1, p) % p  # Regular point addition
    
    x3 = (m**2 - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    
    return x3, y3

# Scalar multiplication (násobení bodu na křivce)
def scalar_multiplication(k, x, y, p):
    x_res, y_res = x, y
    for bit in bin(k)[3:]:
        x_res, y_res = point_addition(x_res, y_res, x_res, y_res, p)  # Point doubling
        if bit == '1':
            x_res, y_res = point_addition(x_res, y_res, x, y, p)  # Point addition
    return x_res, y_res

# Privátní klíč (k)
k = int(key1, 16)  # Převod z hex na int

# Generování veřejného klíče (K) ručně
Kx_manual, Ky_manual = scalar_multiplication(k, Gx, Gy, P)
print(f"--- Veřejný klíč (x, y) přímým výpočtem: \n({Kx_manual}, {Ky_manual})")
