from crypto_agama.agama_trezor import get_default_client, t_connect,t_connect_first
from lib.logger import logger_init


# debug logging 
log = logger_init(log_file='data/debug_trezor.log')

log_msg = "[trezor] t_connect_first"
log.debug(log_msg)

client = t_connect_first() 
# client = get_default_client()    

print("="*50)
print("ok, finish")

"""
------------------------------------------------------------
- connecting to Trezor (get_default_client)

============================================================
device basic info:
============================================================
- client        <trezorlib.client.TrezorClient object at 0x7f0...cd0>
---  label      T202011
---  device_id  B3D...9A7
---  fw_version 2 4 2
------------------------------------------------------------
"""
