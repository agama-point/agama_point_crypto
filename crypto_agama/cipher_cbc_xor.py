# agama_point - cipher_cbc_xor-py.py

"""
CBC (Cipher Block Chaining)
C1 = (IV ⊕ B1) ⊕ K
C2 = (B2 ⊕ C1) ⊕ K
...

from crypto_agama.cipher_cbc_xor import CBC_XOR 
key, iv =  ..,..
plaintext = b'agama'  # Example plaintext (32 bytes)
cbc = CBC_XOR(key, iv)

ciphertext = cbc.encrypt(plaintext)
decrypted_text = cbc.decrypt(ciphertext)
"""


class CBC_XOR:
    def __init__(self, key, iv, block_size=16):
        """
        Inicializuje CBC_XOR šifru.
        
        :param key: 16-bajtový klíč (v tomto příkladu).
        :param iv: 16-bajtový inicializační vektor.
        :param block_size: Velikost bloku (defaultně 16 bajtů).
        """
        self.key = key
        self.iv = iv
        self.block_size = block_size
        
        assert len(self.key) == self.block_size, "Key must be of the size block_size"
        assert len(self.iv) == self.block_size, "IV must be of the size block_size"

    def xor_bytes(self, a, b):
        """XOR dvě pole bajtů stejné délky"""
        return bytes(x ^ y for x, y in zip(a, b))

    def pad(self, plaintext):
        """Pad plaintext na velikost bloku pomocí PKCS7 paddingu"""
        padding_len = self.block_size - (len(plaintext) % self.block_size)
        padding = bytes([padding_len] * padding_len)
        return plaintext + padding

    def unpad(self, padded_plaintext):
        """Odstraní PKCS7 padding z plaintextu"""
        padding_len = padded_plaintext[-1]
        return padded_plaintext[:-padding_len]

    def encrypt(self, plaintext):
        """
        Šifruje plaintext pomocí CBC režimu a XOR operace.
        
        :param plaintext: Plaintext k šifrování (musí být násobek block_size).
        :return: Zašifrovaný ciphertext.
        """
        plaintext = self.pad(plaintext)  # Ujistit se, že délka plaintextu je násobkem velikosti bloku
        ciphertext = b''
        previous_block = self.iv
        
        for i in range(0, len(plaintext), self.block_size):
            block = plaintext[i:i+self.block_size]
            xored_with_key = self.xor_bytes(block, self.key)  # XOR block s klíčem
            encrypted_block = self.xor_bytes(xored_with_key, previous_block)  # XOR s předchozím blokem (nebo IV pro první blok)
            ciphertext += encrypted_block
            previous_block = encrypted_block  # Použijte aktuální zašifrovaný blok jako IV pro další blok
        
        return ciphertext

    def decrypt(self, ciphertext):
        """
        Dešifruje ciphertext pomocí CBC režimu a XOR operace.
        
        :param ciphertext: Ciphertext k dešifrování.
        :return: Dešifrovaný plaintext.
        """
        decrypted = b''
        previous_block = self.iv
        
        for i in range(0, len(ciphertext), self.block_size):
            block = ciphertext[i:i+self.block_size]
            xored_with_prev = self.xor_bytes(block, previous_block)  # XOR s předchozím blokem (nebo IV pro první blok)
            decrypted_block = self.xor_bytes(xored_with_prev, self.key)  # XOR s klíčem
            decrypted += decrypted_block
            previous_block = block  # Použijte aktuální blok jako IV pro další blok
        
        return self.unpad(decrypted)  # Odstranit padding po dešifrování
