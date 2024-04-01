from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# from Crypto.Random import get_random_bytes
### pip install pycryptodome -> Crypto


# Definujeme veřejné parametry
G = 2  # Generátor
n = 17  # Modulo prvočíslo

# Alice a Bob si zvolí své soukromé klíče
a = 5  # Soukromý klíč Alice
b = 3  # Soukromý klíč Bob

# Výpočet veřejných klíčů
A = (G ** a) % n
B = (G ** b) % n

print("A, B",A, B)

# Výpočet společného klíče
s_Alice = (B ** a) % n
s_Bob = (A ** b) % n

# Kontrola, zda mají oba stejný společný klíč
print("společný klíč:", s_Alice, s_Bob)
assert s_Alice == s_Bob

# Symetrické šifrování a dešifrování
def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return ciphertext

def decrypt_message(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode()

# Vytvoření symetrického klíče ze společného klíče
symmetric_key = str(s_Alice).zfill(16)[:16].encode()
print("symmetric_key:", symmetric_key)
print("===========================================")

# Zpráva od Alice pro Boba
message = "agama test"

# Zašifrování zprávy
encrypted_message = encrypt_message(message, symmetric_key)
print("Zašifrovaná zpráva:", encrypted_message)

# Dešifrování zprávy Bobem
decrypted_message = decrypt_message(encrypted_message, symmetric_key)
print("Dešifrovaná zpráva:", decrypted_message)
