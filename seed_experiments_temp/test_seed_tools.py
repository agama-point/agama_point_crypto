# 2021-02-01
from crypto_agama.tools import log_to_file
from priv_data import get_seeds, get_words # words
from crypto_agama.seed_tools import seed_words, mnemonic_info, words_to_4ch
from crypto_agama.agama_cryptos import create_wallet
from crypto_agama.btc_api import addr_info
from crypto_agama.cipher import fleissner_decrypt

bip39 = seed_words()
seeds = get_seeds()

# =================================================
words = get_words()
# words = " "

mnemonic_info(words)

w12_4c13 = words_to_4ch(words,separator="")
print("w12_4c13 ", w12_4c13, len(w12_4c13))
print("="*50)
print(words[:12]+" ...")

if len(w12_4c13)<48:
    w12_4c13 = w12_4c13 + "XYZ"
print()

