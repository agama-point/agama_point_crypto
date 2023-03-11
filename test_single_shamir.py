"""
$ ssss-split -t 3 -n 5
Generating shares using a (3,5) scheme with dynamic security level.
Enter the secret, at most 128 ASCII characters: Using a 168 bit security level.

1-58f87a22d7aa12358e93a81e53217cb681bb4ec36b
.....

$ ssss-combine -t 3
Enter 3 shares separated by newlines:
.....
Share [3/3]: 1-58f87a22d7aa12358e93a81e53217cb681bb4ec36b

Resulting secret: kobyla ma maly bok 23
"""

from lib.agama_shamir_lib import single_shamir_to_words, words_to_single_shamir


# test
s = "1-58f87a22d7aa12358e93a81e53217cb681bb4ec36b"


print("-"*55)
print(s)
print("-"*55)
print(single_shamir_to_words(s))

words = 'rapid marble badge gadget drastic culture innocent tube device craft salad sure danger excite brave scale'

print(words_to_single_shamir(words,2))

"""
-------------------------------------------------------
1-58f87a22d7aa12358e93a81e53217cb681bb4ec36b
-------------------------------------------------------
rest / change
2
(15, 2, 'rapid marble badge gadget drastic culture innocent tube device craft salad sure danger excite brave scale ')
58f87a22d7aa12358e93a81e53217cb681bb4ec36b
"""