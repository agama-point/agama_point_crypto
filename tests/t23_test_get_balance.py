from lib.agama_trezor_lib import get_balance, print_rawaddr


address = 'bc1pq37d...gdwrxwssuxkzw'
balance = get_balance(address)
print("balance",balance)


print_rawaddr(address)
