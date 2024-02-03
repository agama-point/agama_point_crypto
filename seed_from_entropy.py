#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2021-02-01

import time
from mnemonic import Mnemonic
from crypto_agama.btc_api import addr_info
# from crypto_agama.tools import log_to_file
from crypto_agama.agama_transform_tools import num_to_bin, bin_to_hex, hex_to_bin
from cryptos import *
from crypto_agama.agama_seed_tools import BIP39Functions, mnemo_to_seed, mnemonic_info, create_root_key, seed_words, generate_seed11_num
from crypto_agama.agama_cryptos import coin_info, wallet_info, addr3, create_wallet
# from crypto_agama.seed_tools import seed_words, mnemonic_info, words_to_4ch

scan = True
log = True
# entropy: hexa / binary


def phrase_to_key(phrase): 
    #tests to see if word list converts to desired master key
    hashes = BIP39Functions(None, phrase)
    hashes.create_binary_seed()
    return hashes.binary_seed


def seed_test(entropy, passphrase=""):
    print()
    print("="*50, len(entropy))
    if len(entropy) < 39: # -> hexa
        print("[ hex input ]")
        bin_entropy = hex_to_bin(entropy)
    if len(entropy) > 127: # -> bin
        print("[ bin input ]")
        bin_entropy = entropy.replace(" ", "")
        entropy = bin_to_hex(bin_entropy)
        
        existing_hex_str = str(entropy)[2:]  # Odstranění "0x"
        desired_length = 32

        if len(existing_hex_str) < desired_length:
            print("...normalize")
            padding_length = desired_length - len(existing_hex_str)
            print("padding_length",padding_length)
            existing_hex_str = '0' * padding_length + existing_hex_str

        entropy = existing_hex_str # without 0x

    print("input entropy:", entropy)
    print("binary:", bin_entropy)

    hashes = BIP39Functions()
    phrase = hashes.entropy_to_phrase(entropy)
    print("HashingFunctions - phrase:",phrase)
    print("is_valid | reverese_entropy:", hashes.is_checksum_valid(phrase, reverse_entropy=True))
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


seed_test("00000000000000000000000000000000") # 32
seed_test("000102030405060708090a0b0c0d0e0f")
seed_test("ffffffffffffffffffffffffffffffff")


seed_test("00000000000000010000001000000011000001000000010100000110000001110000100000001001000010100000101100001100000011010000111000001111")
seed_test("11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")

# book
seed_test("0c1e24e5917779d297e14d45f14e1a1a")
seed_test("00001100000 11110001001 00111001011 00100010111 01110111100 11101001010 01011111100 00101001101 01000101111 10001010011 10000110100 0011010")


