"""
AgamaPoint23 - simple Mempool experiment
"""
from lib.agama_mempool_lib import Mempool
from lib.agama_blockchain_db import init_tables, add_block, add_tx, add_adrval, blocks_list, get_tx_uid, db_close
# url_base, set_url_base, get_addr, get_addr_txs, get_block_info, get_tx_info

DEBUG = True

#-------------
init_tables()
#-------------

m = Mempool()
if DEBUG: print("start", m.url_base)
m.set_url_base("remote")

# ========================================
# block = 0

# ------------ test ------------
# x
# -----------/ test ------------

for b in range(1050,1060): # 100000,100010 / 1055,1056
    data = m.get_block_info(b, False, True) # debug2, tx_info=True
    #print(b,data[0],data[1],data[2],data[3])
    add_block(b,data[0],data[1],data[2])

    print("*"*60)
    txs_list = data[3]
    for tx in txs_list:
        if not get_tx_uid(tx): # test unique uid
           add_tx(b, tx)
        tx_uid= get_tx_uid(tx)
        print(tx_uid, tx)
    print("*"*60)    

    txs_data_list = data[4]
    print("list_tx", len(txs_data_list))
    
    for data_tx in txs_data_list:
        #print(data_tx)
        print("txid",data_tx["txid"])
        
        inputs = data_tx["vin"]
        outputs = data_tx["vout"]
        print("-"*20)
        print("inputs", inputs)

        for inp in inputs:
            txid = inp["txid"] # test coinbase
            # 'is_coinbase': True
            if txid == '0000000000000000000000000000000000000000000000000000000000000000':
                print("COINBASE")
                addr = 0
            else:
                addr = inp["txid"]

            try:
                val = (inp["value"])
            except:
                val = -1    
            print("inp.val",val)

            add_adrval(tx_uid, "in", addr, "", val)

        for out in outputs:
            type = out["scriptpubkey_type"]
            val = out["value"]
            print("out.val",val)


            try:
                if type =="p2pkh":
                    addr = out["scriptpubkey_address"]
                if type =="p2pk":
                    addr = out["scriptpubkey"]
            except:
                addr = "err"
     
            add_adrval(tx_uid, "out", addr, type, val)

        """
        txid = inputs[0]["txid"] # test coinbase
        if txid == '0000000000000000000000000000000000000000000000000000000000000000':
            print("COINBASE")
        """
        print("-"*20)
        print("outputs", outputs)
        print(outputs[0]["scriptpubkey_type"])
   
    

print("="*50)
#blocks_list()
db_close()
