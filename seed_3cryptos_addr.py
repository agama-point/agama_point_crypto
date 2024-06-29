"""
basic   https://github.com/bitcoinbook/bitcoinbook
prg_src https://github.com/primal100/pybitcointools
verif.  https://iancoleman.io/bip39/
"""

from cryptos import *
from crypto_agama.agama_seed_tools import seed_words, mnemonic_info, words_to_4ch
from priv_data import words_book #, get_seeds, get_words
from crypto_agama.agama_cryptos import coin_info, wallet_info
## = OBJ / ToDo


def addr3(c,w):
    wallet_info(c,w)
    print("[ - add3 - ]")
    addr0 = wallet.new_receiving_address()
    print("0",addr0)
    #addr1 = wallet.new_change_address()
    addr1 = wallet.new_receiving_address()
    print("1",addr1)
    addr2 = wallet.new_receiving_address()
    print("2",addr2)
    # print("last_change_index: ",wallet.last_change_index)

# words = entropy_to_words(os.urandom(16))
words = words_book ### get_words()
words = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
### print(words)
mnemonic_info(words)
# mnemo_seed = mnemo_to_seed(words)

print(keystore.bip39_is_checksum_valid(words))

coin = Bitcoin() # Main default
# coin = Bitcoin(testnet=True)
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
abandon aban...bandon about ( 12 )
0 0 0 0 0 0 0 0 0 0 0 3
validate:  (True, True)
(True, True)
[ - coin_info - ]
coin_symbol: BTC
is_testnet:  False

 ================================
BIP39-BIP44 | Standard Wallets:
[ - wallet_info - ]
m/44'/0'/0'
xprv:  xprv9xpXFhFpqdQK3TmytPBqXtGSwS3DLjojFhTGht8gwAAii8py5X6pxeBnQ6ehJiyJ6nDjWGJfZ95WxByFXVkDxHXrqu53WCRGypk2ttuqncb
xpub: xpub6BosfCnifzxcFwrSzQiqu2DBVTshkCXacvNsWGYJVVhhawA7d4R5WSWGFNbi8Aw6ZRc1brxMyWMzG3DSSSSoekkudhUd9yLb6qx39T9nMdj
----------------
[ - add3 - ]
0 1LqBGSKuX5yYUonjxT5qGfpUsXKYYWeabA
1 1Ak8PffB2meyfYnbXZR9EGfLfFZVpzJvQP
2 1MNF5RSaabFwcbtJirJwKnDytsXXEsVsNb

 ================================
BIP39-BIP49 | Segwit Wallets:
[ - wallet_info - ]
m/49'/0'/0'
xprv:  yprvAHwhK6RbpuS3dgCYHM5jc2ZvEKd7Bi61u9FVhYMpgMSuZS613T1xxQeKTffhrHY79hZ5PsskBjcc6C2V7DrnsMsNaGDaWev3GLRQRgV7hxF
xpub: ypub6Ww3ibxVfGzLrAH1PNcjyAWenMTbbAosGNB6VvmSEgytSER9azLDWCxoJwW7Ke7icmizBMXrzBx9979FfaHxHcrArf3zbeJJJUZPf663zsP
----------------
[ - add3 - ]
0 37VucYSaXLCAsxYyAPfbSi9eh4iEcbShgf
1 3LtMnn87fqUeHBUG414p9CWwnoV6E2pNKS
2 3B4cvWGR8X6Xs8nvTxVUoMJV77E4f7oaia

 ================================
BIP39-BIP84 | New Segwit Wallets:
[ - wallet_info - ]
m/84'/0'/0'
xprv:  zprvAdG4iTXWBoARxkkzNpNh8r6Qag3irQB8PzEMkAFeTRXxHpbF9z4QgEvBRmfvqWvGp42t42nvgGpNgYSJA9iefm1yYNZKEm7z6qUWCroSQnE
xpub: zpub6rFR7y4Q2AijBEqTUquhVz398htDFrtymD9xYYfG1m4wAcvPhXNfE3EfH1r1ADqtfSdVCToUG868RvUUkgDKf31mGDtKsAYz2oz2AGutZYs
----------------
[ - add3 - ]
0 bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu
1 bc1qnjg0jd8228aq7egyzacy8cys3knf9xvrerkf9g
2 bc1qp59yckz4ae5c4efgw2s5wfyvrz0ala7rgvuz8z

"""

