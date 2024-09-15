# Loading the dictionary and creating the mapping
with open('crypto_agama/words_slip39.txt', 'r') as file:
    words = [line.strip() for line in file]

# Verifying the length of the dictionary
assert len(words) == 1024, "The dictionary must contain 1024 words."

# Creating a map from word to index
word_indices = {word: index for index, word in enumerate(words)}

# Defining the lengths of individual fields according to SLIP-0039
ID_LEN = 15
EXT_LEN = 1
ITERATION_EXP_LEN = 4
GROUP_INDEX_LEN = 4
GROUP_THRESHOLD_LEN = 4
GROUP_COUNT_LEN = 4
MEMBER_INDEX_LEN = 4
MEMBER_THRESHOLD_LEN = 4

HEADER_LEN = (ID_LEN + EXT_LEN + ITERATION_EXP_LEN + GROUP_INDEX_LEN +
              GROUP_THRESHOLD_LEN + GROUP_COUNT_LEN + MEMBER_INDEX_LEN +
              MEMBER_THRESHOLD_LEN)

# Function to extract bits from a binary string
def extract_bits(s, start, length):
    return int(s[start:start+length], 2)

# Function to parse the mnemonic phrase according to SLIP-0039
def simple_slip39_parse(mnemonic_phrase, member_count=None):
    test_word_list = mnemonic_phrase.strip().split()

    # Converting words to indices using the map
    indices = [word_indices[word] for word in test_word_list]
    print(f"Indices: {indices}")

    # Converting indices to 10-bit binary strings
    binary_words = [format(index, '010b') for index in indices]
    binary_for_parse = ''.join(binary_words)
    print(f"Binary string: {binary_for_parse}")
    print(f"Binary words: {' '.join(binary_words)}")

    # Ensuring the binary string has sufficient length
    if len(binary_for_parse) < HEADER_LEN:
        print("The binary string is too short to contain all header fields.")
        return
    else:
        position = 0
        id_value = extract_bits(binary_for_parse, position, ID_LEN)
        position += ID_LEN

        ext_value = extract_bits(binary_for_parse, position, EXT_LEN)
        position += EXT_LEN

        iteration_exponent = extract_bits(binary_for_parse, position, ITERATION_EXP_LEN)
        position += ITERATION_EXP_LEN

        group_index = extract_bits(binary_for_parse, position, GROUP_INDEX_LEN)
        position += GROUP_INDEX_LEN

        group_threshold = extract_bits(binary_for_parse, position, GROUP_THRESHOLD_LEN)
        position += GROUP_THRESHOLD_LEN

        group_count = extract_bits(binary_for_parse, position, GROUP_COUNT_LEN)
        position += GROUP_COUNT_LEN

        member_index = extract_bits(binary_for_parse, position, MEMBER_INDEX_LEN)
        position += MEMBER_INDEX_LEN

        member_threshold = extract_bits(binary_for_parse, position, MEMBER_THRESHOLD_LEN)
        position += MEMBER_THRESHOLD_LEN

        # The rest is the shared secret data
        share_value_bits = binary_for_parse[position:]

        # Add 1 to the threshold values and counts
        actual_group_count = group_count + 1
        actual_group_threshold = group_threshold + 1
        actual_member_threshold = member_threshold + 1

        # Print values with descriptions
        print("\n===== Parsing Results =====")
        print(f"Identifier (ID) [15 bits]: {id_value}")
        print(f"Extensibility (EXT) [1 bit]: {ext_value}")
        print(f"Iteration exponent [4 bits]: {iteration_exponent}")
        print(f"Group index [4 bits]: {group_index}")
        print(f"Group threshold [4 bits]: {group_threshold} (actual value: {actual_group_threshold})")
        print(f"Number of groups [4 bits]: {group_count} (actual value: {actual_group_count})")
        print(f"Member index [4 bits]: {member_index}")
        print(f"Member threshold [4 bits]: {member_threshold} (actual value: {actual_member_threshold})")
        print(f"Shared secret data [remaining bits]: {share_value_bits} ({len(share_value_bits)})")

        # Interpretation of the results
        print("\n===== Interpretation =====")
        print(f"This secret has the identifier (ID): {id_value}")
        print(f"Extensibility: {ext_value}")
        print(f"Iteration exponent: {iteration_exponent}")
        print(f"Total number of groups: {actual_group_count}")
        print(f"Group threshold: {actual_group_threshold}")
        print(f"This share belongs to the group with index: {group_index}")
        print(f"Member threshold: {actual_member_threshold}")
        print(f"Member index: {member_index}")

        # Output the threshold and number of shares
        print(f"\nTo recover the secret, {actual_group_threshold} out of {actual_group_count} groups are needed.")
        print(f"In this group, {actual_member_threshold} shares are required to recover the part of the secret.")
        if member_count:
            print(f"The total number of shares in this group is {member_count}.")
            print(f"To recover this part of the secret, {actual_member_threshold} out of {member_count} shares are needed.")
        else:
            print("The total number of shares in this group is not stored in this share and must be known from another source.")



