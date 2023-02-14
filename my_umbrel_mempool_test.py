from lib.agama_umbrel_lib import URL_BASE, get_coins, get_addr, get_addr_txs, get_block_info, get_tx_info


DEBUG = True

print("start", URL_BASE)

#get_coins()

addr="bc1qdkknh0drs79nqkq553umngh3dfmxzwsrp80cnp" # trezor
addr="bc1pjp5mfnfgrer8fzjshy66xw5cec436yc774dflmfntu6a40uv56jss57t53" # umbrel

get_addr(addr, True)

#err get_addr_utxo(addr, True)
get_addr_txs(addr, True)


block = 0
print('-'*50)
get_block_info(block, True, True)

"""
tx1 = "0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098"
tx0 = "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"
get_tx_info(tx0, True)
"""

"""
print('-'*50)

for block in range(100,110):
    get_block_info(block, False, False)
"""