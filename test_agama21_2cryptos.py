# agama_point - crypto21 - 2021
# https://wolovim.medium.com/ethereum-201-hd-wallets-11d0c93c87f7
# generate, to_seed, to_hd_master_key(seed), to_mnemonic

# seed_bytes => words + passphrase
# to_hd_master_key / create_root_key

from mnemonic import Mnemonic
from crypto_agama.transform import create_root_key

TW = 80 # terminal width

mnemo = Mnemonic("english")

print("-"*TW)
print("agama_point - crypto21 - Bitcoin test")
print("-"*TW)
##words = mnemo.generate(strength=128) # 128-256 (12/24)

from priv_data import get_words # words 
words = get_words()
print(words)

#seed = mnemo.to_seed(words, passphrase="SuperDuperSecret")
seed_bytes = mnemo.to_seed(words, passphrase="")
print("mnemo.to_seed = seed_bytes: ", seed_bytes)

xprv = mnemo.to_hd_master_key(seed_bytes)
print("mnemo.to_hd_master_key = xprv: ", xprv) 

##print(mnemo.to_mnemonic(hdmk))

entropy = mnemo.to_entropy(words)
print("entropy: ", entropy)

print("-"*TW)

print("create_root_key: ", create_root_key(seed_bytes))
print("_______root_www: ", "xprv9s21ZrQH143K3Lkdp2LWERaQjMDcGfCLLVrB3QsKmxNPqrwAcGimMY8c3p95mwDieoNAE19rKNqH3FnhiEBFxUa2RWUThPxYjdQ64HQ82Lw")
# xprv9s21ZrQH143K...T2emdEXVYsCzC2U


print("-"*TW)
print("cryptos:")

# https://github.com/primal100/pybitcointools
from cryptos import * # pip install wheel, pbkdf2, cryptos
#words = entropy_to_words(os.urandom(16))

print("wodrs checkum-valid: ", keystore.bip39_is_checksum_valid(words))

"""
c = Bitcoin(testnet=True)
priv = sha256(words)
print("priv:", priv)

pub = c.privtopub(priv)
print("pub:", pub)

addr = c.pubtoaddr(pub)
print("addr:", addr)

print("-"*TW)

#inputs = c.unspent(addr)
#print("inputs:", inputs)
"""

coin = Bitcoin(testnet=True)
wallet = coin.wallet(words)
print("wallet: ", wallet)
der = wallet.keystore.root_derivation # "m/44'/0'/0'"
print("root_derivation: ", der)

xprv = wallet.keystore.xprv
print("xprv: ", xprv)

xpub = wallet.keystore.xpub
print("xpub: ", xpub)

addr1 = wallet.new_receiving_address()
print("addr1: ", addr1)

wpk1 = wallet.privkey(addr1)
print("wallet.privkey: ", wpk1)

print("-"*TW)
addr2 = wallet.new_change_address()
print("addr2: ", addr2)

print("-"*TW)

# ---------------------------------------------------------------
"""
print("BIP84-test")
words_84 = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
#https://github.com/bitcoin/bips/blob/master/bip-0084.mediawiki
words = words_84
print(words)
seed_bytes = mnemo.to_seed(words, passphrase="")
xprv = mnemo.to_hd_master_key(seed_bytes)
print("mnemo.to_hd_master_key = xprv: ", xprv) 
print("create_root_key: ", create_root_key(seed_bytes))
"""

print("--- blockcypher ---")



print("ok")
