from lib.agama_umbrel_lib import Mempool

DEBUG = True

m = Mempool()
m.set_url_base("local")
m.set_debug_mode(False)

file_name = "data_input/block_0-1000.txt"
# file_name = "data_input/block_777000.txt"


with open(file_name, "r") as f:
    lines = f.readlines()
    
for i, line in enumerate(lines):
    if i == 0:
        continue
    values = line.strip().split(";")
    block = values[0]
    print("="*60)
    data = m.get_block_info(block, False, False)
    print(i, data[0], data[1])
    txs = data[2]
    for i, tx in enumerate(txs):
        print("----- ",i, tx)
        m.get_tx_info(tx, False)



"""
data_output/test_block_txs_addr_0-1000.txt
data_output/test_block_txs_addr_770k.txt

"""
