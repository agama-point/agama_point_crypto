"""
https://github.com/josh-kean/BIP39/blob/master/test_functions.py
"""

from crypto_agama.agama_seed_tools import HashingFunctions, mnemo_to_seed, mnemonic_info
from cryptos import *
from crypto_agama.agama_cryptos import coin_info, wallet_info, addr3
# from crypto_agama.seed_tools import seed_words, mnemonic_info, words_to_4ch

"""
def ent_to_phrase(entropy): 
    #tests to see if provided entropy produces desired word list
    hashes = HashingFunctions()
    hashes.get_input(entropy)
    hashes.create_check_sum()
    hashes.create_word_list()
    phrase = hashes.result_word_list
    return phrase
"""


def phrase_to_key(phrase): 
    #tests to see if word list converts to desired master key
    hashes = HashingFunctions(None, phrase)
    hashes.create_binary_seed()
    return hashes.binary_seed

"""
print("bip39josh test")
phrase = ent_to_phrase("00000000000000000000000000000000")
print("HashingFunctions - phrase:",phrase)
"""

hashes = HashingFunctions()
phrase = hashes.entropy_to_phrase("00000000000000000000000000000000")
print("HashingFunctions - phrase:",phrase)

#hashes = HashingFunctions(None, phrase)
#binary_seed = hashes.phrase_to_key(phrase)
binary_seed = phrase_to_key(phrase)
# binary_seed = hashes.create_binary_seed() # x None

print("HashingFunctions - binary_seed:",binary_seed)
words = phrase
mnemo_seed = mnemo_to_seed(words)


print("*"*3)
phrase = hashes.entropy_to_phrase("ffffffffffffffffffffffffffffffff")
mnemonic_info(phrase)
words = phrase
mnemo_seed = mnemo_to_seed(words)
binary_seed = phrase_to_key(phrase)
print("HashingFunctions - binary_seed:",binary_seed)


"""
HashingFunctions - phrase: 
abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about
HashingFunctions - binary_seed: 
c55257c360c07c72029aebc1b53c05ed0362ada38ead3e3e9efa3708e53495531f09a6987599d18264c1e1c92f2cf141630c7a3c4ab7c81b2f001698e7463b04
***
--------------------------------------------------------------------------------
[mnemonic_info]
zoo zoo zoo ...oo zoo wrong ( 12 )
2047 2047 2047 2047 2047 2047 2047 2047 2047 2047 2047 2037
validate:  (True, True)
--------------------------------------------------------------------------------
HashingFunctions - binary_seed: 
ac27495480225222079d7be181583751e86f571027b0497b5b5d11218e0a8a13332572917f0f8e5a589620c6f15b11c61dee327651a14c34e18231052e48c069
mnemo_to_seed_hex (abadon): 
1d89e2f0ad0032fc51ae8b1b0f445b9144355d8a4977d98269e9ddf65d9f69f0c30bd0bac902fe17f6378dde66ed7244cd2e1eb00a6745354f290ca270b2b25d
--------------------------------------------------------------------------------
[mnemonic_info]
zoo zoo zoo ...oo zoo wrong ( 12 )
2047 2047 2047 2047 2047 2047 2047 2047 2047 2047 2047 2037
validate:  (True, True)
"""


print("mnemo_to_seed_hex (abadon): ", mnemo_seed.hex())
mnemonic_info(words)
coin = Bitcoin() # Main default # coin = Bitcoin(testnet=True)
coin_info(coin)

print("\n","="*32)
print("BIP39-BIP44 | Standard Wallets:")
wallet = coin.wallet(words)
addr3(coin,wallet)

print("\n","="*32)
print("BIP39-BIP49 | Segwit Wallets:")
wallet = coin.p2wpkh_p2sh_wallet(words)
addr3(coin,wallet)

print("\n","="*32)
print("BIP39-BIP84 | New Segwit Wallets:")
wallet = coin.p2wpkh_wallet(words)
addr3(coin,wallet)

"""
phrase = entropy_to_phrase0("000000000000000000000000000000000000000000000000")
mnemonic_info(phrase)
"""