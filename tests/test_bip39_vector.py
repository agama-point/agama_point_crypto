import requests, json 
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crypto_agama.agama_seed_tools import BIP39Functions


bip39f = BIP39Functions()

# url = "https://github.com/trezor/python-mnemonic/blob/master/vectors.json"
url = "https://raw.githubusercontent.com/trezor/python-mnemonic/master/vectors.json"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    for item in data['english']:
        hex_value = item[0]
        mnemonic = item[1]
        seed = item[2]
        xprv = item[3]
        
        print(f"Hex: {hex_value}")
        print(f"Mnemonic: {mnemonic}")
        phrase = bip39f.entropy_to_phrase(hex_value)
        print(f"Mnemonic? {phrase}")

        print(f"Seed: {seed}")
        bip39f.create_binary_seed()
        print(f"Seed? {bip39f.binary_seed}") # x ???

        print(f"xPrv: {xprv}")
        print("---------")
else:
    print(f"Chyba při načítání souboru: {response.status_code}")

"""
...
---------
Hex: 80808080808080808080808080808080
Mnemonic: letter advice cage absurd amount doctor acoustic avoid letter advice cage above
Mnemonic? letter advice cage absurd amount doctor acoustic avoid letter advice cage above
Seed: d71de856f81a8acc65e6fc851a38d4d7ec216fd0796d0a6827a3ad6ed5511a30fa280f12eb2e47ed2ac03b5c462a0358d18d69fe4f985ec81778c1b370b652a8
xPrv: xprv9s21ZrQH143K2shfP28KM3nr5Ap1SXjz8gc2rAqqMEynmjt6o1qboCDpxckqXavCwdnYds6yBHZGKHv7ef2eTXy461PXUjBFQg6PrwY4Gzq
---------
...
"""


