from trezorlib.transport import get_transport
from trezorlib.client import TrezorClient, get_default_client
from trezorlib.tools import parse_path
from trezorlib import btc, misc, ui
from trezorlib.messages import InputScriptType
import requests
import datetime
import base58


__version__ = "0.2.3"

"""
2023/02 - agamapoint

https://docs.trezor.io/
https://docs.trezor.io/trezor-firmware/python/trezorlib.html
https://github.com/trezor/trezor-firmware

"""

DEBUG = True
DEBUG2 = False
WIDTH = 60
# -------------------------------- device -------------------------------------------

"""
---
<Features: {'vendor': 'trezor.io', 'major_version': 2, 'minor_version': 5, 'patch_version': 3, 
'device_id': '8C937A...2A2AE', 'pin_protection': True, 'passphrase_protection': True, 
'language': 'en-US', 'label': 'Agama21', 'initialized': True, 
'revision': b'/\x03\xac\xe3\x11XI\x88\xd5\xae\xabX\xfd\x1a\xcf$\xefTq\x1a', 
'unlocked': True, 'needs_backup': False, 'flags': 0, 'model': 'T', 'fw_vendor': 
'SatoshiLabs', 'unfinished_backup': False, 'no_backup': False, 'recovery_mode': False, 
'capabilities': [<Capability.Bitcoin: 1>, <Capability.Bitcoin_like: 2>, 
<Capability.Binance: 3>, <Capability.Cardano: 4>, <Capability.Crypto: 5>, 
<Capability.EOS: 6>, <Capability.Ethereum: 7>, <Capability.Monero: 9>, 
<Capability.NEM: 10>, <Capability.Ripple: 11>, <Capability.Stellar: 12>, 
<Capability.Tezos: 13>, <Capability.U2F: 14>, <Capability.Shamir: 15>, 
<Capability.ShamirGroups: 16>, <Capability.PassphraseEntry: 17>], 'backup_type': <BackupType.Bip39: 0>, 
'sd_card_present': False, 'sd_protection': False, 'wipe_code_protection': False, 
'passphrase_always_on_device': False, 'safety_checks': <SafetyCheckLevel.Strict: 0>, 
'auto_lock_delay_ms': 600000, 'display_rotation': 0, 'experimental_features': False, 'busy': False}>
"""

def t_print_basic_info(client):
    print("="*WIDTH)
    print("device basic info:")
    print("="*WIDTH)
    print("- client       ", client) # --- client: <trezorlib.client.TrezorClient object at 0x7f515b6d5300> ["label"]
    print("---  label     ", client.features.label) # 
    print("---  device_id ", client.features.device_id) # --- Agama21
    print("---  fw_version", client.features.major_version, client.features.minor_version, client.features.patch_version)
    print("-"*WIDTH)


def t_connect_first():
    if DEBUG:
        print("-"*WIDTH)
        print("- connecting to Trezor (get_default_client)")
        print()

    # Use first connected device
    try:
        client = get_default_client()
        t_print_basic_info(client)
    
    except Exception as e:
        if DEBUG:
            print(e)

    return client


def t_connect():
    if DEBUG:
        print("-"*WIDTH)
        print("- connecting to Trezor (TrezorClient, get_transport/ui)")

    # transport = get_transport() # --- bridge:1

    try:
        client = TrezorClient(get_transport(), ui=ui.ClickUI())
        t_print_basic_info(client)
        
    except Exception as e:
        if DEBUG:
            print(e)

    return client


"""
btc: 
'authorize_coinjoin', 'copy', 'exceptions', 'expect', 'from_json', 'get_address', 'get_authenticated_address', 
'get_ownership_id', 'get_ownership_proof', 'get_public_node', 'messages', 'prepare_message_bytes', 'session', 
'sign_message', 'sign_tx', 'verify_message', 'warnings'
"""


# -------------------------------- address -------------------------------------------

def get_btc_address(client,type="SPENDADDRESS",index = 0,show_disp=False):
    # if type == "SPENDADDRESS":
    basic_prefix = "44'/0'/0'/0/"
    btc_script_type = InputScriptType.SPENDADDRESS

    if type == "SPENDP2SHWITNESS":
        basic_prefix = "49'/0'/0'/0/" 
        btc_script_type = InputScriptType.SPENDP2SHWITNESS   

    if type == "SPENDWITNESS":
        basic_prefix = "84'/0'/0'/0/"
        btc_script_type = InputScriptType.SPENDWITNESS   

    if type == "SPENDTAPROOT":
        basic_prefix = "86'/0'/0'/0/"
        btc_script_type = InputScriptType.SPENDTAPROOT  


    path = basic_prefix+str(index)

    bip32_path = parse_path(path)
    address = btc.get_address(client, "Bitcoin", bip32_path, show_display=show_disp, script_type=btc_script_type)
    return address, path


"""
base58_addr = address
# base58_addr = "16MkCp4e3sSC6cksbJC288ZKJ7BBZ9dHhV"
public_key_hex = base58.b58decode(base58_addr).hex()
"""


