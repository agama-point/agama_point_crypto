from cryptos import * # pip install wheel, pbkdf2, cryptos
from mnemonic import Mnemonic
from crypto_agama.agama_seed_tools import create_root_key

# https://pypi.org/project/cryptos/
# https://github.com/primal100/pybitcointools


def create_wallet(words, passphrase="", c="tBTC", wnum = 0, debug=True): # tBTC/BTC/LTC

    mnemo = Mnemonic("english")
    #seed = mnemo.to_seed(words, passphrase="SuperDuperSecret")
    seed_bytes = mnemo.to_seed(words, passphrase)

    xprv = mnemo.to_hd_master_key(seed_bytes)
    entropy = mnemo.to_entropy(words)

    coin = Bitcoin(testnet=True)
    if (c=="LTC"): coin = Litecoin(testnet=False)
    if (c=="BTC"): coin = Bitcoin(testnet=False)
    if (c=="tBTC"): coin = Bitcoin(testnet=True)
    if (c=="tLTC"): coin = Litecoin(testnet=True)

    wallet = coin.wallet(words)

    xprv = wallet.keystore.xprv
    xpub = wallet.keystore.xpub

    # test
    wallet.keystore.root_derivation = "m/84'/0'/0'"
    addr = wallet.new_receiving_address()
    wpk = wallet.privkey(addr)

    if wnum == 1:
      addr = wallet.new_change_address()
      wpk = wallet.privkey(addr)

    if wnum > 1:
      for gen in range(wnum):
        addr = wallet.new_change_address()
        wpk = wallet.privkey(addr)

    deriv = wallet.keystore.root_derivation # "m/44'/0'/0'"

    return addr, wpk, deriv, xprv, entropy

# -------- 2023 -----------------------------------

def coin_info(b):
    print("[ - coin_info - ]")
    print("coin_symbol:",b.coin_symbol)
    print("is_testnet: ",b.is_testnet)
    ## print("is_segwit:  ",b.is_segwit)
    ## print(b.current_block_height)


def wallet_info(c,w, debug=False):
    print("[ - wallet_info - ]")
    print(w.keystore.root_derivation)
    #? print("address_prefixes: ",c.address_prefixes)
    
    if debug:
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

