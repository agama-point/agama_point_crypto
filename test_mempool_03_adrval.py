"""
AgamaPoint23 - simple Mempool experiment
"""
from crypto_agama.agama_mempool import Mempool
from crypto_agama.agama_blockchain_db import init_tables, add_block, add_tx, add_adrval, blocks_list, get_tx_uid, get_addr, delete_all, db_close
# url_base, set_url_base, get_addr, get_addr_txs, get_block_info, get_tx_info

DEBUG = True
DEBUG2 = False

#-------------
#init_tables()
#-------------
# delete_all()

m = Mempool()
if DEBUG: print("start", m.url_base)
m.set_url_base("remote")

# ========================================
# block = 0
# list of blocks [465, 473, 1055, 0] first txs
blocks = range(500000,500001)
blocks = [0,1,2,465,473,1055,1056]
blocks = range(6300,6500)


for b in blocks: # 100000,100010 / 1055,1056
    print()
    print("-"*20)
    print(b)
    print("-"*20)
    data = m.get_block_info(b, False, True) # debug2, tx_info=True
    #print(b,data[0],data[1],data[2],data[3])
    add_block(b,data[0],data[1],data[2])

    txs_list = data[3]
    for tx in txs_list:
        if not get_tx_uid(tx): # test unique uid
           add_tx(b, tx)
        tx_uid= get_tx_uid(tx)
        if DEBUG2: print(tx_uid, tx)

    txs_data_list = data[4]
    if DEBUG2: print("list_tx", len(txs_data_list))
    
    for data_tx in txs_data_list:
        #print(data_tx)
        if DEBUG2: print("txid",data_tx["txid"])
        
        inputs = data_tx["vin"]
        outputs = data_tx["vout"]

        if DEBUG2: print("inputs", inputs)
               
        #---------------------------------------------------------------------------------------- inputs
        for inp in inputs:
            if DEBUG2:
                try:
                    print("=== input prevout scriptpubkey", inp["prevout"]["scriptpubkey"])
                    print("scriptpubkey_type", inp["prevout"]["scriptpubkey_type"])
                    print("value", inp["prevout"]["value"])
                except:
                    print("Err. input prevout")

            txid = inp["txid"] # test coinbase
            
            try:
                type = inp["prevout"]["scriptpubkey_type"]
            except:
                type = ""
                print("Err. inp.scriptpubkey_type")

            #if type =="p2pk":
            try:
                addr = inp["prevout"]["scriptpubkey"]
            except:
                addr = -9    
            
            try:
                val = inp["prevout"]["value"]
            except:
                val = -1        
            
            # 'is_coinbase': True
            if txid == '0000000000000000000000000000000000000000000000000000000000000000':
                if DEBUG2: print("COINBASE")
                addr = 0
                val = 0

            nbid = get_addr(addr)
            print(val, "*** if val>0 add_adrval",b, tx_uid, "in", addr, type, val, nbid[1], nbid)

            if val > 0:
                add_adrval(b, tx_uid, "in", addr, type, val, nbid[1])

        #---------------------------------------------------------------------------------------- outputs
        for out in outputs:
            type = out["scriptpubkey_type"]
            val = out["value"]
            if DEBUG2: print("out.val",val)

            try:
                if type =="p2pkh":
                    addr = out["scriptpubkey_address"]
                if type =="p2pk":
                    addr = out["scriptpubkey"]
            except:
                addr = "err"

            nbid = get_addr(addr)
            if DEBUG2: print("nbid",nbid, addr)
            add_adrval(b, tx_uid, "out", addr, type, val, nbid[1])

        if DEBUG2: 
            print("outputs", outputs)
            print(outputs[0]["scriptpubkey_type"])

print("="*50)
#blocks_list()
db_close()
