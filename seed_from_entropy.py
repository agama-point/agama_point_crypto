#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2021-2024/06

import time
# from mnemonic import Mnemonic
from crypto_agama.trezor_mnemonic import Mnemonic
from crypto_agama.agama_btc_api import addr_info
# from crypto_agama.tools import log_to_file
from crypto_agama.agama_transform_tools import num_to_bin, bin_to_hex, hex_to_bin
from cryptos import *
from crypto_agama.agama_seed_tools import BIP39Functions, entropy_normalize, mnemo_to_seed, mnemonic_info, create_root_key, seed_words, generate_seed11_num
from crypto_agama.agama_cryptos import coin_info, wallet_info, addr3, create_wallet

scan = True
log = True
bip39f = BIP39Functions()


def phrase_to_key(phrase): 
    #tests to see if word list converts to desired master key
    _bip39f = BIP39Functions(None, phrase)
    _bip39f.create_binary_seed()
    return _bip39f.binary_seed


def seed_test(entropy, passphrase=""):
    print()
    print("="*50, len(entropy))

    entropy = entropy_normalize(entropy)
    bin_entropy = hex_to_bin(entropy)
    
    print("input entropy:", entropy)
    print("binary:", bin_entropy)

    phrase = bip39f.entropy_to_phrase(entropy)
    print("BIP39Functions - phrase:",phrase)
    print("is_valid | reverese_entropy:", bip39f.is_checksum_valid(phrase, reverse_entropy=True))
    mnemonic_info(phrase)

    binary_seed = phrase_to_key(phrase)

    print("BIP39Functions - binary_seed:",binary_seed)
    words = phrase
    mnemo_seed = mnemo_to_seed(words)
    print("mnemo_to_seed_hex:?", mnemo_seed.hex())

    mnemo = Mnemonic("english")
    # mnemo = Mnemonic()
    seed_bytes = mnemo.to_seed(words, passphrase)
    
    print("seed_bytes",seed_bytes)
    print("--- BIP39 seed:")
    print(seed_bytes.hex()) # hexadecimal_string = some_bytes.hex()
    print("--- BIP32 root key:")
    root_key = create_root_key(seed_bytes)
    print(root_key)

# ========================================================

seed_test("00000000000000000000000000000000") # 32
seed_test("000102030405060708090a0b0c0d0e0f")
seed_test("ffffffffffffffffffffffffffffffff")

bin_pattern = "01"*16  # 32 pseudo hexa
seed_test(bin_pattern)

bin_pattern = "01"*64  # 128 binary
seed_test(bin_pattern)


seed_test("00000000000000010000001000000011000001000000010100000110000001110000100000001001000010100000101100001100000011010000111000001111")
seed_test("11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")

# book
seed_test("0c1e24e5917779d297e14d45f14e1a1a")
seed_test("00001100000 11110001001 00111001011 00100010111 01110111100 11101001010 01011111100 00101001101 01000101111 10001010011 10000110100 0011010")


