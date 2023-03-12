from lib.agama_shamir_lib import zip_compress, zip_decompress

#                 1         2         3         4
#        123456789012345678901234567890123456789012345678
data = b'ABCDEFGHIJKLMNQHABCDEFGHGHABCDEFGHABCDXZABCDEFGH'
#      b'eJxzdHJ2cXVz93BEo1FFIqJgPAA7wQ0A'
print(data, "compressed to")

encoded_data = zip_compress(data)
print(encoded_data)

#---------------------------------------------------------
print("-"*30)
print("decode")
# encoded_data = 'eJxzdHJ2cXVz93BEo1FFIqIA21oK3A=='
data = zip_decompress(encoded_data)

print(data)


