from crypto_agama.cipher import fleissner_decrypt


f7_a = ((0,3),(0,4),(1,0),(1,2),(1,5),(2,1),(3,5),(4,0),(4,2),(4,3),(5,0),(6,6)) 
f7_b = ((0,3),(1,0),(1,3),(2,1),(3,2),(4,1),(4,4),(4,6),(5,0),(5,5),(6,4),(6,6)) 
f7_c = ((0,1),(0,5),(1,4),(2,0),(2,3),(2,6),(3,5),(4,2),(5,1),(5,4),(6,0),(6,3)) 


t48 = "123456789012345678901234567890123456789012345678"
t48 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUV"

# print(fleissner_decrypt(t48, f=f7_A, ccw=True, center="A"))
# print(fleissner_decrypt(t48, f=f7_B, ccw=True, center="B"))
# print(fleissner_decrypt(t48, f=f7_b, ccw=True, center="b"))
print(fleissner_decrypt(t48, f=f7_a, ccw=True, center="A"))
print(fleissner_decrypt(t48, f=f7_b, ccw=True, center="B"))
print(fleissner_decrypt(t48, f=f7_c, ccw=True, center="c"))

# print(fleissner_decrypt(t48, f=f7_C, ccw=True, center="C",debug=True))
