"""
AgamaPoint23 - simple Mempool experiment
"""
from crypto_agama.agama_umbrel import Mempool
# url_base, set_url_base, get_addr, get_addr_txs, get_block_info, get_tx_info

DEBUG = True

m = Mempool()

if DEBUG:
    print("start", m.url_base)

m.set_url_base("remote")

#get_coins()
"""
block = 0
print('-'*50)
m.get_block_info(block, True, True)
"""

print("="*80, "tx1")
tx1 = "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b" # first blockchain coinbase transaction from block 0
m.get_tx_info(tx1,True)

print("="*80, "tx2")
tx2 = "f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16" # block 170 / first tx A2B (P2PK)
m.get_tx_info(tx2)

"""
================================================================================ tx2
[get_tx_info]
---input---value [BLOCK 170 | 2009-01-12 04:30:25]
None
---output---value---scriptpubkey_type
scriptpubkey_address None
1000000000 p2pk
scriptpubkey_address None
4000000000 p2pk
"""

print("="*80, "tx3")
tx3 = "00e45be5b605fdb2106afa4cef5992ee6d4e3724de5dc8b13e729a3fc3ad4b94" # block 2812 / 6 txs first (P2PKH)
m.get_tx_info(tx3, True)

#m.get_addr(addr1, True)


addr="bc1qdkknh0drs79nqkq553umngh3dfmxzwsrp80cnp" # trezor
addr="bc1pjp5mfnfgrer8fzjshy66xw5cec436yc774dflmfntu6a40uv56jss57t53" # um
addr="1AbHNFdKJeVL8FRZyRZoiTzG9VCmzLrtvm" # TX3, first addr?

m.get_addr(addr, True)

#err get_addr_utxo(addr, True)
m.get_addr_txs(addr, True)
