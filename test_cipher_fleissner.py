from lib.agama_cipher import fleissner_decrypt
# inspir: https://github.com/Zetsuban/Fleissner-Grid/blob/master/fleissner.py


f7_A = ((0,1),(0,4),(0,5),(1,2),(2,1),(2,4),(3,0),(3,4),(4,0),(5,1),(5,3),(6,6)) # inverse
f7_a = ((0,3),(0,4),(1,0),(1,2),(1,5),(2,1),(3,5),(4,0),(4,2),(4,3),(5,0),(6,6)) 
f7_B = ((0,1),(0,5),(1,2),(1,4),(2,3),(3,0),(3,1),(4,4),(4,6),(5,5),(6,4),(6,6)) #i
f7_b = ((0,3),(1,0),(1,3),(2,1),(3,2),(4,1),(4,4),(4,6),(5,0),(5,5),(6,4),(6,6)) 
f7_C = ((0,2),(0,6),(1,0),(1,5),(2,4),(3,2),(3,6),(4,1),(4,5),(5,0),(5,3),(6,2)) #i
f7_c = ((0,1),(0,5),(1,4),(2,0),(2,3),(2,6),(3,5),(4,2),(5,1),(5,4),(6,0),(6,3)) 


t48 = "123456789012345678901234567890123456789012345678"
t48 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUV"
t48 = "------------============abcdefghijkl............"

# print(fleissner_decrypt(t48, f=f7_b, ccw=False, center="a"))
# print(fleissner_decrypt(t48, f=f7_b, ccw=True, center="a")) # ok
print(fleissner_decrypt(t48, f=f7_a, ccw=False, center="A"))

"""
print(fleissner_decrypt(t48, f=f7_B, ccw=True, center="b"))
print(fleissner_decrypt(t48, f=f7_b, ccw=True, center="c"))
print(fleissner_decrypt(t48, f=f7_a, ccw=True, center="A"))
print(fleissner_decrypt(t48, f=f7_b, ccw=True, center="B"))
print(fleissner_decrypt(t48, f=f7_c, ccw=True, center="C"))
"""
# print(fleissner_decrypt(t48, f=f7_C, ccw=True, center="C",debug=True))

"""
...

abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUV 48
K a m y L b z
n M A o c B N
d p O e C q f
P D r C Q g s
E R h F t S G
u i H T j v U
k I w l V J x
"""
