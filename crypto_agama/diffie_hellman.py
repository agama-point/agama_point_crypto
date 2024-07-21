# Ahama Point - simple Diffie-Hellman explanation

"""
g = 2   # Generator
p = 17  # Modulo prime number

# Alice and Bob choose their private keys
a = 5   # Alice's private key
b = 3   # Bob's private key

# Calculation of public keys
A = (g ** a) % p  # -> 15
B = (g ** b) % p  # -> 8

[a] private/secret | [A] public KEY
"""


class DiffieHellmanKeys:
    def __init__(self, p, g):
        self.p = p  # Modulus
        self.g = g  # Base
        self.shared_secret = ""
        self.public_key = ""
        self.print_info = False
 

    def modular_exponentiation(self, base, exp, mod):
        result = 1
        base = base % mod
        steps = exp.bit_length()  # Total number of bits in the exponent
        if self.print_info:
            print("\nProgress: ",end="")
        for i in range(steps):
            if self.print_info:
                # print(f"Progress: {((i + 1) / steps) * 100:.2f}%")
                print(".",end="")
            if (exp >> i) & 1:
                result = (result * base) % mod
            base = (base * base) % mod
        return result


    def generate_public_key(self, private_key):
        # public_key = self.g ** private_key % self.p
        self.public_key = self.modular_exponentiation(self.g, private_key, self.p)
        return self.public_key


    def generate_shared_secret(self, private_key, other_public_key):
        # shared_secret = other_public_key ** private_key % self.p
        self.shared_secret = self.modular_exponentiation(other_public_key, private_key, self.p)
        return self.shared_secret


    def get_hex_shared32(self):
        M32 = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF # MASK for 16 Bytes (16*2 Hex_chars)
        secret_16B = self.shared_secret & M32
        return hex(secret_16B)[2:]