"""
--- suite:
16MkCp4e3sSC6cksbJC288ZKJ7BBZ9dHhV

--- python:
address = btc.get_address(client, "Bitcoin", bip32_path, True)
print("Bitcoin address:", address)
# ("44'/0'/0'/0/0")  --- Bitcoin address: 16MkCp4e3sSC6cksbJC288ZKJ7BBZ9dHhV

#trezorctl get-address --coin Bitcoin --script-type address --address "m/44'/0'/0'/0/0"
#Please confirm action on your Trezor device.
#16MkCp4e3sSC6cksbJC288ZKJ7BBZ9dHhV


index = 0
basic_prefix = "44'/0'/0'/0/"
path = basic_prefix+str(index)

bip32_path = parse_path(path)
address = btc.get_address(client, "Bitcoin", bip32_path, True, script_type=InputScriptType.SPENDADDRESS)
print(path, "address:", address) # SPENDADDRESS: 1/16Mk...
print("-"*50)

path = "49'/0'/0'/0/0"
bip32_path = parse_path(path)
address = btc.get_address(client, "Bitcoin", bip32_path, True, script_type=InputScriptType.SPENDP2SHWITNESS)
print(path, "Bitcoin address:", address) # SPENDWITNESS: 3/3DSrz...

path = "84'/0'/0'/0/0"
bip32_path = parse_path(path)
address = btc.get_address(client, "Bitcoin", bip32_path, True, script_type=InputScriptType.SPENDWITNESS)
print(path, "Bitcoin address:", address) # SPENDWITNESS: bc1q/bc1qd...


trezor_github_src/trezor-firmware-master/core/tests/test_apps.bitcoin.address.py

client: 
    "TrezorClient",
    coin_name: str,
    n: "Address",
    show_display: bool = False,
    multisig: Optional[messages.MultisigRedeemScriptType] = None,
    script_type: messages.InputScriptType = messages.InputScriptType.SPENDADDRESS,
    ignore_xpub_magic: bool = False,

    
script_type:
correct_derivation_paths = [
            ([H_(44), H_(0), H_(0), 0, 0], InputScriptType.SPENDADDRESS),  
            # btc is segwit coin, but non-segwit paths are allowed as well
            
            ([H_(44), H_(0), H_(0), 0, 1], InputScriptType.SPENDADDRESS),
            ([H_(44), H_(0), H_(0), 1, 0], InputScriptType.SPENDADDRESS),
            ([H_(49), H_(0), H_(0), 0, 0], InputScriptType.SPENDP2SHWITNESS),
            ([H_(49), H_(0), H_(0), 1, 0], InputScriptType.SPENDP2SHWITNESS),
            ([H_(49), H_(0), H_(0), 0, 1123], InputScriptType.SPENDP2SHWITNESS),
            ([H_(49), H_(0), H_(0), 1, 44444], InputScriptType.SPENDP2SHWITNESS),
            ([H_(49), H_(0), H_(5), 0, 0], InputScriptType.SPENDP2SHWITNESS),
            ([H_(84), H_(0), H_(0), 0, 0], InputScriptType.SPENDWITNESS),
            ([H_(84), H_(0), H_(5), 0, 0], InputScriptType.SPENDWITNESS),
            ([H_(84), H_(0), H_(5), 0, 10], InputScriptType.SPENDWITNESS),
            ([H_(48), H_(0), H_(5), H_(0), 0, 10], InputScriptType.SPENDMULTISIG),
        ]

messages.
class InputScriptType(IntEnum):
    SPENDADDRESS = 0
    SPENDMULTISIG = 1
    EXTERNAL = 2
    SPENDWITNESS = 3
    SPENDP2SHWITNESS = 4
    SPENDTAPROOT = 5      
"""

# -------------------------------- blockchain -------------------------------------------
# --- blockchain.info ---

def get_balance(address):
    url = f'https://blockchain.info/q/addressbalance/{address}'
    if DEBUG2:
        print("-"*WIDTH) 
        print(url)
        print("-"*WIDTH)

    response = requests.get(url)
    return int(response.text)


def print_rawaddr(address):
    url = 'https://blockchain.info/rawaddr/' + address
    print("-"*WIDTH) 
    print(url)
    print("-"*WIDTH)
    try:
        response = requests.get(url)
        data = response.json()
        #  print("data", data)


        transactions = data['txs']
        for tx in transactions:
            if DEBUG2:
                print("."*WIDTH)
                print(tx)
                print("."*WIDTH)
            print("Transaction ID: ", tx['hash'])
            print("Time:   ", datetime.datetime.fromtimestamp(tx['time']).strftime('%Y-%m-%d %H:%M:%S'))
            print("Amount: ", tx['out'][0]['value'])
            print("Address:", tx['out'][0]['addr'])
            print("Balance:", tx['out'][1]['value'])
            print("-"*WIDTH)
    except:
        print("Err")

# -------------------------------- transactions -----------------------------------------
# ToDo
