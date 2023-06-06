from agama_nostr.client import Client 
from crypto_agama.transform import hash_sha256_str
from crypto_agama.agama_cipher import xor_crypt
from crypto_agama.tools import get_env_key
# export PYTHONPATH="$PYTHONPATH:./"

try:
    print("-"*39)
    AGAMA_KEY_0 = get_env_key("AGAMA_KEY_0") # key nostr hexa
    print("AGAMA_KEY_0",AGAMA_KEY_0)
except:
    print("Err. - set .env")

shagama = hash_sha256_str("agama")
print("hash_sha256:",shagama)
# hash_sha256: 52589fac98630c603bd5c2b08cb0f6ccf273cc4a4772f0ff28d49a01bc7d2f4b

k0 = "fe1b24847779704934f15ea7c7c751709e20a5f8b218cde0c1843200a168b448"

print("-"*39)
print("data", k0)
print("-key", AGAMA_KEY_0)
c_data = xor_crypt(k0,AGAMA_KEY_0)
print("-xor", c_data)
n_data = xor_crypt(c_data,AGAMA_KEY_0)
print("-new", n_data)
"""
    #================================================================
    #         1         2         3         4         5         6  64
    #1234567890123456789012345678901234567890123456789012345678901234 
data fe1b24847779704934f15ea7c7c751709e20a5f8b218cde0c1843200a168b448
-key 52589fac98630c603bd5c2b08cb0f6ccf273cc4a4772f0ff28d49a01bc7d2f4b
-xor ac43bb28ef1a7c290f249c174b77a7bc6c5369b2f56a3d1fe950a8011d159b03
-new fe1b24847779704934f15ea7c7c751709e20a5f8b218cde0c1843200a168b448

data = key > xor = 0
key = 0    > xor = data
"""

k = k0
nc = Client(k, False)
nc.print_keys_info()
print("pub_key hexa:")
print(nc.public_key)
pk = nc.public_key.bech32()

"""
Private key: 
nsec1lcdjfprh09cyjd83t6nu0363wz0zpf0ckgvvmcxpsseqpgtgk3yq6e84gu => 
fe1b24847779704934f15ea7c7c751709e20a5f8b218cde0c1843200a168b448
Public key:  
npub1zrqv6mdcjymcu650tx46wzvumyjhk09pagcm2q5jfkqx0k6p5lgsnycjrs
================================================================
         1         2         3         4         5         6  64
1234567890123456789012345678901234567890123456789012345678901234 
fe1b24847779704934f15ea7c7c751709e20a5f8b218cde0c1843200a168b448 SEC
10c0cd6db891378e6a8f59aba7099cd9257b3ca1ea31b502924d8067db41a7d1 PUB
================================================================
52589fac98630c603bd5c2b08cb0f6ccf273cc4a4772f0ff28d49a01bc7d2f4b
hash_sha256_str("agama") 
----------------------------------------------------------------
"""