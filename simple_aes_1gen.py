# simple AES (Vygenerování a výpis Substituční tabulky)

def generate_SBox():
    SBox = [0] * 256
    for i in range(256):
        byte = i
        # SubBytes transformace
        byte = substitute_byte(byte)
        SBox[i] = byte
    return SBox

def substitute_byte(byte):
    # Non-linear substitution
    s = byte
    s = s ^ (s << 1) ^ (s & 0x80 and 0x1B or 0)
    return s & 0xFF

def print_SBox(SBox):
    for i in range(16):
        for j in range(16):
            print(format(SBox[i * 16 + j], '02X'), end=' ')
        print()

# - generate and print
SBox = generate_SBox()
print_SBox(SBox)
