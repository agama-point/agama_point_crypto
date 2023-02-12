import requests
import json
import datetime
import subprocess

DEBUG = True
WIDTH = 50

URL_BASE = 'http://192.168.0.220:3006/api/' # Umbrel - local IP
#  url_base = 'https://mempool.space/api/'

# -------------------------------------------------------------------------------


def get_block_info(b, debug2 = False, tx_info = False):
    url = URL_BASE  +"block-height/"+str(b)

    if debug2:
       print()
       print("="*WIDTH) 
       print('get_block:', b)
       print('- url', url)

    response = requests.get(url, allow_redirects=True, timeout=20)  
    """
    curl -sSL > -L allow_redirects=True    
    """

    if response.status_code == 404:
        raise ValueError("Block not found")

    if response.status_code == 200:
        block_hash = response.text
    else:
        print("Request failed with status code:", response.status_code)
    

    url = URL_BASE + 'block/'+str(block_hash)
    response = requests.get(url, allow_redirects=True, timeout=10)
    data = response.text
    json_data =  json.loads(data)

    if debug2: 
        print('===== json_data',json_data)
        print('- id',json_data["id"])

    dt = datetime.datetime.fromtimestamp(json_data["timestamp"])
    print("["+str(b)+"]", block_hash, dt) # 1, 00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048

    # transactions
    url = URL_BASE + 'block/'+str(block_hash)+'/txids'
    response = requests.get(url)   

    json_data_txs = response.text
    if debug2: print("transactions",json_data_txs)
    json_data_txs =  json.loads(json_data_txs)

    lentx = len(json_data_txs)
    if lentx > 0:
        if debug2: print('len', len(json_data_txs))
        if tx_info:
            for tx_id in json_data_txs:
                get_tx_info(tx_id, debug2 = True)
                """
                print(tx)
                #"https://mempool.space/api/tx/15e10745f15593a899cef391191bdd3d7c12412cc4696b7bcb669d0feadc8521"
                url = URL_BASE + 'tx/'+str(tx_id)
                response = requests.get(url)   
                data_tx = response.text
                json_data_tx =  json.loads(data_tx)
                if debug2: 
                    print("===== json_data_tx",json_data_tx)
                    print("--- fee", json_data_tx["fee"])
                    print("--- vout", int(json_data_tx["vout"][0]["value"])/10**8)
                """

def get_tx_info(tx_id, debug2 = True):
    url = URL_BASE + 'tx/'+str(tx_id)

    if debug2: 
        print("="*WIDTH)
        print("tx_info url", url)
    if len(tx_id) != 64:
        raise ValueError("Invalid transaction ID")

    response = requests.get(url)   

    if response.status_code == 404:
        raise ValueError("Transaction not found")
    
    if response.status_code != 200:
        raise ValueError("Failed to retrieve transaction")

    data_tx = response.json()
    if debug2: 
        print("data",data_tx)
    outputs = data_tx.get("vout") # Získání seznamu výstupů transakce

    op_return = None
    for output in outputs: # Prohledání výstupů transakce a hledání textu opreturn
            print("===== output",output)
            print("- value",output.get("value"))
            """zacina 6a pokud má scriptPubKey hodnotu "6a04616263646566", tak data "abcdef" byla uložena v rámci transakce."""
            scriptpubkey = output.get("scriptpubkey")
            if debug2: 
                print("*"*WIDTH)
                print("- scriptpubkey",scriptpubkey)
                print("*"*WIDTH)
            op_return = scriptpubkey


            print("- scriptpubkey_asm",output.get("scriptpubkey_asm"))
            #op_return = output.get("scriptpubkey_asm").get("OP_PUSHBYTES_65")
            """
            op_pushbytes = data_tx['vout'][0]['scriptpubkey_asm'].split()[1]
            if debug2: 
                print("."*50)
                print(op_pushbytes)
                print("."*50)
            op_return = op_pushbytes
            """    

            """
            if output.get("scriptpubkey").get("hex").startswith("6a"):
                op_return = output.get("scriptpubkey").get("hex")
                break
            """

    if op_return is None:
        raise ValueError("OP_RETURN/OP_PUSHBYTES_65 not found in transaction outputs")

    # Získání textu opreturn
    # op_return = op_return[10:].decode("hex")
    # decoded_string = bytes.fromhex(op_return).decode('utf-8')
    
    try:
        decoded_string = bytes.fromhex(op_return)
        print(decoded_string)
    except ValueError:
        print("Not a hexadecimal string")
    

    """
    if debug2: 
        print()
        print("===== json_data_tx",json_data_tx)
        print("--- fee", json_data_tx["fee"])
        print("--- vout", int(json_data_tx["vout"][0]["value"])/10**8)
    """

