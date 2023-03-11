"""
AgamaPoint - 2023
simple Mempool/Etc. library
"""

import time, datetime
import requests, json
# import subprocess

__version__ = "0.23.03"

DEBUG = True
WIDTH = 50

URL_BASE_LOCAL  = 'http://192.168.0.220:3006/api/' # my Umbrel - local IP
URL_BASE_REMOTE = 'https://mempool.space/api/'



class Mempool():
    def __init__(self, hw=1):
        if DEBUG:
            print("-"* WIDTH)
            print("class Mempool init")
            
        self.url_base = URL_BASE_LOCAL
        self.debug = DEBUG # main global debug mode
        
    def set_url_base(self, val_str):  
        if val_str == "local":
            self.url_base = URL_BASE_LOCAL

        if val_str == "remote":
            self.url_base = URL_BASE_REMOTE

        print("-"* WIDTH)
        print("set_url_base --- >",self.url_base)

    def set_debug_mode(self, debug):
        self.debug = debug
        print("-"* WIDTH)
        print("set_debug --- >",self.debug)


    # ------------------------------------------------------------


    def get_block_info(self, b, debug2 = False, tx_info = False):
        if self.debug: print("\r\n[get_block_info]")
        url = self.url_base  +"block-height/"+str(b)

        if debug2:
            print()
            print("="*WIDTH) 
            print('get_block:', b)
            print('- url', url)

        response = requests.get(url, allow_redirects=True, timeout=50)  
        """
        curl -sSL > -L allow_redirects=True    
        """

        if response.status_code == 404:
            raise ValueError("Block not found")

        if response.status_code == 200:
            block_hash = response.text
        else:
            print("Request failed with status code:", response.status_code)
        
        url = self.url_base  + 'block/'+str(block_hash)
        response = requests.get(url, allow_redirects=True, timeout=10)
        data = response.text
        json_data =  json.loads(data)
        
        if debug2: 
            print('===== json_data',json_data)
            print('- id',json_data["id"])

        dt = datetime.datetime.fromtimestamp(json_data["timestamp"])
        print(f"[{b}] {block_hash} | {dt}")

        # transactions
        url = self.url_base + 'block/'+str(block_hash)+'/txids'
        response = requests.get(url)   

        json_data_txs = response.text
        if debug2: 
            print("transactions",json_data_txs)
        json_data_txs =  json.loads(json_data_txs)

        lentx = len(json_data_txs)
        if lentx > 0:
            if debug2: print('len', len(json_data_txs))
            if tx_info:
                for tx_id in json_data_txs:
                    self.get_tx_info(tx_id, debug2 = self.debug)
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
        return lentx, dt, json_data_txs, json_data["id"]



    def get_tx_info(self, tx_id, debug2 = False):
        if self.debug: print("\r\n[get_tx_info]")
        url = self.url_base + 'tx/'+str(tx_id)

        if debug2: 
            print("-"*WIDTH)
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

        inputs = data_tx.get("vin") 
        outputs = data_tx.get("vout") # Získání seznamu výstupů transakce
        # dt = datetime.datetime.fromtimestamp(data_tx.get("block_time"))
        status = data_tx.get("status")
        block_time = datetime.datetime.fromtimestamp(status.get("block_time"))
        block_height = status.get("block_height")
        if debug2:
            print(f"> input---value [BLOCK {block_height} | {block_time}]")
        else:
            print("> input---value")

        for input in inputs: # Prohledání výstupů transakce a hledání textu opreturn
                if debug2: 
                    print(input)
                print(input.get("value"))
                
        print("> output---value---scriptpubkey_type")
        for output in outputs: # Prohledání výstupů transakce a hledání textu opreturn
                if debug2:
                    print(output)
                #  print("scriptpubkey_address", output.get("scriptpubkey_address"))
                print(f"{output.get('value'):12} {output.get('scriptpubkey_type'):12} {output.get('scriptpubkey_address')}")
                # scriptpubkey = output.get("scriptpubkey")
        
        return inputs, outputs
                
                

    def get_opreturn(self, tx_id, debug2 = False):
        if self.debug: print("\r\n[get_opreturn]", tx_id)
        url = self.url_base + 'tx/'+str(tx_id)

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
        
        outputs = data_tx.get("vout")

        if debug2: 
            print("===== outputs",outputs)

        inputs = data_tx.get("vin")
        if debug2: 
            print("===== inputs",inputs)

        # vout.scriptsig hledam: 104455468652054696d657...            
        
        op_return = None
        ns = 16

        for input in inputs:
                if debug2:
                    print("===== input",input)
                
                scriptsig = input.get("scriptsig")
                
                if DEBUG: 
                    print("scriptsig:",scriptsig)
                if debug2:
                    print("scriptsig[ns:]:",scriptsig[ns:])
                    

        """       
        if op_return is None:
            raise ValueError("OP_RETURN not found in transaction outputs")
    
        op_return_txt = scriptsig.decode("hex")
        print("op_return_txt",op_return_txt)
        """

        try:  
            decoded_string = bytes.fromhex(scriptsig[ns:]).decode('utf-8')
            print("decoded_string: ",decoded_string)
        except ValueError:
            print("Not a hexadecimal string")



    def get_addr(self, address, debug2 = True):
        if self.debug: print("\r\n[get_addr]")
        url = self.url_base + "address/" + address
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



    def get_addr_txs(self, address, debug2 = True):
        if self.debug: print("\r\n[get_addr_txs]")
        # url = f'https://blockchain.info/q/addressbalance/{address}'
        url = self.url_base + "address/" + address + "/txs"
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
        # if debug2: print("===== json_data_txs",json_data_txs)
        json_data_txs =  json.loads(json_data_txs)

        print("value","scriptpubkey_type")
        for tx in json_data_txs:
            if debug2: 
                # print(tx)
                # print("--- vin", tx["vin"][0]["value"])/10**8
                txi = tx['vin'][0]['prevout']
                try:
                    txaddr = (txi["scriptpubkey_address"])
                except:
                    txaddr = None
                # print(f"{txi['value']:12} {txi['scriptpubkey_type']:8} {txo['scriptpubkey_address']}")
                print(f"{txi['value']:12} {txi['scriptpubkey_type']:8} {txaddr} ")
                #funded_txo_sum = tx.get("chain_stats").get("funded_txo_sum")
            #funded_txo_sum = json_data_txs["chain_stats"]
            #print("funded_txo_sum",funded_txo_sum)

        

    def get_addr_utxo(self, address, debug2 = True):
        # url = f'https://blockchain.info/q/addressbalance/{address}'
        url = self.url_base + "address/" + address + "/utxo"
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



    def get_coins(self):
        url = self.url_base + "/blockchain/coins"

        response = requests.get(url)   
        # data = response.json()
        # data = response.text
        data = response.text

        try:
            print("blockchain/coins",data)
        except:
            print("Err")
        
        # return int(response.text)

"""
    def get_block_info_curl(b, debug2 = False):
        url = self.url_base +"block-height/"+str(b)

        result = subprocess.run(["curl",  "-sSL", url], stdout=subprocess.PIPE)
        # print(result.stdout.decode("utf-8"))
        block_hash = result.stdout.decode("utf-8").rstrip("\r\n")
        
        url = self.url_base + 'block/'+str(block_hash)
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
"""
