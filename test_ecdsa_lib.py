# import hashlib
import ecdsa
from crypto_agama.agama_transform_tools import norm_hex, hex_to_wif, wif_to_private_key, measure_time
from crypto_agama.ecc import scalar_multiplication # ,point_addition

key1 = "F000000000000000000000000000000000000000000000000000000000000001"
#key1 = norm_hex("1")

print("key:", key1, len(key1))
wif_key1 = hex_to_wif(key1)
print("--- hex_to_wif | Nekomprimovaný WIF klíč:", wif_key1)
wif_key = wif_key1

# Dekódování WIF na 256bitový privátní klíč
private_key_bytes = wif_to_private_key(wif_key)
print("--- private_key: ", private_key_bytes.hex(), len((str(private_key_bytes.hex()))))


@measure_time
def gen_pub_ecdsa(private_key_bytes):
    # Generování veřejného klíče pomocí ecdsa (secp256k1)
    sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    public_key_bytes = vk.to_string()

    # Rozdělení veřejného klíče na souřadnice x a y
    Kx_lib = int.from_bytes(public_key_bytes[:32], 'big')
    Ky_lib = int.from_bytes(public_key_bytes[32:], 'big')
    return Kx_lib, Ky_lib

Kx, Ky = gen_pub_ecdsa(private_key_bytes)
print(f"--- Veřejný klíč (x, y) pomocí knihovny ecdsa: \n({Kx}, {Ky})")

# --------------------------------------------------------------------------
# Generování veřejného klíče (K) vlastní knihovnou (lib)
@measure_time
def gen_pub_ecdsa_lib(private_key):
    Kx_lib, Ky_lib = scalar_multiplication(private_key)
    return Kx_lib, Ky_lib

# Privátní klíč (k)
k = int(key1, 16)  # Převod z hex na int

Kx_manual, Ky_manual = gen_pub_ecdsa_lib(k)
print(f"--- Veřejný klíč (x, y) přímým výpočtem: \n({Kx_manual}, {Ky_manual})")


"""
key: F000000000000000000000000000000000000000000000000000000000000001 64
--- hex_to_wif | Nekomprimovaný WIF klíč: 5Kdz4Q4NKAq1hTsFWjy2J34E5PuQP7H9qMCFqBwecJcWFqFccMc
--- private_key:  f000000000000000000000000000000000000000000000000000000000000001 64
[ measure_time ] Function 'gen_pub_ecdsa' took 0.0090 seconds to complete.
--- Veřejný klíč (x, y) pomocí knihovny ecdsa:
(113367971205901600938991701977814468019800821204299814295244998056039807689344, 111307963124501043733543508282389961746358683775100625875144825001771122734935)
[ measure_time ] Function 'gen_pub_ecdsa_lib' took 0.0077 seconds to complete.
--- Veřejný klíč (x, y) přímým výpočtem:
(113367971205901600938991701977814468019800821204299814295244998056039807689344, 111307963124501043733543508282389961746358683775100625875144825001771122734935)
"""