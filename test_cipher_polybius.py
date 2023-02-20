from lib.agama_cipher import polybius_decrypt

""" polybius code
- 1 2 3 4 5
1 A B C D E
2 F G H I K
3 L M N O P
4 Q R S T U
5 V W X Y Z
"""

print(polybius_decrypt("agama")) # --> 11 22 11 32 11
