from crypto_agama.seed_tools import seed_words, mnemonic_info
from crypto_agama.agama_seed_tools import BIP39Functions
from priv_data import words_book, words_trezor


bip39f = BIP39Functions()

def test_mnemonic(w):
    print("="*50)
    mnemonic_info(w)

    binf = bip39f.words_to_entropy(w)
    print(bip39f.entropy_bin, " :: ", bip39f.check_sum)
    e = bip39f.entropy_hex # == binf
    print(e)
    print(bip39f.entropy_to_phrase(e))
    print()

# =========================================
# w = "army van defense carry jealous true garbage claim echo media make crunch" # words_andreas
w = words_book
test_mnemonic(w)


w = words_trezor
test_mnemonic(w)

"""
==================================================
army van def... make crunch ( 12 )
96 1929 459 279 956 1866 764 333 559 1107 1076 423
validate:  (True, True)
00001100000111100010010011100101100100010111011101111001110100101001011111100001010011010100010111110001010011100001101000011010  ::  0111
0c1e24e5917779d297e14d45f14e1a1a
army van defense carry jealous ... echo media make crunch

==================================================
inside label...net surprise ( 12 )
937 993 518 1366 470 2046 555 704 1565 900 1189 1747
validate:  (True, True)
01110101001011111000010100000011010101010110001110101101111111111001000101011010110000001100001110101110000100100101001011101101  ::  0011
752f85035563adff915ac0c3ae1252ed
inside label dolphin ... earth fix senior identify net surprise
"""




