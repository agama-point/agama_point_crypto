"""
Agama Point - simple AES_XOR example
XOR-CBC (Cipher Block Chaining)
C1 = B1 (+) IV, C2 = B2 (+) C1 ... previous_block
"""

def xor_bytes(a, b):
    """XOR two byte arrays of the same length"""
    return bytes(x ^ y for x, y in zip(a, b))

def pad(plaintext, block_size):
    """Pad plaintext to be a multiple of block_size using PKCS7 padding"""
    padding_len = block_size - (len(plaintext) % block_size)
    padding = bytes([padding_len] * padding_len)
    return plaintext + padding

def unpad(padded_plaintext):
    """Remove PKCS7 padding from plaintext"""
    padding_len = padded_plaintext[-1]
    return padded_plaintext[:-padding_len]

def simple_encrypt(plaintext, key, iv):
    """Encrypt plaintext using a simple XOR-based CBC-like method"""
    block_size = 16
    assert len(key) == block_size, "Key must be 16 bytes"
    assert len(iv) == block_size, "IV must be 16 bytes"
    
    plaintext = pad(plaintext, block_size)  # Ensure plaintext length is a multiple of block size
    ciphertext = b''
    previous_block = iv
    
    for i in range(0, len(plaintext), block_size):
        block = plaintext[i:i+block_size]
        xored_block = xor_bytes(block, key)  # Simplified 'encryption' using XOR with key
        encrypted_block = xor_bytes(xored_block, previous_block)  # XOR with previous block (or IV for the first block)
        ciphertext += encrypted_block
        previous_block = encrypted_block  # Use current encrypted block as IV for next block
    
    return ciphertext

def simple_decrypt(ciphertext, key, iv):
    """Decrypt ciphertext using a simple XOR-based CBC-like method"""
    block_size = 16
    assert len(key) == block_size, "Key must be 16 bytes"
    assert len(iv) == block_size, "IV must be 16 bytes"
    
    decrypted = b''
    previous_block = iv
    
    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i:i+block_size]
        xored_block = xor_bytes(block, previous_block)  # XOR with previous block (or IV for the first block)
        decrypted_block = xor_bytes(xored_block, key)  # Simplified 'decryption' using XOR with key
        decrypted += decrypted_block
        previous_block = block  # Use current block as IV for next block
    
    return unpad(decrypted)  # Remove padding after decryption

# Example usage
key = b'1234567890abcdef'  # 16 bytes key
iv = b'fedcba0987654321'  # 16 bytes IV
print("key", key.hex() ," :",len(str(key.hex())))
print("iv", iv.hex())

plaintext = b'agama test 567 - a neco navic? ...ale asi jen bez diakritiky :('  # Example plaintext (32 bytes)

ciphertext = simple_encrypt(plaintext, key, iv)
print(f'Ciphertext: {ciphertext.hex()} ({len(str(ciphertext.hex()))})')

decrypted_text = simple_decrypt(ciphertext, key, iv)
print(f'Decrypted text: {decrypted_text.decode()}')
