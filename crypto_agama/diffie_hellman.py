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
# Parameters for Diffie-Hellman
G = 3  # Generator 3, 123
M127 = 170141183460469231731687303715884105727  # Modulo prvočíslo 17, 9973, 1000009999, 123456789011, M61=2305843009213693951, M127
# print("M127:", 2**127-1, " :.",len(str(2**127-1))) #  Mersenne prime M127 :. 39 digits

class DiffieHellmanKeys:
    def __init__(self, g=3, p=M127):
        self.g = g  # Base / Generator
        self.p = p  # Modulus / Prime
        self.shared_secret = ""
        self.public_key = ""
        self.print_info = False

    def __repr__(self):
        return f"DiffieHellmanKeys\n(g = {self.g}, p = {self.p}) \n"

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


    def is_primitive_root(self, g, p):
        """ Check if g is a primitive root modulo p"""
        if g <= 1 or g >= p:
            return False

        required_set = set(num for num in range(1, p))  # only for "small" p!
        actual_set = set(pow(g, powers, p) for powers in range(1, p)) # Compute the powers of g mod p
    
        return required_set == actual_set


    def get_hex_shared32(self):
        M32 = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF # MASK for 16 Bytes (16*2 Hex_chars)
        secret_16B = self.shared_secret & M32
        return hex(secret_16B)[2:]
