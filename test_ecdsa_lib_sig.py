from crypto_agama.ecc import scalar_multiplication, sign_message, verify_signature


# Input data
private_key_hex = "F000000000000000000000000000000000000000000000000000000000000001"
private_key = int(private_key_hex, 16)
print("priv_key:", private_key)
message = "Hello, AgamaPoint!"

# Generate the public key from the private key
public_key_x, public_key_y = scalar_multiplication(private_key)
public_key = (public_key_x, public_key_y)

# Sign the message
r, s = sign_message(private_key, message)
print(f"Signature (r, s): ({r}, {s})")

# Verify the signature
valid = verify_signature(public_key, message, r, s)
print(f"Is the signature valid? {valid}")
