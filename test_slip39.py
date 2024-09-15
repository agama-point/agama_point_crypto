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
