from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives import serialization
from crypto_agama.tools import get_env_key
import ctypes


def hex_to_priv(hex):
    pem_key = bytes.fromhex(hex_key)
    private_key = serialization.load_pem_private_key(
        pem_key,
        password=None  # secret phrase or password=None
    )
    return private_key


# Generate the RSA private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=1024, #2048
)


# Výpis klíče jako hexa
pem_key = private_key.private_bytes(
    encoding=Encoding.PEM,
    format=PrivateFormat.PKCS8,
    encryption_algorithm=NoEncryption()
)

hex_key = pem_key.hex()

print("hex_key:")
print(hex_key)

# Výpis klíče jako bytearray
bytearray_key = bytearray(pem_key)

print("-"*39)

message = b"secret text"
ciphertext = private_key.public_key().encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print(ciphertext)

print("-"*39)
plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print(plaintext)

hex_key = "2d2d2d2d2d424547494e2050524956415445204b45592d2d2d2d2d0a4d494943646749424144414e42676b71686b6947397730424151454641415343416d417767674a6341674541416f4742414d782b556b496475675467667532740a6577597a57302f626a6f2f45484767462f6a796f4e34574644744c574a6244534365312b35567768775035505065474670554f6338736d6f666141616e5849610a772f4363416f44746235466f6479426341554a544a6670435a475544754b366e4f42677a4f6e2b45316a5167745771713658306e7a7346566e6365527a71334a0a3957493543385a6875312b45456572704f452f3963586c336e74356641674d42414145436759416432352f6c4758514d764436734d33565144585761726d4d640a614c514247456272306c2f773965475a4e5431686d506c73484f6765554b74654e6e48426d514c7459574174773555384b456175333275576d5344674d5857750a494e31477537417a4c5647654d74753056453855345070456f696937757473624c465064774e6b716b733431584138756d657a646562677138617a736b786b750a49744c39667148723348496e747a6f4f79514a42414f6f615071303051656b33705267576479366374746a3444414437412f74616e537032536d6339792b616f0a50316f625056346e33396b4f62683153502f7859396948564c41744a435268696c3356575363673465555543515144666e78444d496133647042776f2b794f630a4541725732416f4d594c6c31344e6d7256584f6d30622f43776b4b5830342b745a4d50364375363745524977674b76724754315839492b7871417048654771560a7a616c54416b45416736627579496b79352b30624d30697644632b6b4a4c436154354c61306d684c4b71344c656251504431426645465678565a6f6e45504a450a69736a4f6f794f4568394a5353715a774c76364448734841444a463134514a4161715636706b2b396b6f474d71494b314264326b766265456530693579687a300a306b424c6970686e6f714e776a4f58706c4b454530622f62414c337764633833726b52344f2f5533666c754d6f3238724c63784b58774a4156536b4c4a462b700a785148585a6e6572772b5963704945514d584f6239574c35353145706b4167466f456d6c453478556b51554a6856662b4876436344436a394a694f67683163500a56656579665235495a616b5757773d3d0a2d2d2d2d2d454e442050524956415445204b45592d2d2d2d2d0a"
print("RSA_HEX - len:",len(hex_key))

private_key = hex_to_priv(hex_key)

input_file = "data/nostr1.txt"

with open(input_file, "r", encoding="utf-8") as file:
    plaintext = file.read()


#bytearray_text = bytearray(plaintext.encode())
## ctypes_array = (ctypes.c_ubyte * len(bytearray_text)).from_buffer(bytearray_text)
#ctypes_buffer = ctypes.create_string_buffer(bytearray_text)
#ctypes_pointer = ctypes.cast(ctypes_buffer, ctypes.POINTER(ctypes.c_ubyte))
#print(ctypes_pointer)
#message = ctypes_pointer # # bytearray(plaintext.encode())
#message = message = plaintext.encode("utf-8")


message = b"secret text - via hex key 12345678901234567890 - longer text?" 
#                     1         2         3         4         5         6
#           0123456789012345678901234567890123456789012345678901234567890

ciphertext = private_key.public_key().encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print(ciphertext)


print("get_env_key")
hex_key_env = get_env_key("RSA")
private_key_env = hex_to_priv(hex_key_env)


print("-"*39)
plaintext_env = private_key_env.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print(plaintext_env)








