# 2021-02-01

from priv_data import get_seeds, get_words # words

from crypto_agama.agama_seed_tools import seed_words, mnemonic_info, words_to_4ch
from crypto_agama.agama_cryptos import create_wallet
from crypto_agama.agama_btc_api import addr_info
from crypto_agama.tools import log_to_file

bip39 = seed_words()
seeds = get_seeds()

print("--- test_seed_tools.py ---")

for words in seeds:
    mnemonic_info(words)
    print("-"*50)

print(words_to_4ch(words))
