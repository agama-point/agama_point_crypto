#!/usr/bin/env python
"""
crypto_agama/
agama_seed_tools 2016-24
---------------------------
"""

import hashlib, binascii, base58, hmac
from unicodedata import normalize
from hashlib import sha256
from .seed_english_words import english_words_bip39
from .agama_transform_tools import str_to_hex, short_str, convert_to_base58
from .agama_transform_tools import bin_to_hex, hex_to_bin
from .cipher import caesar_encrypt
#from mnemonic import Mnemonic

__version__ = "0.3.2" # 2024/06


DEBUG = True
TW = 80 # terminal width

MAINNET_PREFIX = '80'
TESTNET_PREFIX = 'EF'
#mnemo = Mnemonic("english")

BASE_58_CHARS = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
BASE_58_CHARS_LEN = len(BASE_58_CHARS)


def safe_hexlify(a):
    return binascii.hexlify(a)


def safe_from_hex(s):
    return s.decode('hex')


bh2u = safe_hexlify
hfu = binascii.hexlify
bfh = safe_from_hex
hmac_sha_512 = lambda x, y: hmac.new(x, y, hashlib.sha512).digest()


def seed_words():
    from crypto_agama.seed_english_words import english_words_bip39
    return english_words_bip39.split(",")

bip39 = seed_words()


def entropy_normalize(entropy):
    if len(entropy) < 39: # -> hexa
        print("[ hex input ]")
        bin_entropy = hex_to_bin(entropy)
    if len(entropy) > 127: # -> bin
        print("[ bin input ]")
        bin_entropy = entropy.replace(" ", "")
        entropy = bin_to_hex(bin_entropy)
        
        existing_hex_str = str(entropy)[2:]  # delete "0x"
        desired_length = 32

        if len(existing_hex_str) < desired_length:
            padding_length = desired_length - len(existing_hex_str)
            # print("padding_length",padding_length)
            existing_hex_str = '0' * padding_length + existing_hex_str

        entropy = existing_hex_str # without 0x
    return entropy



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



# --- josh-kean/BIP39 --- 2018 #class containing all the hashing functions
class BIP39Functions:
    def __init__(self, entropy = None, result_word_list = None):
        ##self.word_list = open('crypto_agama/words.txt', 'r').readlines()
        ##self.word_list = [word[:-1] for word in self.word_list]
        self.word_list = seed_words()
        self.word_list_length = len(self.word_list)
        self.entropy = entropy
        self.entropy_bin = None
        self.entropy_hex = None
        self.result_word_list = result_word_list
        self.binary_seed = None
        self.passphrase = 'agAma'
        self.check_sum = None


    def create_binary_ent(self):
        b = len(self.entropy)*4
        if b <= 128:
            self.entropy_bin = format(int(self.entropy, 16), "0128b")
        elif b <= 160:
            self.entropy_bin = format(int(self.entropy, 16), "0160b")
        elif b <= 192:
            self.entropy_bin = format(int(self.entropy, 16), "0192b")
        elif b <= 224:
            self.entropy_bin = format(int(self.entropy, 16), "0224b")
        elif b <= 256:
            self.entropy_bin = format(int(self.entropy, 16), "0256b")


    def get_input(self, user_input):
        self.entropy = user_input
        #need cases to ensure binary is 128, 160, 192, 224, or 256 bits long
        self.create_binary_ent()


    #checksum is created by taking the first len(ent) (in this case 256 bits)/32 bits of sha256 of entropy
    def create_check_sum(self):
        entropy_hash = hashlib.sha256(bytes.fromhex(self.entropy)).hexdigest()
        entropy_hash = format(int(entropy_hash,16), "0256b")#converts entropy hash to binary
        self.check_sum = entropy_hash[:len(self.entropy_bin)//32]


    def create_word_list(self):
        ent_and_chk = f'{self.entropy_bin}{self.check_sum}'
        self.result_word_list = ' '.join([self.word_list[int(ent_and_chk[11*x:11*(x+1)],2)] for x in range(len(ent_and_chk)//11
)])

    def create_binary_seed(self):
        self.binary_seed = hashlib.pbkdf2_hmac('sha512', str.encode(self.result_word_list), str.encode('mnemonic'+self.passphrase), 2048).hex()


    def master_key(self):
        entropy = self.get_input()
        chk_sum = self.check_sum()
        word_list = self.create_word_list()
        master_k = self.create_master_key()


    def entropy_to_phrase(self, entropy):
        self.get_input(entropy)
        self.create_check_sum()
        self.create_word_list()
        phrase = self.result_word_list
        return phrase


    # returns tuple (is_checksum_valid, is_wordlist_valid, entropy)
    def is_checksum_valid(self, mnemonic, reverse_entropy = False):
        words = [ normalize('NFKD', word) for word in mnemonic.split()]
        words_len = len(words)
        wordlist = self.word_list # wordlist_english
        n = len(wordlist)
        checksum_length = 11*words_len//33
        entropy_length = 32*checksum_length
        i = 0
        words.reverse()
        while words:
            w = words.pop()
            try:
                k = wordlist.index(w)
            except ValueError:
                return False, False
            i = i*n + k
        if words_len not in [12, 15, 18, 21, 24]:
            return False, True
        entropy = i >> checksum_length
        checksum = i % 2**checksum_length
        h = '{:x}'.format(entropy)
        while len(h) < entropy_length/4:
            h = '0'+h
        b = bytearray.fromhex(h)
        hashed = int(hfu(hashlib.sha256(b).digest()), 16)
        calculated_checksum = hashed >> (256 - checksum_length)
        if reverse_entropy:
            return checksum == calculated_checksum, True, h
        else:
            return checksum == calculated_checksum, True


    def words_to_entropy(self, words):
        """mneno 2 entr + checksum"""
        word_list = words.split()
        indices = [self.word_list.index(word) for word in word_list]
        bin_str = ''.join([f'{index:011b}' for index in indices])
        
        total_bits = len(bin_str)
        num_words = len(word_list)
        checksum_bits = num_words // 3
        entropy_bits = total_bits - checksum_bits
        
        self.entropy_bin = bin_str[:entropy_bits]
        self.check_sum = bin_str[entropy_bits:] if checksum_bits > 0 else ''

        hex_str = hex(int(self.entropy_bin, 2))[2:]
        # Zajistí, že délka hexadecimálního řetězce bude sudá (doplní nuly, pokud je potřeba)
        self.entropy_hex = hex_str.zfill((len(hex_str) + 1) // 2 * 2)
        
        return self.entropy_hex # self.entropy_bin, self.check_sum


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
  num_list = [] 
  w_arr = words.split()
  for _w in w_arr:
      _wnum = bip39.index(_w)
      print(_w, _wnum, end=" |")
      num_list.append(_wnum)
    
  return num_list


def bip39nums_to_words(num_arr):
  words = ""
  for _i in num_arr:
      _w = bip39[_i]
      words +=  _w + " "
  return words.rstrip()


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