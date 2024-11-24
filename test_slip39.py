from crypto_agama.slip0039 import simple_slip39_parse, validate_checksum


print("="*50)
#test_words0 = "webcam withdraw academic acid capital"
test_words = "herald flea academic cage avoid space trend estate dryer hairy evoke eyebrow improve airline artwork garlic premium duration prevent oven"
simple_slip39_parse(test_words) #, member_count=3)

print("="*50)
ext = 0  # Choose 0 or 1 depending on the mnemonic
# Validate checksum with detailed debug output (print_debug=True by default)
is_valid = validate_checksum(test_words, ext)
print(f"Checksum valid: {is_valid}")


"""
Indices: [999, 1009, 0, ... ] webcam withdraw academic acid ... ??? https://iancoleman.io/slip39/ error!
1111100111 1111110001 0000000000 0000000001 ...
111110011111111  1  0001  0000  0000  0000  0000  0001 

==================================================
Indices: [434, 352, 0, 114, 62, 843, 934, 299, 247, 420, 305, 322, 458, 21, 55, 385, 689, 250, 692, 633]
Binary string: 01101100100101100000000000000000011100100000111110110100101111101001100100101011001111011101101001000100110001010100001001110010100000010101000011011101100000011010110001001111101010101101001001111001
Binary words: 0110110010 0101100000 0000000000 0001110010 0000111110 1101001011 1110100110 0100101011 0011110111 0110100100 0100110001 0101000010 0111001010 0000010101 0000110111 0110000001 1010110001 0011111010 1010110100 1001111001

===== Parsing Results =====
Identifier (ID) [15 bits]: 13899
Extensibility (EXT) [1 bit]: 0
Iteration exponent [4 bits]: 0
Group index [4 bits]: 0
Group threshold [4 bits]: 0 (actual value: 1)
Number of groups [4 bits]: 0 (actual value: 1)
Member index [4 bits]: 7
Member threshold [4 bits]: 2 (actual value: 3)
Shared secret data [remaining bits]: 0000111110110100101111101001100100101011001111011101101001000100110001010100001001110010100000010101000011011101100000011010110001001111101010101101001001111001 (160)

===== Interpretation =====
This secret has the identifier (ID): 13899
Extensibility: 0
Iteration exponent: 0
Total number of groups: 1
Group threshold: 1
This share belongs to the group with index: 0
Member threshold: 3
Member index: 7

To recover the secret, 1 out of 1 groups are needed.
In this group, 3 shares are required to recover the part of the secret.
The total number of shares in this group is not stored in this share and must be known from another source.

Err.???
==================================================
Complete mnemonic: herald flea academic cage avoid space trend estate dryer hairy evoke eyebrow improve airline artwork garlic premium duration prevent oven
Checksum words: ['duration', 'prevent', 'oven']
Mnemonic words: ['herald', 'flea', 'academic', 'cage', 'avoid', 'space', 'trend', 'estate', 'dryer', 'hairy', 'evoke', 'eyebrow', 'improve', 'airline', 'artwork', 'garlic', 'premium', 'duration', 'prevent', 'oven']
Main part (without checksum): ['herald', 'flea', 'academic', 'cage', 'avoid', 'space', 'trend', 'estate', 'dryer', 'hairy', 'evoke', 'eyebrow', 'improve', 'airline', 'artwork', 'garlic', 'premium']
Indices of main part: [434, 352, 0, 114, 62, 843, 934, 299, 247, 420, 305, 322, 458, 21, 55, 385, 689]
Indices of main part: [434, 352, 0, 114, 62, 843, 934, 299, 247, 420, 305, 322, 458, 21, 55, 385, 689]
Indices of main part: [434, 352, 0, 114, 62, 843, 934, 299, 247, 420, 305, 322, 458, 21, 55, 385, 689]
Customization string: shamir
RS message (indices + customization string): [434, 352, 0, 114, 62, 843, 934, 299, 247, 420, 305, 322, 458, 21, 55, 385, 689, 115, 104, 97, 1Indices of main part: [434, 352, 0, 114, 62, 843, 934, 299, 247, 420, 305, 322, 458, 21, 55, 385, 689]
Customization string: shamir
Indices of main part: [434, 352, 0, 114, 62, 843, 934, 299, 247, 420, 305, 322, 458, 21, 55, 385, 689]
Indices of main part: [434, 352, 0, 114, 62, 843, 934, 299, 247, 420, 305, 322, 458, 21, 55, 385, 689]
Indices of main part: [434, 352, 0, 114, 62, 843, 934, 299, 247, 420, 305, 322, 458, 21, 55, 385, 689]
Customization string: shamir
RS message (indices + customization string): [434, 352, 0, 114, 62, 843, 934, 299, 247, 420, 305, 322, 458, 21, 55, 385, 689, 115, 104, 97, 109, 105, 114]
Calculated checksum (indices): [17, 16, 16]
Expected checksum indices (from words): [250, 692, 633]
Calculated checksum: [17, 16, 16]
Expected checksum indices: [250, 692, 633]
Checksum valid: False
"""
