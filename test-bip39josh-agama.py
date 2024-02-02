"""
https://github.com/josh-kean/BIP39/blob/master/test_functions.py
https://github.com/scgbckbone/btc-hd-wallet
"""
from mnemonic import Mnemonic
from crypto_agama.agama_seed_tools import HashingFunctions, mnemo_to_seed, mnemonic_info, create_root_key
from cryptos import *
from crypto_agama.agama_cryptos import coin_info, wallet_info, addr3
# from crypto_agama.seed_tools import seed_words, mnemonic_info, words_to_4ch


def phrase_to_key(phrase): 
    #tests to see if word list converts to desired master key
    hashes = HashingFunctions(None, phrase)
    hashes.create_binary_seed()
    return hashes.binary_seed


def seed_test(entropy, passphrase=""):
    print("="*50)
    hashes = HashingFunctions()
    phrase = hashes.entropy_to_phrase(entropy)
    print("HashingFunctions - phrase:",phrase)
    mnemonic_info(phrase)
    
    #hashes = HashingFunctions(None, phrase)
    #binary_seed = hashes.phrase_to_key(phrase)
    binary_seed = phrase_to_key(phrase)
    # binary_seed = hashes.create_binary_seed() # x None

    print("HashingFunctions - binary_seed:",binary_seed)
    words = phrase
    mnemo_seed = mnemo_to_seed(words)
    print("mnemo_to_seed_hex:?", mnemo_seed.hex())

    mnemo = Mnemonic("english")

    # print("BIP39 Passphrase (optional): ", passphrase)
    seed_bytes = mnemo.to_seed(words, passphrase)
    #seed_bytes = mnemo.to_seed(words, passphrase="")
    # print("mnemo.to_seed = seed_bytes: ", seed_bytes)
    print("seed_bytes",seed_bytes)
    print("--- BIP39 seed:")
    print(seed_bytes.hex()) # hexadecimal_string = some_bytes.hex()
    print("--- BIP32 root key:")
    root_key = create_root_key(seed_bytes)
    print(root_key)


seed_test("00000000000000000000000000000000")
seed_test("000102030405060708090a0b0c0d0e0f")
seed_test("ffffffffffffffffffffffffffffffff")



"""
==================================================
HashingFunctions - phrase: abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about
--------------------------------------------------------------------------------
[mnemonic_info]
abandon aban...bandon about ( 12 )
0 0 0 0 0 0 0 0 0 0 0 3
validate:  (True, True)
--------------------------------------------------------------------------------
HashingFunctions - binary_seed: c55257c360c07c72029aebc1b53c05ed0362ada38ead3e3e9efa3708e53495531f09a6987599d18264c1e1c92f2cf141630c7a3c4ab7c81b2f001698e7463b04
mnemo_to_seed_hex:? a6b8f37ae15bbce7ffaf883dfae55ef847dd71816c4b510a554c95ccc291989e0a9c8e99455de874b71fee38ac262433ba15a58fe3851a2fbf14b424f3522fa3
seed_bytes b'^\xb0\x0b\xbd\xdc\xf0i\x08H\x89\xa8\xab\x91UV\x81e\xf5\xc4S\xcc\xb8^p\x81\x1a\xae\xd6\xf6\xda_\xc1\x9aZ\xc4\x0b8\x9c\xd3p\xd0\x86 m\xec\x8a\xa6\xc4=\xae\xa6i\x0f \xad=\x8dH\xb2\xd2\xce\x9e8\xe4'
--- BIP39 seed:
5eb00bbddcf069084889a8ab9155568165f5c453ccb85e70811aaed6f6da5fc19a5ac40b389cd370d086206dec8aa6c43daea6690f20ad3d8d48b2d2ce9e38e4
--- BIP32 root key:
version_BYTES:  mainnet_private
xprv9s21ZrQH143K3GJpoapnV8SFfukcVBSfeCficPSGfubmSFDxo1kuHnLisriDvSnRRuL2Qrg5ggqHKNVpxR86QEC8w35uxmGoggxtQTPvfUu

==================================================
HashingFunctions - phrase: abandon amount liar amount expire adjust cage candy arch gather drum buyer
--------------------------------------------------------------------------------
[mnemonic_info]
abandon amou...r drum buyer ( 12 )
0 64 1030 64 643 28 257 266 88 771 540 251
validate:  (True, True)
--------------------------------------------------------------------------------
HashingFunctions - binary_seed: f9bc537d3c2e74f58b7531ed7370d580114de81533720dba2a041ba9fd2d7821f0f7d55447e9f09e1e0730ee76a102073819929131a0349c502227c90699e7d0
mnemo_to_seed_hex:? 99c119f5da78b155c15720665cfbdd3ef5feaf51fdb5f61e20b5e2037923811133618a75bbefeb19df8cdc42ecbb552561964329f16adc9227aaa4a9592d64cf
seed_bytes b'7y\xb0A\xfa\xb4%\xe9\xc0\xfdU\x84k*\x03\xe9\xa3\x88\xfb\x12x@g\xbd\x8e\xbd\xb4d\xc2WJ\x05\xbc\xc7\xa8\xebT\xd7\xb2\xa2\xc8B\x0f\xf6\x0fc\x07"\xeaQ2\xd2\x86\x05\xdb\xc9\x96\xc8\xca}z\x83\x11\xc0'
--- BIP39 seed:
3779b041fab425e9c0fd55846b2a03e9a388fb12784067bd8ebdb464c2574a05bcc7a8eb54d7b2a2c8420ff60f630722ea5132d28605dbc996c8ca7d7a8311c0
--- BIP32 root key:
version_BYTES:  mainnet_private
xprv9s21ZrQH143K2XojduRLQnU8D8K59KSBoMuQKGx8dW3NBitFDMkYGiJPwZdanjZonM7eXvcEbxwuGf3RdkCyyXjsbHSkwtLnJcsZ9US42Gd

==================================================
HashingFunctions - phrase: zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo wrong
--------------------------------------------------------------------------------
[mnemonic_info]
zoo zoo zoo ...oo zoo wrong ( 12 )
2047 2047 2047 2047 2047 2047 2047 2047 2047 2047 2047 2037
validate:  (True, True)
--------------------------------------------------------------------------------
HashingFunctions - binary_seed: ac27495480225222079d7be181583751e86f571027b0497b5b5d11218e0a8a13332572917f0f8e5a589620c6f15b11c61dee327651a14c34e18231052e48c069
mnemo_to_seed_hex:? 1d89e2f0ad0032fc51ae8b1b0f445b9144355d8a4977d98269e9ddf65d9f69f0c30bd0bac902fe17f6378dde66ed7244cd2e1eb00a6745354f290ca270b2b25d
seed_bytes b"\xb6\xa6\xd8\x92\x19B\xdd\x98\x06`~\xbc'PAk(\x9a\xde\xa6i\x19\x87i\xf2\xe1^\xd9&\xc3\xaa\x92\xbf\x88\xec\xe221{N\xa4c\xe8K\x0f\xcd;SWx\x12\xeeD\x9c\xccD\x8e\xb4^oTN%\xb6"
--- BIP39 seed:
b6a6d8921942dd9806607ebc2750416b289adea669198769f2e15ed926c3aa92bf88ece232317b4ea463e84b0fcd3b53577812ee449ccc448eb45e6f544e25b6
--- BIP32 root key:
version_BYTES:  mainnet_private
xprv9s21ZrQH143K2PfMvkNViFc1fgumGqBew45JD8SxA59Jc5M66n3diqb92JjvaR61zT9P89Grys12kdtV4EFVo6tMwER7U2hcUmZ9VfMYPLC
"""
