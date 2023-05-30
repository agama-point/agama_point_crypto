from crypto_agama.agama_cipher import caesar_encrypt

s = 13
text = "pokus agama 123 a nějaký špeky" # so better just no spaces without diacritics and numbers

print("-"*50)
print("Plain Text : " + text)
print("Shift pattern : " + str(s))
print("Cipher: " + caesar_encrypt(text,s))

print("Test decrypt: " + caesar_encrypt("CBXHF NTNZN RST N ARWNXN JCRXL",s))
print("-"*50)

"""
--------------------------------------------------
Plain Text : pokus agama 123 a nějaký špeky
Shift pattern : 13
Cipher: CBXHF NTNZN RST N ARWNXN JCRXL
Test decrypt: POKUS AGAMA EFG A NEJAKA WPEKY
--------------------------------------------------
"""