"""
================================================== 32
input entropy: 00000000000000000000000000000000
binary: 0
BIP39Functions - phrase: abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about
is_valid | reverese_entropy: (True, True, '00000000000000000000000000000000')
--------------------------------------------------------------------------------
[mnemonic_info]
abandon aban...bandon about ( 12 )
0 0 0 0 0 0 0 0 0 0 0 3 
validate:  (True, True)
--------------------------------------------------------------------------------
BIP39Functions - binary_seed: 7f7da6b23d82bd11fc04753a82939ef7ebc9ca1c57d800063e8fc9aa3105a1873126c2f900199f91055a1c608b8a550a905a9eb44343dd70972bf02a6e39bb58
mnemo_to_seed_hex:? a6b8f37ae15bbce7ffaf883dfae55ef847dd71816c4b510a554c95ccc291989e0a9c8e99455de874b71fee38ac262433ba15a58fe3851a2fbf14b424f3522fa3
seed_bytes b'^\xb0\x0b\xbd\xdc\xf0i\x08H\x89\xa8\xab\x91UV\x81e\xf5\xc4S\xcc\xb8^p\x81\x1a\xae\xd6\xf6\xda_\xc1\x9aZ\xc4\x0b8\x9c\xd3p\xd0\x86 m\xec\x8a\xa6\xc4=\xae\xa6i\x0f \xad=\x8dH\xb2\xd2\xce\x9e8\xe4'
--- BIP39 seed:
5eb00bbddcf069084889a8ab9155568165f5c453ccb85e70811aaed6f6da5fc19a5ac40b389cd370d086206dec8aa6c43daea6690f20ad3d8d48b2d2ce9e38e4
--- BIP32 root key:
version_BYTES:  mainnet_private
xprv9s21ZrQH143K3GJpoapnV8SFfukcVBSfeCficPSGfubmSFDxo1kuHnLisriDvSnRRuL2Qrg5ggqHKNVpxR86QEC8w35uxmGoggxtQTPvfUu

================================================== 32
input entropy: 000102030405060708090a0b0c0d0e0f
binary: 5233100606242806050955395731361295
BIP39Functions - phrase: abandon amount liar amount expire adjust cage candy arch gather drum buyer
is_valid | reverese_entropy: (True, True, '000102030405060708090a0b0c0d0e0f')
--------------------------------------------------------------------------------
[mnemonic_info]
abandon amou...r drum buyer ( 12 )
0 64 1030 64 643 28 257 266 88 771 540 251 
validate:  (True, True)
--------------------------------------------------------------------------------
BIP39Functions - binary_seed: cffc2c0c98bbef4aceda31cb4cc1a2faf6435fab82bcc6e6080f0eb30ba71b78a982b8f8d4b2051c55dfe799598acc06746fe7da20b0239c5a073d9a3fbb33e6
mnemo_to_seed_hex:? 99c119f5da78b155c15720665cfbdd3ef5feaf51fdb5f61e20b5e2037923811133618a75bbefeb19df8cdc42ecbb552561964329f16adc9227aaa4a9592d64cf
seed_bytes b'7y\xb0A\xfa\xb4%\xe9\xc0\xfdU\x84k*\x03\xe9\xa3\x88\xfb\x12x@g\xbd\x8e\xbd\xb4d\xc2WJ\x05\xbc\xc7\xa8\xebT\xd7\xb2\xa2\xc8B\x0f\xf6\x0fc\x07"\xeaQ2\xd2\x86\x05\xdb\xc9\x96\xc8\xca}z\x83\x11\xc0'
--- BIP39 seed:
3779b041fab425e9c0fd55846b2a03e9a388fb12784067bd8ebdb464c2574a05bcc7a8eb54d7b2a2c8420ff60f630722ea5132d28605dbc996c8ca7d7a8311c0
--- BIP32 root key:
version_BYTES:  mainnet_private
xprv9s21ZrQH143K2XojduRLQnU8D8K59KSBoMuQKGx8dW3NBitFDMkYGiJPwZdanjZonM7eXvcEbxwuGf3RdkCyyXjsbHSkwtLnJcsZ9US42Gd

================================================== 32
input entropy: ffffffffffffffffffffffffffffffff
binary: 340282366920938463463374607431768211455
BIP39Functions - phrase: zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo wrong
is_valid | reverese_entropy: (True, True, 'ffffffffffffffffffffffffffffffff')
--------------------------------------------------------------------------------
[mnemonic_info]
zoo zoo zoo ...oo zoo wrong ( 12 )
2047 2047 2047 2047 2047 2047 2047 2047 2047 2047 2047 2037 
validate:  (True, True)
--------------------------------------------------------------------------------
BIP39Functions - binary_seed: 16ef1651d73d8f6ca2d1eaec4b9481d62d47c58e839d70605232a26b6e90c4d7d672d0f8057f8f269190d9dcaa15655ca9a1a3d44d6668852ee2ef6c758efade
mnemo_to_seed_hex:? 1d89e2f0ad0032fc51ae8b1b0f445b9144355d8a4977d98269e9ddf65d9f69f0c30bd0bac902fe17f6378dde66ed7244cd2e1eb00a6745354f290ca270b2b25d
seed_bytes b"\xb6\xa6\xd8\x92\x19B\xdd\x98\x06`~\xbc'PAk(\x9a\xde\xa6i\x19\x87i\xf2\xe1^\xd9&\xc3\xaa\x92\xbf\x88\xec\xe221{N\xa4c\xe8K\x0f\xcd;SWx\x12\xeeD\x9c\xccD\x8e\xb4^oTN%\xb6"
--- BIP39 seed:
b6a6d8921942dd9806607ebc2750416b289adea669198769f2e15ed926c3aa92bf88ece232317b4ea463e84b0fcd3b53577812ee449ccc448eb45e6f544e25b6
--- BIP32 root key:
version_BYTES:  mainnet_private
xprv9s21ZrQH143K2PfMvkNViFc1fgumGqBew45JD8SxA59Jc5M66n3diqb92JjvaR61zT9P89Grys12kdtV4EFVo6tMwER7U2hcUmZ9VfMYPLC

================================================== 32
input entropy: 01010101010101010101010101010101
binary: 1334440654591915542993625911497130241
BIP39Functions - phrase: absurd amount doctor acoustic avoid letter advice cage absurd amount doctor adjust
is_valid | reverese_entropy: (True, True, '01010101010101010101010101010101')
--------------------------------------------------------------------------------
[mnemonic_info]
absurd amoun...octor adjust ( 12 )
8 64 514 16 128 1028 32 257 8 64 514 28 
validate:  (True, True)
--------------------------------------------------------------------------------
BIP39Functions - binary_seed: ef120cdfbfbc3dbcbba67f362a59408fdfd6dfb71df2f2d4adbe4a9cc29d616ef9597ad317b2f0405e199a175900c5c016c075bb853ad1f03b12eedeebb111b3
mnemo_to_seed_hex:? 91d476abe4fbedcbad8ef572393c71f25ae22616f1a1c834456572c87151a6ab0736718dbe552b3b91a3b2ff6e22b6f6e27ffce41d53a07a41bcde6ffaff7c85
seed_bytes b'\x02Y-B<N|m\x18\x94w\x13\xb4\x7fyW\xc9\xf1\xdd\xd0\xa1\x96\xd6I\xd7w\xcd\x91F\x9c\x0f\xb3\x04\x9c)V|m\x03\xdf\x9e2\xb2\xc6\xa4F\xbe\t\x8e\x1ek\x84Ve\xed\xb8\x10\xd4\xdb\xd0\xdf\x03\xab\x96'
--- BIP39 seed:
02592d423c4e7c6d18947713b47f7957c9f1ddd0a196d649d777cd91469c0fb3049c29567c6d03df9e32b2c6a446be098e1e6b845665edb810d4dbd0df03ab96
--- BIP32 root key:
version_BYTES:  mainnet_private
xprv9s21ZrQH143K3Rg822CndWLHVYVjW3QMbRtkzervRBSGNPvz8d3u2eBpS6an8yQsCLHGhZhmrnC5L6gwDkkuTtMXRX6zZdcSRExLxSxZMEh

================================================== 128
input entropy: 55555555555555555555555555555555
binary: 113427455640312821154458202477256070485
BIP39Functions - phrase: fetch primary fetch primary fetch primary fetch primary fetch primary fetch problem
is_valid | reverese_entropy: (True, True, '55555555555555555555555555555555')
--------------------------------------------------------------------------------
[mnemonic_info]
fetch primar...etch problem ( 12 )
682 1365 682 1365 682 1365 682 1365 682 1365 682 1371 
validate:  (True, True)
--------------------------------------------------------------------------------
BIP39Functions - binary_seed: 1eb9a4a43269f3024e4f94330fe28502ffcc85780c680b6a4b1165e2fefc75eed3ae854fe760fbdf226bedb99d0055e45d00f97ab262653834ccf7706d2d20e7
mnemo_to_seed_hex:? 006f1556b2585e31b0cbb1e8939d5dcb7b260e94709bec82f83bcbe8df048af7c90c3a7613c360dd96b6fda00c2aa3f04fd7d092d05563dd43fd198ea6770100
seed_bytes b'\xaa[G\xca\xa9;\xe5\xf0\xcbj\xf2\x94u\x85=\\<\x85\xd6\x0f\x0c\x8a\xb8\x87\xdbx\xa3\xd6T<\x92\xc6\xe7JfY\xcb?\xf4J|\x8d\x02J\x04\x999b<@Z;\xbd\xb6\x98\x80\x92\x19\xfd\xc7\xc8\xa5* '
--- BIP39 seed:
aa5b47caa93be5f0cb6af29475853d5c3c85d60f0c8ab887db78a3d6543c92c6e74a6659cb3ff44a7c8d024a049939623c405a3bbdb698809219fdc7c8a52a20
--- BIP32 root key:
version_BYTES:  mainnet_private
xprv9s21ZrQH143K2RcvhRnxEyR9biHrBRfd6fidChZyWAKgSZ26gcxiGRrvGARzuu4LaYtU5w8x2rGe8Gad1Ud6E4ZqAy2YFzYVtkBqvaVViRj

================================================== 128
input entropy: 000102030405060708090a0b0c0d0e0f
binary: 5233100606242806050955395731361295
BIP39Functions - phrase: abandon amount liar amount expire adjust cage candy arch gather drum buyer
is_valid | reverese_entropy: (True, True, '000102030405060708090a0b0c0d0e0f')
--------------------------------------------------------------------------------
[mnemonic_info]
abandon amou...r drum buyer ( 12 )
0 64 1030 64 643 28 257 266 88 771 540 251 
validate:  (True, True)
--------------------------------------------------------------------------------
BIP39Functions - binary_seed: cffc2c0c98bbef4aceda31cb4cc1a2faf6435fab82bcc6e6080f0eb30ba71b78a982b8f8d4b2051c55dfe799598acc06746fe7da20b0239c5a073d9a3fbb33e6
mnemo_to_seed_hex:? 99c119f5da78b155c15720665cfbdd3ef5feaf51fdb5f61e20b5e2037923811133618a75bbefeb19df8cdc42ecbb552561964329f16adc9227aaa4a9592d64cf
seed_bytes b'7y\xb0A\xfa\xb4%\xe9\xc0\xfdU\x84k*\x03\xe9\xa3\x88\xfb\x12x@g\xbd\x8e\xbd\xb4d\xc2WJ\x05\xbc\xc7\xa8\xebT\xd7\xb2\xa2\xc8B\x0f\xf6\x0fc\x07"\xeaQ2\xd2\x86\x05\xdb\xc9\x96\xc8\xca}z\x83\x11\xc0'
--- BIP39 seed:
3779b041fab425e9c0fd55846b2a03e9a388fb12784067bd8ebdb464c2574a05bcc7a8eb54d7b2a2c8420ff60f630722ea5132d28605dbc996c8ca7d7a8311c0
--- BIP32 root key:
version_BYTES:  mainnet_private
xprv9s21ZrQH143K2XojduRLQnU8D8K59KSBoMuQKGx8dW3NBitFDMkYGiJPwZdanjZonM7eXvcEbxwuGf3RdkCyyXjsbHSkwtLnJcsZ9US42Gd

================================================== 128
input entropy: ffffffffffffffffffffffffffffffff
binary: 340282366920938463463374607431768211455
BIP39Functions - phrase: zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo wrong
is_valid | reverese_entropy: (True, True, 'ffffffffffffffffffffffffffffffff')
--------------------------------------------------------------------------------
[mnemonic_info]
zoo zoo zoo ...oo zoo wrong ( 12 )
2047 2047 2047 2047 2047 2047 2047 2047 2047 2047 2047 2037 
validate:  (True, True)
--------------------------------------------------------------------------------
BIP39Functions - binary_seed: 16ef1651d73d8f6ca2d1eaec4b9481d62d47c58e839d70605232a26b6e90c4d7d672d0f8057f8f269190d9dcaa15655ca9a1a3d44d6668852ee2ef6c758efade
mnemo_to_seed_hex:? 1d89e2f0ad0032fc51ae8b1b0f445b9144355d8a4977d98269e9ddf65d9f69f0c30bd0bac902fe17f6378dde66ed7244cd2e1eb00a6745354f290ca270b2b25d
seed_bytes b"\xb6\xa6\xd8\x92\x19B\xdd\x98\x06`~\xbc'PAk(\x9a\xde\xa6i\x19\x87i\xf2\xe1^\xd9&\xc3\xaa\x92\xbf\x88\xec\xe221{N\xa4c\xe8K\x0f\xcd;SWx\x12\xeeD\x9c\xccD\x8e\xb4^oTN%\xb6"
--- BIP39 seed:
b6a6d8921942dd9806607ebc2750416b289adea669198769f2e15ed926c3aa92bf88ece232317b4ea463e84b0fcd3b53577812ee449ccc448eb45e6f544e25b6
--- BIP32 root key:
version_BYTES:  mainnet_private
xprv9s21ZrQH143K2PfMvkNViFc1fgumGqBew45JD8SxA59Jc5M66n3diqb92JjvaR61zT9P89Grys12kdtV4EFVo6tMwER7U2hcUmZ9VfMYPLC

================================================== 32
input entropy: 0c1e24e5917779d297e14d45f14e1a1a
binary: 16107253210189746418104142711095171610
BIP39Functions - phrase: army van defense carry jealous true garbage claim echo media make crunch
is_valid | reverese_entropy: (True, True, '0c1e24e5917779d297e14d45f14e1a1a')
--------------------------------------------------------------------------------
[mnemonic_info]
army van def... make crunch ( 12 )
96 1929 459 279 956 1866 764 333 559 1107 1076 423 
validate:  (True, True)
--------------------------------------------------------------------------------
BIP39Functions - binary_seed: 7279fdb6da02e133273d793461f23534497834c88d9df1fff2a5761edc4564065082c6a0e2fc2c934ea9614a5f49df916df5b21f1dd5ccbe1be697a86b6dc89d
mnemo_to_seed_hex:? 4f2c76795aafb17902d7a3d8ff6db6c4158415e4ad996dec1b9d201f4285590ac0fa32ff057720e1a1dd087d6031e5cd37d67720da929869bf76118bb7215a3d
seed_bytes b'[V\xc4\x170?\xaa?\xcb\xa7\xe5t\x00\xe1 \xa0\xca\x83\xecZO\xc9\xff\xbau\x7f\xbec\xfb\xd7z\x89\xa1\xa3\xbeLg\x19oW\xc3\x9a\x88\xb7css8\x91\xbf\xab\xa1n\xd2z\x81<\xee\xd4\x98\x80L\x05p'
--- BIP39 seed:
5b56c417303faa3fcba7e57400e120a0ca83ec5a4fc9ffba757fbe63fbd77a89a1a3be4c67196f57c39a88b76373733891bfaba16ed27a813ceed498804c0570
--- BIP32 root key:
version_BYTES:  mainnet_private
xprv9s21ZrQH143K3t4UZrNgeA3w861fwjYLaGwmPtQyPMmzshV2owVpfBSd2Q7YsHZ9j6i6ddYjb5PLtUdMZn8LhvuCVhGcQntq5rn7JVMqnie

================================================== 139
input entropy: 0c1e24e5917779d297e14d45f14e1a1a
binary: 16107253210189746418104142711095171610
BIP39Functions - phrase: army van defense carry jealous true garbage claim echo media make crunch
is_valid | reverese_entropy: (True, True, '0c1e24e5917779d297e14d45f14e1a1a')
--------------------------------------------------------------------------------
[mnemonic_info]
army van def... make crunch ( 12 )
96 1929 459 279 956 1866 764 333 559 1107 1076 423 
validate:  (True, True)
--------------------------------------------------------------------------------
BIP39Functions - binary_seed: 7279fdb6da02e133273d793461f23534497834c88d9df1fff2a5761edc4564065082c6a0e2fc2c934ea9614a5f49df916df5b21f1dd5ccbe1be697a86b6dc89d
mnemo_to_seed_hex:? 4f2c76795aafb17902d7a3d8ff6db6c4158415e4ad996dec1b9d201f4285590ac0fa32ff057720e1a1dd087d6031e5cd37d67720da929869bf76118bb7215a3d
seed_bytes b'[V\xc4\x170?\xaa?\xcb\xa7\xe5t\x00\xe1 \xa0\xca\x83\xecZO\xc9\xff\xbau\x7f\xbec\xfb\xd7z\x89\xa1\xa3\xbeLg\x19oW\xc3\x9a\x88\xb7css8\x91\xbf\xab\xa1n\xd2z\x81<\xee\xd4\x98\x80L\x05p'
--- BIP39 seed:
5b56c417303faa3fcba7e57400e120a0ca83ec5a4fc9ffba757fbe63fbd77a89a1a3be4c67196f57c39a88b76373733891bfaba16ed27a813ceed498804c0570
--- BIP32 root key:
version_BYTES:  mainnet_private
xprv9s21ZrQH143K3t4UZrNgeA3w861fwjYLaGwmPtQyPMmzshV2owVpfBSd2Q7YsHZ9j6i6ddYjb5PLtUdMZn8LhvuCVhGcQntq5rn7JVMqnie
"""