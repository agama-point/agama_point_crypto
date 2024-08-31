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

"""
priv_key: 108555083659983933209597798445644913612440610624038028786991485007418559037441
random_k: 111583794569822749533334261307317682780121412452982544101788556302902202281272 
hash_z:   46957728168510006349267012936007887871147273396380056022350853207462321186747
Signature (r, s): (25087459343984940959948366158697803135846104810457191245301314903304682375125, 78763891837782071723963155053684258666505492857818681864387969341472656388229)
Is the signature valid? True
"""