"""
================================================== 32
[ hex input ]
input entropy: 00000000000000000000000000000000
binary: 0b0
HashingFunctions - phrase: abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about
is_valid | reverese_entropy: (True, True, '00000000000000000000000000000000')
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

================================================== 32
[ hex input ]
input entropy: 000102030405060708090a0b0c0d0e0f
binary: 0b10000001000000011000001000000010100000110000001110000100000001001000010100000101100001100000011010000111000001111
HashingFunctions - phrase: abandon amount liar amount expire adjust cage candy arch gather drum buyer
is_valid | reverese_entropy: (True, True, '000102030405060708090a0b0c0d0e0f')
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

================================================== 32
[ hex input ]
input entropy: ffffffffffffffffffffffffffffffff
binary: 0b11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111  
HashingFunctions - phrase: zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo wrong
is_valid | reverese_entropy: (True, True, 'ffffffffffffffffffffffffffffffff')
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

================================================== 128
[ bin input ]
...normalize
padding_length 3
input entropy: 000102030405060708090a0b0c0d0e0f
binary: 00000000000000010000001000000011000001000000010100000110000001110000100000001001000010100000101100001100000011010000111000001111    
HashingFunctions - phrase: abandon amount liar amount expire adjust cage candy arch gather drum buyer
is_valid | reverese_entropy: (True, True, '000102030405060708090a0b0c0d0e0f')
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

================================================== 128
[ bin input ]
input entropy: ffffffffffffffffffffffffffffffff
binary: 11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111    
HashingFunctions - phrase: zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo wrong
is_valid | reverese_entropy: (True, True, 'ffffffffffffffffffffffffffffffff')
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

================================================== 32
[ hex input ]
input entropy: 0c1e24e5917779d297e14d45f14e1a1a
binary: 0b1100000111100010010011100101100100010111011101111001110100101001011111100001010011010100010111110001010011100001101000011010      
HashingFunctions - phrase: army van defense carry jealous true garbage claim echo media make crunch
is_valid | reverese_entropy: (True, True, '0c1e24e5917779d297e14d45f14e1a1a')
--------------------------------------------------------------------------------
[mnemonic_info]
army van def... make crunch ( 12 )
96 1929 459 279 956 1866 764 333 559 1107 1076 423
validate:  (True, True)
--------------------------------------------------------------------------------
HashingFunctions - binary_seed: 3338a6d2ee71c7f28eb5b882159634cd46a898463e9d2d0980f8e80dfbba5b0fa0291e5fb888a599b44b93187be6ee3ab5fd3ead7dd646341b2cdb8d08d13bf7
mnemo_to_seed_hex:? 4f2c76795aafb17902d7a3d8ff6db6c4158415e4ad996dec1b9d201f4285590ac0fa32ff057720e1a1dd087d6031e5cd37d67720da929869bf76118bb7215a3d
seed_bytes b'[V\xc4\x170?\xaa?\xcb\xa7\xe5t\x00\xe1 \xa0\xca\x83\xecZO\xc9\xff\xbau\x7f\xbec\xfb\xd7z\x89\xa1\xa3\xbeLg\x19oW\xc3\x9a\x88\xb7css8\x91\xbf\xab\xa1n\xd2z\x81<\xee\xd4\x98\x80L\x05p'
--- BIP39 seed:
5b56c417303faa3fcba7e57400e120a0ca83ec5a4fc9ffba757fbe63fbd77a89a1a3be4c67196f57c39a88b76373733891bfaba16ed27a813ceed498804c0570
--- BIP32 root key:
version_BYTES:  mainnet_private
xprv9s21ZrQH143K3t4UZrNgeA3w861fwjYLaGwmPtQyPMmzshV2owVpfBSd2Q7YsHZ9j6i6ddYjb5PLtUdMZn8LhvuCVhGcQntq5rn7JVMqnie

================================================== 139
[ bin input ]
...normalize
padding_length 1
input entropy: 0c1e24e5917779d297e14d45f14e1a1a
binary: 00001100000111100010010011100101100100010111011101111001110100101001011111100001010011010100010111110001010011100001101000011010    
HashingFunctions - phrase: army van defense carry jealous true garbage claim echo media make crunch
is_valid | reverese_entropy: (True, True, '0c1e24e5917779d297e14d45f14e1a1a')
--------------------------------------------------------------------------------
[mnemonic_info]
army van def... make crunch ( 12 )
96 1929 459 279 956 1866 764 333 559 1107 1076 423
validate:  (True, True)
--------------------------------------------------------------------------------
HashingFunctions - binary_seed: 3338a6d2ee71c7f28eb5b882159634cd46a898463e9d2d0980f8e80dfbba5b0fa0291e5fb888a599b44b93187be6ee3ab5fd3ead7dd646341b2cdb8d08d13bf7
mnemo_to_seed_hex:? 4f2c76795aafb17902d7a3d8ff6db6c4158415e4ad996dec1b9d201f4285590ac0fa32ff057720e1a1dd087d6031e5cd37d67720da929869bf76118bb7215a3d
seed_bytes b'[V\xc4\x170?\xaa?\xcb\xa7\xe5t\x00\xe1 \xa0\xca\x83\xecZO\xc9\xff\xbau\x7f\xbec\xfb\xd7z\x89\xa1\xa3\xbeLg\x19oW\xc3\x9a\x88\xb7css8\x91\xbf\xab\xa1n\xd2z\x81<\xee\xd4\x98\x80L\x05p'
--- BIP39 seed:
5b56c417303faa3fcba7e57400e120a0ca83ec5a4fc9ffba757fbe63fbd77a89a1a3be4c67196f57c39a88b76373733891bfaba16ed27a813ceed498804c0570
--- BIP32 root key:
version_BYTES:  mainnet_private
xprv9s21ZrQH143K3t4UZrNgeA3w861fwjYLaGwmPtQyPMmzshV2owVpfBSd2Q7YsHZ9j6i6ddYjb5PLtUdMZn8LhvuCVhGcQntq5rn7JVMqnie



"""