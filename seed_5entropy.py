from crypto_agama.agama_seed_tools import seed_words, mnemonic_info, words_to_bip39nums
from crypto_agama.agama_seed_tools import BIP39Functions, entropy_normalize, seed_words

bip39f = BIP39Functions()

print("-"*32)
print("[ --- test entropy --- ]")

def seed_test(entropy, passphrase=""):
    # entropy = entropy_normalize(entropy)
    print("input entropy:", entropy)
    phrase = bip39f.entropy_to_phrase(entropy)
    print("BIP39Functions - phrase:",phrase)
    print("is_valid | reverese_entropy:", bip39f.is_checksum_valid(phrase, reverse_entropy=True))
    mnemonic_info(phrase)
    return phrase

# ===================================================================
en_hex = "80808080808080808080808080808080"
words = seed_test(en_hex)
nums12 = words_to_bip39nums(words)

print("\n",nums12)
#seed = mnemo_to_seed(words)
#print(seed)

"""
bip39 vectors: https://github.com/trezor/python-mnemonic/blob/master/vectors.json
"80808080808080808080808080808080"
"letter advice cage absurd amount doctor acoustic avoid letter advice cage above"

[ --- test entropy --- ]
input entropy: 80808080808080808080808080808080
BIP39Functions - phrase: letter advice cage absurd amount doctor acoustic avoid letter advice cage above
is_valid | reverese_entropy: (True, True, '80808080808080808080808080808080')
--------------------------------------------------------------------------------
[mnemonic_info]
letter advic...e cage above ( 12 )
1028 32 257 8 64 514 16 128 1028 32 257 4
validate:  (True, True)
--------------------------------------------------------------------------------
letter 1028 |advice 32 |cage 257 |absurd 8 |amount 64 |doctor 514 |acoustic 16 |avoid 128 |letter 1028 |advice 32 |cage 257 |above 4 |
 [1028, 32, 257, 8, 64, 514, 16, 128, 1028, 32, 257, 4]
"""