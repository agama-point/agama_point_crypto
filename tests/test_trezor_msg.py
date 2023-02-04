"""
2023/02 - agamapoint - simple verify
https://github.com/trezor/trezor-firmware
https://docs.trezor.io/trezor-firmware/
https://docs.trezor.io/trezor-firmware/python/trezorlib.html
"""

from trezorlib.client import get_default_client
from trezorlib.tools import parse_path
from trezorlib import btc

# Vyber bip32 cesty pro publikovy klic // bip32_path = client.expand_path("44'/0'/0'/0/0")
bip32_path = parse_path("44'/0'/0'/0/0")
print("bip32_path", bip32_path)

print("-"*12,"start","-"*12)

# Get the first address of first BIP44 account
# (should be the same address as shown in wallet.trezor.io)
address = "16MkCp4e3sSC6cksbJC288ZKJ7BBZ9dHhV"
print("Bitcoin address:", address)

print("-"*12,"verify","-"*12)
message = "test123"
client = get_default_client()

# signed_message_sig = b"\x1f|\xc0\xdf\xa2L\x02\x11\x1d\\7\x9f=qM.\xfb\xa0\x1eB\xa2\x89e\xb8\x94,\xfc]\xb5\xec\xe0\xdd\x0c0N\xac\x05F>\xd0\xb1\xb4\xc8\xd7\xe1\x00\xfa\xb3\xd5\xeb\x06\x01S4\x17R_i\x0f\xfa\xe1'\xd5^{"
hex_string = "1f7cc0dfa24c02111d5c379f3d714d2efba01e42a28965b8942cfc5db5ece0dd0c304eac05463ed0b1b4c8d7e100fab3d5eb0601533417525f690ffae127d55e7b"

signed_message_sig = bytes.fromhex(hex_string)
print("signed_message_sig",signed_message_sig)

verify = btc.verify_message(client, 'Bitcoin', address, signed_message_sig, message)
print("verify",verify)

# closing of communication
client.close()


"""
------------ start ------------
Bitcoin address: 16MkCp4e3sSC6cksbJC288ZKJ7BBZ9dHhV
------------ verify ------------
Please confirm action on your Trezor device.
verify True
"""
