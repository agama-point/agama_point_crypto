"""
basic   https://github.com/bitcoinbook/bitcoinbook
prg_src https://github.com/primal100/pybitcointools
verif.  https://iancoleman.io/bip39/
"""

from cryptos import *
from crypto_agama.seed_tools import seed_words, mnemonic_info, words_to_4ch
from priv_data import words_book #, get_seeds, get_words

## = OBJ / ToDo

def coin_info(b):
    print("[ - coin_info - ]")
    print("coin_symbol:",b.coin_symbol)
    print("is_testnet: ",b.is_testnet)
    ## print("is_segwit:  ",b.is_segwit)
    ## print(b.current_block_height)


def wallet_info(c,w):
    print("[ - wallet_info - ]")
    print(w.keystore.root_derivation)
    #? print("address_prefixes: ",c.address_prefixes)
    print("xprv: ",w.keystore.xprv)
    print("xpub:",w.keystore.xpub)
    ## print("coin:",w.coin)
    ## print("details:",w.details)
    ## print("balance:",w.balance)
    ## print("pubkey_receiving",w.pubkey_receiving)

    print("-"*16)


def addr3(c,w):
    wallet_info(c,w)
    print("[ - add3 - ]")
    addr0 = wallet.new_receiving_address()
    print("0",addr0)
    addr1 = wallet.new_change_address()
    print("1",addr1)
    addr2 = wallet.new_change_address()
    print("2",addr2)
    print("last_change_index: ",wallet.last_change_index)

# words = entropy_to_words(os.urandom(16))
words = words_book ### get_words()

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
army van def... make crunch ( 12 )
96 1929 459 279 956 1866 764 333 559 1107 1076 423 
validate:  (True, True)
(True, True)
[ - coin_info - ]
coin_symbol: BTC
is_testnet:  False

 ================================
BIP39-BIP44 | Standard Wallets:
[ - wallet_info - ]
m/44'/0'/0'
xprv:  xprv9yymDxtAiwgiooASPoaeTHjhKmhAvZdTeCJXCp3KFg2zaB7ezjDVXbA4JgKqhsdtzYGuFeorgfc26kTCGY6of1PYNH9oQqYmvpS8V1oZjzc
xpub: xpub6Cy7dUR4ZKF22HEuVq7epRgRsoXfL2MK1RE81CSvp1ZySySoYGXk5PUY9y9Cc5ExpnSwXyimQAsVhyyPDNDrfj4xjDsKZJNYgsHXoEPNCYQ
----------------
[ - add3 - ]
0 1HQ3rb7nyLPrjnuW85MUknPekwkn7poAUm
1 12Co6qiQ7zrehMz4PugN5tYMNZ7UozUjSv
2 16gLEe3z2BULAEhieF5zESeW7VzhSocDF4
last_change_index:  2

 ================================
BIP39-BIP49 | Segwit Wallets:
[ - wallet_info - ]
m/49'/0'/0'
xprv:  yprvAJ4QaLC8GW7fjEBLksUpbYbmCsUfSDYiEjteuZepv3ZwDHGy5cf8VaGC4iREzgEBjP1f1YWGaxzBsqp47LtDYgBDqnSujQNaLd3d1jvVMzW
xpub: ypub6X3kyqj26sfxwiForu1pxgYVkuK9qgGZbxpFhx4SUP6v65c7d9yP3Nafv1SrMF3uhyu4hzHPptQj8NajcT6YVSUfZ6mNDe2Kqyg7nvNj9Ye
----------------
[ - add3 - ]
0 3FEQ7b7rMMRK3VmP778dUJCeQjBcQ4arXZ
1 3DMveQocjGHzEAzZQBM7W9LbtWPpKzTN7B
2 3Pru2QHnLj8uLq9n8eaoP4ekRUVGBtiBGL
last_change_index:  2

 ================================
BIP39-BIP84 | New Segwit Wallets:
[ - wallet_info - ]
m/84'/0'/0'
xprv:  zprvAdN52HMQ2Yo3okKTgq26vdf3ppGZtiEuqJKzNZG7ozJHeWG9P6qixZRfbjudets6Bbw14d7Y53bRngmzC121kKiofQ5kdFWRqaAHFAv7jep
xpub: zpub6rMRRntHrvMM2EPvnrZ7HmbnNr74JAxmCXFbAwfjNKqGXJbHve9yWMk9SzsF9jQHM6RsaExfmAjyypn369i5dT3uXrRyiDra5nqpCjuPmWT
----------------
[ - add3 - ]
0 bc1qg0azlj4w2lrq8jssrrz6eprt2fe7f7edm4vpd5
1 bc1q57swnsnzhrdjmlj7wexe7x8emgrhwd04n2gktd
2 bc1qpvsc52v2h2856mg67tx0z804c86f5cu6apg3un
last_change_index:  2

"""

