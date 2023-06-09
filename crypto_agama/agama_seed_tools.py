#!/usr/bin/env python

import hashlib, binascii, base58, hmac
from hashlib import sha256
from .seed_english_words import english_words_bip39
from .transform import str_to_hex, short_str, convert_to_base58
from .cipher import caesar_encrypt
#from mnemonic import Mnemonic

__version__ = "0.2.1" # 2023/06


DEBUG = True
TW = 80 # terminal width

MAINNET_PREFIX = '80'
TESTNET_PREFIX = 'EF'
#mnemo = Mnemonic("english")

BASE_58_CHARS = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
BASE_58_CHARS_LEN = len(BASE_58_CHARS)


def seed_words():
    from crypto_agama.seed_english_words import english_words_bip39
    return english_words_bip39.split(",")

bip39 = seed_words()


def mnemonic_info(words,short=True):
  if DEBUG:
      print("-" * TW) 
      print("[mnemonic_info]")
  from cryptos import keystore
  if short: print(short_str(words),end=" ")
  else: print(words)

  w_arr = words.split() # words_to_array
  print("(",len(w_arr),")")

  for _w in w_arr:
      _wnum = bip39.index(_w)
      if short: print(_wnum, end=" ")
      else:  print(_w, _wnum, end=" ")

  print()
  print("validate: ", keystore.bip39_is_checksum_valid(words))
  print("-" * TW) 


def generate_seed11(pattern):
    bits = pattern*int(256/len(pattern))
    print(bits) # 132 bits
    bw = 11 # BIP39 words 2048 == 11 bits
    words11 = ""

    for i in range(11): # 12 words: 11 + 1 chceksum
        wordbits = bits[bw*i:bw*(i+1)]
        wordindex = int(wordbits, 2) #bin2num
        #wordindex = int(f'{wordbits:#0}')
        try:
            word = bip39[wordindex]
            words11 +=  word + " "
        except:
            word = "err"
        print(i+1, wordbits, wordindex, word)
    return words11


def generate_seed11_num(numbers, multi=1): # multi: 1,2,3 max (3*999?)
    numbers = str(numbers)*2
    bw = 11
    words11 = ""

    for i in range(bw): # 12 words: 11 + 1 chceksum
        num3 = int(numbers[i*3:i*3+3])*multi 
        try:
            word = bip39[num3]
            words11 +=  word + " "
        except:
            word = "err"
        print(i+1, num3, word)
    return words11


def generate_seed11_num_list(num_list, multi=1): # (123,567,666,...)
    words11 = ""
    i = 0
    for num in num_list: # 12 words: 11 + 1 chceksum
        try:
            word = bip39[int(num)]
            words11 +=  word + " "
            i += 1
        except:
            word = "err"
    print("-> num nums: ", i)
    return words11


def generate_seed11_txt(text, multi=1):
    text_hex = str(str_to_hex(text))
    print(text_hex)
    bw = 11
    words11 = ""

    for i in range(bw): # 12 words: 11 + 1 chceksum
        num = int(text_hex[i*2:i*2+2],16)
        try:
            word = bip39[num]
            words11 +=  word + " "
        except:
            word = "err"
        print(i+1, num, word)
    return words11


def words_to_bip39nums(words):
  w_arr = words.split()
  for _w in w_arr:
      _wnum = bip39.index(_w)
      print(_w, _wnum, end=" ")


def words_to_4ch(words,c=13,separator=" ", str_w=True):
  _i = 0
  words4 = ""
  w_arr4 = words.split()

  for _w in w_arr4:
      if c: w_arr4[_i] = caesar_encrypt(_w[:4],c)
      else: w_arr4[_i] = _w[:4]
      words4 += w_arr4[_i] + separator
      _i += 1

  if str_w: return  words4
  else: return w_arr4


def w42w(we4, debug = True):
    if debug: print("[w4_2_w]")
    wr = "Err."
    for w in bip39: # words
        if w.startswith(we4):
            if debug: print(w, "="*5)
            wr = w
            break
        else:
            if w.startswith(we4[:3]):
                if len(w)==3:
                    if debug: print(w, "-"*5)
                    wr=w
                    break
    return wr


def mnemo_to_seed(mnemonic,passphrase=""):
    PBKDF2_ROUNDS = 2048
    # passphrase = "mnemonic" + passphrase
    mnemonic_bytes = mnemonic.encode("utf-8")
    passphrase_bytes = passphrase.encode("utf-8")
    stretched = hashlib.pbkdf2_hmac("sha512", mnemonic_bytes, passphrase_bytes, PBKDF2_ROUNDS)
    return stretched[:64]


def create_root_key(seed_bytes,version_BYTES = "mainnet_private"):
   # the HMAC-SHA512 `key` and `data` must be bytes:
   I = hmac.new(b'Bitcoin seed', seed_bytes, hashlib.sha512).digest()
   L, R = I[:32], I[32:]
   master_private_key = int.from_bytes(L, 'big')
   master_chain_code = R

   VERSION_BYTES = {
      'mainnet_public': binascii.unhexlify('0488b21e'), 'mainnet_private': binascii.unhexlify('0488ade4'),
      'testnet_public': binascii.unhexlify('043587cf'), 'testnet_private': binascii.unhexlify('04358394'),
   }

   print("version_BYTES: ", version_BYTES)

   version_bytes = VERSION_BYTES[version_BYTES] #  testnet_public
   depth_byte = b'\x00'
   parent_fingerprint = b'\x00' * 4
   child_number_bytes = b'\x00' * 4
   key_bytes = b'\x00' + L
   all_parts = (
      version_bytes,       #  4 bytes
      depth_byte,          #  1 byte
      parent_fingerprint,  #  4 bytes
      child_number_bytes,  #  4 bytes
      master_chain_code,   # 32 bytes
      key_bytes,           # 33 bytes
   )
   all_bytes = b''.join(all_parts)
   root_key = base58.b58encode_check(all_bytes).decode('utf8')
   return root_key


