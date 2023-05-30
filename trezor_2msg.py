"""
2023/02 - agamapoint - sign message with trezor
https://github.com/trezor/trezor-firmware
https://docs.trezor.io/trezor-firmware/
https://docs.trezor.io/trezor-firmware/python/trezorlib.html
"""

from trezorlib.client import get_default_client
from trezorlib.tools import parse_path
from trezorlib import btc

from trezorlib.client import TrezorClient
#  from trezorlib.transport_hid import HidTransport # padá / nezná
from trezorlib.ui import ClickUI

from trezorlib import misc, ui
from trezorlib.transport import get_transport


"""
# Vytvoreni instance TrezorClient // client = TrezorClient(get_transport())
try:
    client = TrezorClient(get_transport(), ui=ui.ClickUI())
    print("--- client:", client) # --- client: <trezorlib.client.TrezorClient object at 0x7f515b6d5300> ["label"]
    print("[label]", client.features.label) # --- Agama21

except Exception as e:
    print(e)
"""


# Vyber bip32 cesty pro publikovy klic // bip32_path = client.expand_path("44'/0'/0'/0/0")
bip32_path = parse_path("44'/0'/0'/0/0")
print("bip32_path", bip32_path)


"""
https://docs.trezor.io/

pip3 install --upgrade setuptools
pip3 install trezor

https://github.com/trezor/python-trezor/blob/master/tools/helloworld.py

"""
print("-"*12,"start","-"*12)
print("connecting to Trezor")

try:
    ##client = TrezorClient(get_transport(), ui=ui.ClickUI())
    # Use first connected device
    client = get_default_client()
    
except Exception as e:
    print(e)


# Print out TREZOR's features and settings
# print(client.features)

print("- device id:   ", client.features.device_id)
print("- trezor label:", client.features.label)
print()


# Get the first address of first BIP44 account
# (should be the same address as shown in wallet.trezor.io)
address = btc.get_address(client, "Bitcoin", bip32_path, True)
print("Bitcoin address:", address)

"""
python:
address = btc.get_address(client, "Bitcoin", bip32_path, True)
print("Bitcoin address:", address)
# ("44'/0'/0'/0/0")  --- Bitcoin address: 16MkCp4e3sSC6cksbJC288ZKJ7BBZ9dHhV
"""

print("-"*12,"sign","-"*12)
message = "test123"
# signed_message = client.sign_message('Bitcoin', bip32_path, message, script_type='segwit')

signed_message = btc.sign_message(client, 'Bitcoin', bip32_path, message)
print("- signed_message", signed_message)

print("- signed_message.HEX",signed_message.signature.hex())



print("-"*12,"verify","-"*12)
message = "test123"


verify = btc.verify_message(client, 'Bitcoin', address, signed_message.signature, message)
print("verify",verify)


# Uzavreni komunikace s Trezorem
client.close()



"""
------------ start ------------
connecting to Trezor
- device id:    8C937A10F77699614B82A2AE
- trezor label: Agama21

Please confirm action on your Trezor device.
Bitcoin address: 16MkCp4e3sSC6cksbJC288ZKJ7BBZ9dHhV
------------ sign ------------
- signed_message <MessageSignature: {'address': '16MkCp4e3sSC6cksbJC288ZKJ7BBZ9dHhV', 'signature': b"\x1f|\xc0\xdf\xa2L\x02\x11\x1d\\7\x9f=qM.\xfb\xa0\x1eB\xa2\x89e\xb8\x94,\xfc]\xb5\xec\xe0\xdd\x0c0N\xac\x05F>\xd0\xb1\xb4\xc8\xd7\xe1\x00\xfa\xb3\xd5\xeb\x06\x01S4\x17R_i\x0f\xfa\xe1'\xd5^{"}>
- signed_message.HEX 1f7cc0dfa24c02111d5c379f3d714d2efba01e42a28965b8942cfc5db5ece0dd0c304eac05463ed0b1b4c8d7e100fab3d5eb0601533417525f690ffae127d55e7b
------------ verify ------------
verify True/False
"""
