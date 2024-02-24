import time
from crypto_agama.agama_transform_tools import hash_sha256_str

"""
inspir:
~$ i=0; while ! (echo -n "Agama Point $i" | sha256sum | tr -d "\n"; echo " (nonce=$i)")|grep -E "^00"; do let i++; done
"""


def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = round(end_time - start_time, 3)
        print(f"Function {func.__name__} took {execution_time} seconds", end="")
        print(f"({round(execution_time/60, 2)} min.)") if execution_time > 60 else print()
        return result
    return wrapper


@measure_time
def sub_mining(message="Agama Point", hr=2):
    print()
    print("="*30, hr)
    nonce = 0
    ## step = 10000000
    while True:
        message_with_nonce = message + " " +str(nonce) #f"{message} {str(nonce)}".encode('utf-8')
        
        hash_result = hash_sha256_str(message_with_nonce) #hashlib.sha256(message_with_nonce).hexdigest()
        
        if hash_result.startswith('0'*hr):
            print(f"Nonce found: {nonce} -> ", message_with_nonce)
            print(f"SHA256 Hash: {hash_result}")
            break
        
        nonce += 1
        ## if nonce % step == 0: print(nonce/step,end=" | ")


"""
print(hash_sha256_str("Agama Point"))
#bf11c007b3eddfa1ebcca54617f27c337e14ea840551537d8a239945b04abd00

print(hash_sha256_str("Agama Point 263"))
#00999ac48b71fc267a67f78bb379d554020d062343d344269d62d4b9f55b90b1
"""


for i in range(2,8):
    sub_mining("Agama Point", i)


"""
============================== 2
Nonce found: 263 ->  Agama Point 263
SHA256 Hash: 00999ac48b71fc267a67f78bb379d554020d062343d344269d62d4b9f55b90b1
Function sub_mining took 0.0 seconds

============================== 3
Nonce found: 3439 ->  Agama Point 3439
SHA256 Hash: 00059e3f5b79199b149f1da0535603c2f466dab975e07528b5c180b9a6616b9e
Function sub_mining took 0.017 seconds

============================== 4
Nonce found: 101339 ->  Agama Point 101339
SHA256 Hash: 000036cb70be3b8235589a84b92ffefbee4344429f57235036a00c89f89ff6b3
Function sub_mining took 0.164 seconds

============================== 5
Nonce found: 411413 ->  Agama Point 411413
SHA256 Hash: 0000031fc7878dfd5be258443c6d8ab63308c8ccaecc2829bb24ef3d72928de4
Function sub_mining took 0.651 seconds

============================== 6
Nonce found: 587451 ->  Agama Point 587451
SHA256 Hash: 0000007f91c02305905d3583c461bb1985b8f957524b115a0287ab5bd0901f00
Function sub_mining took 1.027 seconds

============================== 7
Nonce found: 209949850 ->  Agama Point 209949850
SHA256 Hash: 00000005434496a4937f988f644002737b4cda57137fd05f061690de6ca715a5
Function sub_mining took 317.216 seconds(5.29 min.)
"""
