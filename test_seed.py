#!/usr/bin/env python3
# 2021-02 / 2023-05

from crypto_agama.seed_tools import seed_words, mnemonic_info, words_to_4ch
from crypto_agama.agama_cryptos import create_wallet
from crypto_agama.btc_api import addr_info
from crypto_agama.tools import log_to_file, get_env_key


bip39 = seed_words()

print("--- test_seed_tools.py ---")
words_andreas = "army van defense carry jealous true garbage claim echo media make crunch"

mnemonic_info(words_andreas)
print(words_to_4ch(words_andreas))
