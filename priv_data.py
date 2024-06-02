# bip39 vectors: https://github.com/trezor/python-mnemonic/blob/master/vectors.json
w_000000 = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
w_111111 = "zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo wrong" # "11111" last chsm: wrong winter ...
w_808080 = "letter advice cage absurd amount doctor acoustic avoid letter advice cage above"

# https://iancoleman.io/bip39/
words_book = "army van defense carry jealous true garbage claim echo media make crunch"
entro_book = "0c1e24e5917779d297e14d45f14e1a1a"
andreas_cz = "bouda vzpoura hrdina doufat nejprve vrhat limetka facka kapela operace ofsajd hoboj"

words_trezor = "inside label dolphin print depart zone earth fix senior identify net surprise"
entro_trezor = "752f85035563adff915ac0c3ae1252ed"
trezor_cz = "nasadit nutit jelen puberta hryzat zvukovod kanibal kultura smysl muzikant penalta ujednat"

words_tbtc = "major easy ignore body rule stay gorilla eager arch actor scan thank" # www

words_cryptos12 = "practice display use aisle armor salon glue okay sphere rather belt mansion"
words_cryptos15 = "jealous silver churn hedgehog border physical market parent hungry design cage lab drill clay attack"

words_test = "..."


seeds = (words_book, words_tbtc)

def get_words(): return words_tbtc
def get_seeds(): return seeds # words_tbtc

"""
from priv_data import words_book
words = words_book
...
"""