# def is_valid_wif(wifPriv):
#   return numToWIF(WIFToNum(wifPriv)) == wifPriv


def num_to_address(numPriv):
    pko = ecdsa.SigningKey.from_secret_exponent(numPriv, CURVE_TYPE)
    pubkey = binascii.hexlify(pko.get_verifying_key().to_string())
    pubkeySHA256Hash = sha256(binascii.unhexlify('04' + pubkey)).hexdigest()
    pubkeySHA256RIPEMD160Hash = hashlib.new('ripemd160', binascii.unhexlify(pubkeySHA256Hash)).hexdigest()

    hash1 = sha256(binascii.unhexlify('00' + pubkeySHA256RIPEMD160Hash)).hexdigest()
    hash2 = sha256(binascii.unhexlify(hash1)).hexdigest()
    checksum = hash2[:8]

    encodedPubKeyHex = pubkeySHA256RIPEMD160Hash + checksum
    encodedPubKeyNum = int(encodedPubKeyHex, 16)

    base58CharIndexList = []
    while encodedPubKeyNum != 0:
      base58CharIndexList.append(encodedPubKeyNum % BASE_58_CHARS_LEN)
      encodedPubKeyNum /= BASE_58_CHARS_LEN

    m = 0
    while encodedPubKeyHex[0 + m : 2 + m] == '00':
        base58CharIndexList.append(0)
        m = m + 2

    address = ''
    for i in base58CharIndexList:
      address = BASE_58_CHARS[i] + address

    return '1' + address


def ent_to_phrase(entropy): 
    #tests to see if provided entropy produces desired word list
    hashes = HashingFunctions()
    hashes.get_input(entropy)
    hashes.create_check_sum()
    hashes.create_word_list()
    phrase = hashes.result_word_list
    return phrase


def phrase_to_key(phrase): 
    #tests to see if word list converts to desired master key
    hashes = HashingFunctions(None, phrase)
    hashes.create_binary_seed()
    return hashes.binary_seed


def num_to_wif(numPriv,prefix=MAINNET_PREFIX,leading="1",debug=DEBUG):
  # base58.b58encode_check(bytes).decode('utf8')
  privKeyHex = prefix+hex(numPriv)[2:].strip('L').zfill(64)
  privKeySHA256Hash = sha256(binascii.unhexlify(privKeyHex)).hexdigest()
  privKeyDoubleSHA256Hash = sha256(binascii.unhexlify(privKeySHA256Hash)).hexdigest()
  checksum = privKeyDoubleSHA256Hash[:8]
  wifNum = int(privKeyHex + checksum, 16)
  if debug: print("DEBUG-wifNum: ", wifNum)
  wifNum58 = convert_to_base58(wifNum)
  if debug: print("DEBUG-wifNum58: ", wifNum58)
  return leading + wifNum58


def wif_to_num(wifPriv):
    numPriv = 0
    for i in range(len(wifPriv)):
      numPriv += BASE_58_CHARS.index(wifPriv[::-1][i])*(BASE_58_CHARS_LEN**i)

    numPriv = numPriv/(2**32)%(2**256)
    return numPriv


def create_root_key2(seed_bytes,version_BYTES = "mainnet_private"):
   print("--- _create_root_key: running ---")
   # the HMAC-SHA512 `key` and `data` must be bytes:
   I = hmac.new(b'Bitcoin seed', seed_bytes, hashlib.sha512).digest()
   L, R = I[:32], I[32:]
   master_private_key = int.from_bytes(L, 'big')
   master_chain_code = R
   print("hmac-sha512 (B2x): ", I.hex())
   print("master_private_key ", master_private_key)
   print("master_chain_code (B2x)", master_chain_code.hex())



   VERSION_BYTES = {
      'mainnet_public': binascii.unhexlify('0488b21e'), 
      'mainnet_private': binascii.unhexlify('0488ade4'),
      'testnet_public': binascii.unhexlify('043587cf'), 
      'testnet_private': binascii.unhexlify('04358394'),
   }

   print("version_BYTES: ", version_BYTES)

   version_bytes = VERSION_BYTES[version_BYTES] #  testnet_public
   depth_byte = b'\x00'
   parent_fingerprint = b'\x00' * 4
   child_number_bytes = b'\x00' * 4
   key_bytes = b'\x00' + L
   all_parts = (
      version_bytes,       #  4 bytes  
      depth_byte,          #  1 byte
      parent_fingerprint,  #  4 bytes
      child_number_bytes,  #  4 bytes
      master_chain_code,   # 32 bytes
      key_bytes,           # 33 bytes
   )
   all_bytes = b''.join(all_parts)
   print("all_bytes: ", all_bytes)
   print("all_bytes (b2x): ", all_bytes.hex())
   root_key = base58.b58encode_check(all_bytes).decode('utf8')
   print("root_key: ",root_key)
   return root_key

"""
def mnemo_to_seed_old(mnemonic):
    PBKDF2_ROUNDS = 2048
    # passphrase = "mnemonic" + passphrase
    mnemonic_bytes = mnemonic.encode("utf-8")
    passphrase_bytes = passphrase.encode("utf-8")
    stretched = hashlib.pbkdf2_hmac("sha512", mnemonic_bytes, passphrase_bytes, PBKDF2_ROUNDS)
    return stretched[:64]
"""
