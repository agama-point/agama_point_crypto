#!/usr/bin/env python
"""
crypto_agama/
agama_transform_tools 2016-24
-----------------------------
"""
from math import ceil
from hashlib import sha256
import binascii, zlib, base64
import re
# import hashlib, ecdsa

__version__ = "0.3.7" # 2024/01

DEBUG = False

"""
num_to_hex(255)           # '0xff'
hex_to_num('0xff')        # 255
num_to_bin(123)           # '0b1111011'
num_to_bin(123, True)     # '1111011' # to string
num_to_bin(123, True,11)  # '00001111011' # to string 11
hex_to_bin('0xff')        # '0b11111111'
hex_to_bin('0x3',True)    # 11 / to_string=True
hex_to_bin4('0x3')        # 0011

bin_to_hex('0b11111111')  # '0xff'
bin_to_hex('0b11111111',True,5) # '000ff'

bin_to_hex( "110011001")  # 0x199  1100110011 / L9
bin8_to_hex("110011001")  # 0xcc01 110011001 00000001 / L16 last?

str_to_hex("abc")         # '616263' # ASCII
str_to_bin("abc")         #'110000111000101100011'
bin_to_str('110000111000101100011') # x?  b'\x18qc'
bin8_to_hex?
bin_to_str?
int_to_bytes?
bytes_to_hex: >>> b'\xde\xad\xbe\xef'.hex() # 'deadbeef'

short_str("abcdefghijklmnopqrtsuvwxyz")     # 'abcdefghijkl...opqrtsuvwxyz'
short_str("abcdefghijklmnopqrtsuvwxyz",3)   # 'abc...xyz'
text_to_bits("abc")                         # '011000010110001001100011' # ASCII code
text_from_bits('011000010110001001100011')  # 'abc'

pattern = hex_to_bin(str_to_hex("ab8"),to_string=True)
# 11000010110001000111000
bin_normalize8("11000010110001000111")      # 11000010110001000111000 [len 8]
bin_to_str("11000010110001000111000")       # ab8

hash_sha256_str("agama") # '52589fac98630c603bd5c2b08cb0f6ccf273cc4a4772f0ff28d49a01bc7d2f4b'

hashhex = hash_sha256_str("agama")
hashnum = int(hashhex, 16)
convert_to_base58(hashnum) # '6YSp1VMaYGo5enJRFFwhhcNmrhGWPmJgSZqiS2sv3fwQ'

num_to_wif | wif_to_num | is_valid_wif
seed_words | num_to_address

---- adv arr
bin_arr_from_str(string, 32, False)     # bin_data32 arr from ascii str latin1
bin_data = bin_arr_from_str(string, 64) # bin_data64 str\n
"""

BASE_58_CHARS = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
BASE_58_CHARS_LEN = len(BASE_58_CHARS)


def hash_sha256_str(string):
    """
    Return a SHA-256 hash of the given string
    """
    return sha256(string.encode('utf-8')).hexdigest()


def convert_to_base58(num):
    sb = ''
    while (num > 0):
        r = num % 58   # divide by 58 and gives the remainder
        sb = sb + BASE_58_CHARS[r]
        num = num // 58
    return sb[::-1]


def num_to_hex(num):
   # ret = num.to_bytes(((integer.bit_length() + 7) // 8),"big").hex()
   ret = hex(num)
   return ret


def hex_to_num(hex):
  return int(hex, 16)


def hex_to_bin(hex_number, to_string = False):
  #bin(private_key1.to_bin())
  _bin = bin(int(hex_number, base=16))
  if to_string:
    return str(_bin)[2:]
  else:
    return _bin


def hex_to_bin4(hex_number):
    binary_number = "".join(format(int(c, 16), "04b") for c in hex_number)
    return binary_number


def pad_string_left(text, length=11, padding_char='0'):
    padding_length = length - len(text)
    if padding_length <= 0:
        return text
    else:
        padded_text = padding_char * padding_length + text
        return padded_text


def num_to_bin(num, to_string = False, length=11):
  _bin = bin(int(num))
  if to_string:
    return pad_string_left(str(_bin)[2:],length)
  else:
    return _bin


def bin_to_hex(binx, to_string = False, length=8):
   if to_string:
      return pad_string_left(str(hex(int(binx, 2)))[2:],length)
   else:
      return hex(int(binx, 2))


def bin8_to_hex(binary_number):
    hex_number = ""
    chunks = [binary_number[i:i+8] for i in range(0, len(binary_number), 8)]
    for chunk in chunks:
        hex_digit = hex(int(chunk, 2))[2:] #.zfill(2)
        hex_number += hex_digit

    hex_number = "0x" + hex_number
    return hex_number


def bin8_to_hex_old(strh):	
   tB = []
   tBs ="0x"	
   try:
     for ib in range (0,160):
       Bapp = bin_to_hex("0b"+str(strh)[2+ib*8:2+ib*8+8])	 
       tB.append(Bapp)
       print(Bapp,end="")
       tBs = tBs+tB[ib][2:4]
       #print ib,tB[ib]
   except: 
     err=True
     print(ib,end="")
   return tBs


def str_to_hex(str_txt, code='utf-8'):   # 'utf-8' / 'latin-1'
  # string_to_ascii
  # hex_data = bytes.fromhex(string).hex()
  # hex_data = string.encode('latin-1').hex()
  if len(code)>0:
     ascii_hex = str_txt.encode(code).hex()
  else:
     ascii_hex = str_txt.encode("ascii").hex()
  return ascii_hex


def hex_to_str(hex_data,code='utf-8'):
  if len(code)>0:
     string = bytes.fromhex(hex_data).decode(code)
  else:
     string = bytes.fromhex(hex_data).decode()
  return string


def str_to_bin(str_txt):
  # res = bin(reduce(lambda x, y: 256*x+y, (ord(c) for c in str), 0))
  res = ''.join(format(ord(i), 'b') for i in str_txt)
  return res


def bin_to_str(bin):
  n = int(bin, 2)
  return binascii.unhexlify('%x' % n)


def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int_to_bytes(n).decode(encoding, errors)


def int_to_bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1))) 


def short_str(s,l=12):
  return str(s[:l])+"..."+str(s[-l:])


# ------------------------ hexdump -------------------------
def group(a, *ns):
  for n in ns:
    a = [a[i:i+n] for i in range(0, len(a), n)]
  return a


def join(a, *cs):
  return [cs[0].join(join(t, *cs[1:])) for t in a] if cs else a


def hexdump(data):
  toHex = lambda c: '{:02X}'.format(c)
  toChr = lambda c: chr(c) if 32 <= c < 127 else '.'
  make = lambda f, *cs: join(group(list(map(f, data)), 8, 2), *cs)
  hs = make(toHex, '  ', ' ')
  cs = make(toChr, ' ', '')
  for i, (h, c) in enumerate(zip(hs, cs)):
    print ('{:010X}: {:48}  {:16}'.format(i * 16, h, c))

# -------------------------- extract numbers from string
def extract_numbers(s):
    nums = re.findall(r'\d+', s)
    return ''.join(nums)

# -------------------------- hard split human readable "11bits" from long number
def split_numbers(result_string):
    numbers = []
    current_number = ''
    
    for digit in result_string:
        current_number += digit
        if int(current_number) >= 2048:
            numbers.append(int(current_number[:-1]))
            current_number = digit
    
    # Add the last remaining number to the list
    numbers.append(int(current_number))
    
    return numbers

# ----- numeral systems /  conversions -------------------------
def decimal_to_base(number, base, zfill=5):
    if number == 0:
        return '0'

    result = ''
    while number:
        number, remainder = divmod(number, base)
        result = str(remainder) + result


    return result.zfill(zfill) if result else '0'


def base_to_decimal(base_number, base):
    if base == 4:
        valid_digits = set('0123')
    elif base == 5:
        valid_digits = set('012345')
    elif base == 6:
        valid_digits = set('012345')
    elif base == 7:
        valid_digits = set('0123456')
    else:
        return "Invalid base"

    if any(digit not in valid_digits for digit in base_number):
        return "Invalid input"

    decimal = 0
    power = len(base_number) - 1
    for digit in base_number:
        decimal += int(digit) * (base ** power)
        power -= 1
    return decimal


# ---------------------------zip -------------------------------
def zip_compress(data): # b'ABC'
    compressed_data = zlib.compress(data)
    if DEBUG: print(data, "compressed to",compressed_data)
    encoded_data = base64.b64encode(compressed_data)
    return encoded_data


def zip_decompress(encoded_data):
    compressed_data = base64.b64decode(encoded_data)
    data = zlib.decompress(compressed_data)
    return data


# --------------- adv. arr --------------------------
def bin_arr_from_str(s, bits=64, to_str=True):
    if to_str:
        bin_data = ""
    else:
        bin_data = []

    hex_data = str_to_hex(s,'latin-1')
    delx = int(bits/64*16)
    parts_num = ceil(len(hex_data)/delx)
    padded_hex = hex_data.ljust(int(parts_num*delx), "5") # 32/64*16=8, 64>16
    #if bits == 64:
    #    padded_hex = hex_data.ljust(parts_num*bits/64*16, "5")
    #else:
    #    padded_hex = hex_data.ljust(parts_num*8, "5")
    if DEBUG:
      print(padded_hex)
      print('latin-1 hex: 345678901234567890123456789012345678901234567890123')
      print('          1         2         3         4         5         6   ')
      print(hex_data, len(hex_data), len(hex_data)/8)
      print(padded_hex, len(padded_hex), parts_num)
      print(hex_to_str(hex_data,'latin-1'))
    
    bp = int(bits/32) # 32: 1 / 64: 2
    for part in range(int(parts_num)):
        part8 = padded_hex[bp*part*8:bp*part*8+8*bp]
        bin_part = num_to_bin(hex_to_num(part8),True,bits)
        if to_str:
            bin_data += bin_part + "\n"
        else:
            bin_data.append(bin_part)

    return bin_data


def str_from_bin_arr(bin_data):
  hex_data = ""
  s = ""
  for line in bin_data.splitlines():
      # cleaned_line = line.strip() # for arr
      str1 = bin_to_hex(str(line),True,8)
      try:
          s += hex_to_str(str1,'latin-1')
      except:
          s += "???"
  return(s)


def bin_normalize8(bin_str):
    pattern = bin_str.rstrip('0')
    remainder = len(pattern) % 8
    if DEBUG: print("remainder",remainder)
    pattern += "0" * (7 - remainder) if remainder != 0 else ""
    return pattern