# GF1024 class implements Reed-Solomon codec over GF(1024)
class GF1024:
    # Primitive polynomial for GF(1024), x^10 + x^3 + 1
    # This polynomial defines the finite field GF(1024)
    prim_poly = 0b10000000001

    def __init__(self):
        # Initialize exponentiation and logarithm tables
        self.exp_table = [0] * 1024
        self.log_table = [0] * 1024
        self.generate_tables()

    def generate_tables(self):
        # Generate exponentiation and logarithm tables for GF(1024)
        value = 1
        for i in range(1023):
            self.exp_table[i] = value
            self.log_table[value] = i
            value <<= 1
            # Apply the primitive polynomial if the value exceeds 10 bits
            if value & 1024:
                value ^= self.prim_poly
        self.exp_table[1023] = self.exp_table[0]

    # Addition in GF(1024) is simply XOR
    def gf_add(self, a, b):
        return a ^ b

    # Subtraction is identical to addition in GF(1024)
    def gf_subtract(self, a, b):
        return self.gf_add(a, b)

    # Multiplication in GF(1024) using exponent and logarithm tables
    def gf_multiply(self, a, b):
        if a == 0 or b == 0:
            return 0
        return self.exp_table[(self.log_table[a] + self.log_table[b]) % 1023]

    # Division in GF(1024) using exponent and logarithm tables
    def gf_divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Division by zero in GF(1024)")
        if a == 0:
            return 0
        return self.exp_table[(self.log_table[a] - self.log_table[b]) % 1023]

    # Power in GF(1024) using the exponentiation table
    def gf_pow(self, a, power):
        if a == 0:
            return 0
        return self.exp_table[(self.log_table[a] * power) % 1023]

    # Inversion in GF(1024)
    def gf_inverse(self, a):
        return self.gf_pow(a, 1022)


# RS1024 class for encoding with Reed-Solomon over GF(1024)
class RS1024:
    def __init__(self, gf):
        self.gf = gf

    # Encode the message using Reed-Solomon encoding
    def encode(self, message, nsym):
        generator = [1]
        # Build generator polynomial
        for i in range(nsym):
            generator = self.poly_multiply(generator, [1, self.gf.exp_table[i]])

        # Pad the message with zeros for encoding
        message_padded = message + [0] * nsym
        for i in range(len(message)):
            coef = message_padded[i]
            if coef != 0:
                for j in range(len(generator)):
                    message_padded[i + j] ^= self.gf.gf_multiply(generator[j], coef)

        # Return the last 'nsym' elements as the checksum
        return message_padded[-nsym:]

    # Polynomial multiplication in GF(1024)
    def poly_multiply(self, p, q):
        result = [0] * (len(p) + len(q) - 1)
        for j in range(len(q)):
            for i in range(len(p)):
                result[i + j] ^= self.gf.gf_multiply(p[i], q[j])
        return result

# Initialize the Galois field and Reed-Solomon encoder
gf1024 = GF1024()
rs1024 = RS1024(gf1024)

# Load the wordlist and create the mapping of words to indices
def load_words(file_path='crypto_agama/words_slip39.txt'):
    with open(file_path, 'r') as file:
        words = [line.strip() for line in file]
    assert len(words) == 1024, "The dictionary must contain 1024 words."
    return words, {word: index for index, word in enumerate(words)}

# Load the words and word indices
words, word_indices = load_words()

# Calculate the checksum for the mnemonic phrase
def calculate_checksum(mnemonic, ext, print_debug=True):
    words = mnemonic.split()
    if print_debug:
        print(f"Mnemonic words: {words}")  # Debug: List of mnemonic words

    # Remove the last 3 words (the checksum)
    main_part = words[:-3]
    if print_debug:
        print(f"Main part (without checksum): {main_part}")  # Debug: Main part of mnemonic

    # Convert words to their corresponding indices
    indices = [word_indices[word] for word in main_part]
    if print_debug:
        print(f"Indices of main part: {indices}")  # Debug: Indices of main words
    
    # Use customization string based on 'ext' (0 for 'shamir', 1 for 'shamir_extendable')
    customization_string = "shamir_extendable" if ext == 1 else "shamir"
    if print_debug:
        print(f"Customization string: {customization_string}")  # Debug: Customization string used

    # Encode the message using RS1024
    rs_message = indices + [ord(c) for c in customization_string]  # Convert the string to list of numbers
    if print_debug:
        print(f"RS message (indices + customization string): {rs_message}")  # Debug: RS message including customization string
    
    checksum = rs1024.encode(rs_message, 3)  # Encode and get the last 3 words as checksum
    if print_debug:
        print(f"Calculated checksum (indices): {checksum}")  # Debug: Calculated checksum indices

    return checksum

# Validate if the checksum in the mnemonic is correct
def validate_checksum(mnemonic, ext, print_debug=True):
    words = mnemonic.split()
    if print_debug:
        print(f"Complete mnemonic: {mnemonic}")  # Debug: Full mnemonic

    # The last three words are the checksum
    checksum_words = words[-3:]
    if print_debug:
        print(f"Checksum words: {checksum_words}")  # Debug: Extracted checksum words

    # Calculate the checksum from the mnemonic
    calculated_checksum = calculate_checksum(mnemonic, ext, print_debug)

    # Convert checksum words into their corresponding indices
    expected_checksum_indices = [word_indices[checksum_words[0]], word_indices[checksum_words[1]], word_indices[checksum_words[2]]]
    if print_debug:
        print(f"Expected checksum indices (from words): {expected_checksum_indices}")  # Debug: Expected checksum indices from words

    # Final debug output for comparison
    if print_debug:
        print(f"Calculated checksum: {calculated_checksum}")
        print(f"Expected checksum indices: {expected_checksum_indices}")

    # Return True if calculated checksum matches expected checksum
    return calculated_checksum == expected_checksum_indices

"""
# Example usage
mnemonic = "herald flea academic cage avoid space trend estate dryer hairy evoke eyebrow improve airline artwork garlic premium duration prevent oven"
ext = 0  # Choose 0 or 1 depending on the mnemonic

# Validate checksum with detailed debug output (print_debug=True by default)
is_valid = validate_checksum(mnemonic, ext)
print(f"Checksum valid: {is_valid}")

# Validate checksum with less verbose output (print_debug=False)
is_valid = validate_checksum(mnemonic, ext, print_debug=False)
print(f"Checksum valid (less verbose): {is_valid}")
"""