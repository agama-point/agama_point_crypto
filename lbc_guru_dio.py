"""
Bitcoin private key database :-D
Page 1 out of 904625697166532776746648320380374280100293470930272690489102837043110636675
"""
import hashlib
import base58
import ecdsa

from crypto_agama.agama_transform_tools import hex_to_wif, wif_to_private_key


key1 = "0000000000000000000000000000000000000000000000000000000000000001"
wif_key1 = hex_to_wif(key1)
print("--- hex_to_wif | Nekomprimovaný WIF klíč:", wif_key1)
wif_key = wif_key1 # "5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf" # .....000001 hex

private_key_bytes = wif_to_private_key(wif_key) # 2. decoce WIF to 256bit priv.key
print("--- private_key: ",private_key_bytes.hex(), len((str(private_key_bytes.hex()))))

# pubkey generate (secp256k1) | SHA-256 + RIPEMD-160
sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
vk = sk.verifying_key

public_key_bytes = b'\x04' + vk.to_string()
sha256_bpk = hashlib.sha256(public_key_bytes).digest()  
ripemd160_bpk = hashlib.new('ripemd160', sha256_bpk).digest()
versioned_payload = b'\x00' + ripemd160_bpk # add ver. ( for Bitcoin Mainnet 0x00)
checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4] # double sha [:4B]
address_bytes = versioned_payload + checksum
bitcoin_address = base58.b58encode(address_bytes).decode()

# --- Compressed
# comp. pub.key (33 Bytes)
public_key_bytes_compressed = b'\x02' + vk.to_string()[:32] if vk.to_string()[-1] % 2 == 0 else b'\x03' + vk.to_string()[:32]
sha256_bpk = hashlib.sha256(public_key_bytes_compressed).digest()
ripemd160_bpk = hashlib.new('ripemd160', sha256_bpk).digest()
versioned_payload = b'\x00' + ripemd160_bpk
checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]
address_bytes = versioned_payload + checksum
compressed_bitcoin_address = base58.b58encode(address_bytes).decode()

# ============================================================

print("[ basic principle testing ]")
print(wif_key, bitcoin_address, compressed_bitcoin_address)

"""
pip install hashlib
pip base58
pip ecdsa

"""
# https://lbc.cryptoguru.org/dio/

"""
test:
--- hex_to_wif | Nekomprimovaný WIF klíč: 5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf
--- private_key:  0000000000000000000000000000000000000000000000000000000000000001 64
[ basic principle testing ]
5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf  1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm 1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH
-------------------------------------------------------------------------------------------------------------------------

Private Key                                          Address                            Compressed Address
1
5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf  1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm 1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH
5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAvUcVfH  1LagHJk2FyCV2VzrNHVqg3gYG4TSYwDV4m  1cMh228HTCiwS8ZsaakH8A8wze1JR5ZsP
5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreB1FQ8BZ  1NZUP3JAc9JkmbvmoTv7nVgZGtyJjirKV1 1CUNEBjYrCn2y1SdiUMohaKUi4wpP326Lb
2
5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreRBLscCA  1Jhh65j6YvN3p4gE2zxcS4MkYkwcTpcCAE 1JYRNTLhwfZJxbaZAPmgx83Fm3s5rx4NeH
5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreRMTfq7A  1BRBsf9HojfnZRMRADLUra6HsDqzZo8LqN 1LeFtfa5ix5bLVKhrKUXpdKjR2uR8CMHAL
5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreRQ8FEcR  1CKxahXbfD6NQnutS4w15DdxLb15Xgvrtw 1Lh78i5CMfzAqVLAYbbpRaemTRrVKfALbB

"""


# https://www.blockchain.com/explorer/addresses/btc/1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm