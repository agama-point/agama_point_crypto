from crypto_agama.cipher import caesar_encrypt

s = 13
text = "pokus agama 123 a nějaký špeky" # takze lepe jen nez mezer a cisel

print("Plain Text : " + text)
print("Shift pattern : " + str(s))
print("Cipher: " + caesar_encrypt(text,s))

print("Test decrypt: " + caesar_encrypt("CBXHF NTNZN RST N ARWNXN JCRXL",s))

"""
Cipher: CBXHF NTNZN RST N ARWNXN JCRXL
Test decrypt: POKUS AGAMA EFG A NEJAKA WPEKY
"""
