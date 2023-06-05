# Agama Point simple ciphers library
# 2017-23

__version__ = "0.2.5"


"""
print "Plain Text : " + text
print "Shift pattern : " + str(s)
print "Cipher: " + caesar_encrypt(text,s)
"""


def caesar_encrypt(text,s=13,up=True):
   result = ""

   for i in range(len(text)):
      char = text[i]
      # Encrypt uppercase characters in plain text
      
      if (char.isupper() or (ord(char) == 32)):
         if(ord(char) == 32):
            result += " "
         else:
            result += chr((ord(char) + s-65) % 26 + 65)
      # Encrypt lowercase characters in plain text
      else:
         result += chr((ord(char) + s - 97) % 26 + 97)
   if (up): 
      result = result.upper()
   
   return result



""" polybius code - basic an simple way:
- 1 2 3 4 5
1 A B C D E
2 F G H I K
3 L M N O P
4 Q R S T U
5 V W X Y Z
"""
p1 = {
"A": "11", "B": "12", "C": "13", "D": "14", "E": "15",
"F": "21", "G": "22", "H": "23", "I": "24", "K": "25",
"L": "31", "M": "32", "N": "33", "O": "34", "P": "35",
"Q": "41", "R": "42", "S": "43", "T": "44", "U": "45",
"V": "51", "W": "52", "X": "53", "Y": "54", "Z": "55"
}

def polybius_decrypt(text, p=p1):
   polyb = ""
   for ch in text:
      try:
         _i = ch.upper()
         _pi = p[_i]
         # print(ch, _pi)
         polyb += _pi + " "
      except:
         print("polybios_decrypt.Err")
   return polyb


# function to display polybius cipher text 
def polybius_cipher(s): 
   for char in s:

      row = int((ord(char) - ord('a')) / 5) + 1 # finding row of the table
      col = ((ord(char) - ord('a')) % 5) + 1 # finding column of the table
      if char == 'k': 
            row = row - 1
            col = 5 - col + 1
      # if character is greater than 'j' 
      elif ord(char) >= ord('j'): 
            if col == 1 : 
                  col = 6
                  row = row - 1
            col = col - 1
      print(row, col, end ='', sep ='')



f7_x = ((),(),(),(),(),(),(),(),(),(),(),()) # template
# f7_A = ((0,1),(0,4),(0,5),(1,2),(2,1),(2,4),(3,0),(3,4),(4,0),(5,1),(5,3),(6,6)) # inverse
f7_a = ((0,3),(0,4),(1,0),(1,2),(1,5),(2,1),(3,5),(4,0),(4,2),(4,3),(5,0),(6,6)) 
# f7_B = ((0,1),(0,5),(1,2),(1,4),(2,3),(3,0),(3,1),(4,4),(4,6),(5,5),(6,4),(6,6)) #i
f7_b = ((0,3),(1,0),(1,3),(2,1),(3,2),(4,1),(4,4),(4,6),(5,0),(5,5),(6,4),(6,6)) 
# f7_C = ((0,2),(0,6),(1,0),(1,5),(2,4),(3,2),(3,6),(4,1),(4,5),(5,0),(5,3),(6,2)) #i
f7_c = ((0,1),(0,5),(1,4),(2,0),(2,3),(2,6),(3,5),(4,2),(5,1),(5,4),(6,0),(6,3)) 

# t48 = "123456789012345678901234567890123456789012345678x" #48+1
# matrix 7x7: size=7, ccw: counterclockwise

def fleissner_decrypt(text, f=f7_a, size=7,center="A", ccw = False, debug=False):
   f_temp ="-"*size*size
   if debug: print(text,len(text))
   # f_temp[0] = center
   i = int(3*size + 3)
   f_temp = f_temp[:i] + center + f_temp[i:]
   if debug: print(f_temp, len(f_temp))

   fl = list(f)
   fln = fl
   _i = 0
   _ii = 0

   for rotate in range(4):
      if debug:
         print("----- rotate ", rotate)
         print(fl)
      _i = 0

      for xy in fl:
         i = int(xy[0]*size + xy[1])
         f_temp = f_temp[:i] + text[_ii] + f_temp[i+1:]
         if ccw: fln[_i] = (size - fl[_i][1] - 1, fl[_i][0])
         else:   fln[_i] = (fl[_i][1], size - fl[_i][0] - 1)
         _i += 1
         _ii += 1

      if debug:
         print(f_temp)
         print("fln    ",fl)
      fl = fln
      if ccw: fl = sorted(fl, key=lambda tup: tup[0]*10+tup[1])
      # else:   fl = sorted(fl, key=lambda tup: tup[1]*10+tup[0], reverse=True)
      else:   fl = sorted(fl, key=lambda tup: tup[0]*10+tup[1])
      if debug: print("sorted ",fl)

   _j = 0
   for x in range(size):
      for y in range(size):
         print(f_temp[_j], end = " ")
         _j += 1
      print()


def xor_crypt(data,key): # simple XOR
    data_int = int(data, 16)
    key_int = int(key, 16)
    result = data_int ^ key_int
    # hex(result)[2:]
    return hex(result)[2:].zfill(len(data))