def get_addr(address, debug2 = True):
    url = URL_BASE + "address/" + address
    if debug2:
        print()
        print("="*WIDTH) 
        print("get_addr:",url)
        print("-"*WIDTH)

    response = requests.get(url, allow_redirects=True, timeout=20)
    
    if response.status_code == 404:
        raise ValueError("Address not found")
    
    if response.status_code != 200:
        raise ValueError("Failed to retrieve address")
      
    data = response.json()
    if debug2: 
        print(data)



def get_addr_txs(address, debug2 = True):
    # url = f'https://blockchain.info/q/addressbalance/{address}'
    url = URL_BASE + "address/" + address + "/txs"
    if debug2:
        print()
        print("="*WIDTH) 
        print("get_addr_txs:",url)
        print("-"*WIDTH)

    response = requests.get(url, allow_redirects=True, timeout=10)

    if response.status_code == 404:
        raise ValueError("Address not found")
    
    if response.status_code != 200:
        raise ValueError("Failed to retrieve address")
    

    json_data_txs = response.text
    if False: print("===== json_data_txs",json_data_txs)
    json_data_txs =  json.loads(json_data_txs)

    for tx in json_data_txs:
        if debug2: 
            print("+"*50)
            # print(tx)
            # print("--- vin", tx["vin"][0]["value"])/10**8
            print("+++ scriptpubkey_type", tx["vin"][0]["prevout"]["scriptpubkey_type"])
            print("+++ value", tx["vin"][0]["prevout"]["value"])
            #funded_txo_sum = tx.get("chain_stats").get("funded_txo_sum")
        #funded_txo_sum = json_data_txs["chain_stats"]
        #print("funded_txo_sum",funded_txo_sum)

    


def get_addr_utxo(address, debug2 = True):
    # url = f'https://blockchain.info/q/addressbalance/{address}'
    url = URL_BASE + "address/" + address + "/utxo"
    if debug2:
        print()
        print("="*WIDTH) 
        print("get_addr_utxo:",url)
        print("-"*WIDTH)

    response = requests.get(url)

    if response.status_code == 404:
        raise ValueError("Address not found")
    
    if response.status_code != 200:
        raise ValueError("Failed to retrieve address")
    
    return int(response.text)



def get_coins():
    url = URL_BASE + "/blockchain/coins"

    response = requests.get(url)   
    # data = response.json()
    # data = response.text
    data = int(response.text)

    try:
        print("blockchain/coins",data)
    except:
        print("Err")
    
    # return int(response.text)


def get_block_info_curl(b, debug2 = False):
    url = URL_BASE  +"block-height/"+str(b)

    result = subprocess.run(["curl",  "-sSL", url], stdout=subprocess.PIPE)
    # print(result.stdout.decode("utf-8"))
    block_hash = result.stdout.decode("utf-8").rstrip("\r\n")
    
    url = URL_BASE + 'block/'+str(block_hash)
    result = subprocess.run(["curl",  "-sSL", url], stdout=subprocess.PIPE)
    data = result.stdout.decode("utf-8").rstrip("\r\n")
    json_data =  json.loads(data)
    if debug2: 
        print('--- data',json_data)
        print('- id',json_data["id"])
    dt = datetime.datetime.fromtimestamp(json_data["timestamp"])
    
    print(b, "block_hash", block_hash, dt)

    # transactions
    url = URL_BASE + 'block/'+str(block_hash)+'/txids'
    result = subprocess.run(["curl",  "-sSL", url], stdout=subprocess.PIPE)
    data = result.stdout.decode("utf-8").rstrip("\r\n")

    json_data_txs =  json.loads(data)
    lenx = len(json_data_txs)
    if lenx > 1:
        print('-'*50)
        print('len', lenx)
        for tx in json_data_txs:
            print(tx)
            #"https://mempool.space/api/tx/15e10745f15593a899cef391191bdd3d7c12412cc4696b7bcb669d0feadc8521"
            url = url_base + 'tx/'+str(tx)
            response = requests.get(url)   
            data_tx = response.text
            json_data_tx =  json.loads(data_tx)
            if debug2: print(json_data_tx)
            
            print("--- fee", json_data_tx["fee"])
            print("--- vout", int(json_data_tx["vout"][0]["value"])/10**8)
