# ecc

# cyclic supbgroup
# group operation: point addition: add P (+) Q = R / doubling P (+) P = 2P
# scalar multiplication

"""
XX, YY = X1 * X1 % p, Y1 * Y1 % p
YYYY = YY * YY % p
S = 2 * ((X1 + YY) ** 2 - XX - YYYY) % p
M = 3 * XX + a

T = (M * M - 2 * S) % p
# X3 = T

Y3 = (M * (S - T) - 8 * YYYY) % p
//Z3 = 2 * Y1 % p

return T, Y3, //Z3
"""

# --- Extended Euclidean algorithm
def _euclid(sml, big):
    #When the smaller value is zero, it's done, gcd = b = 0*sml + 1*big
    if sml == 0:
        return (big, 0, 1)
    else:
        #Repeat with sml and the remainder, big%sml
        g, y, x = _euclid(big % sml, sml)
        #Backtrack through the calculation, rewriting the gcd as we go. From the values just
        #returned above, we have gcd = y*(big%sml) + x*sml, and rewriting big%sml we obtain
        #gcd = y*(big - (big//sml)*sml) + x*sml = (x - (big//sml)*y)*sml + y*big
        return (g, x - (big//sml)*y, y)


# --- Compute the multiplicative inverse mod n of a with 0 < a < n
def mult_inv(a, n):  # mult_inv(2*P_1.y, self.char))
    g, x, y = _euclid(a, n)
    #If gcd(a,n) is not one, then a has no multiplicative inverse
    if g != 1:
        raise ValueError('multiplicative inverse does not exist')
    #If gcd(a,n) = 1, and gcd(a,n) = x*a + y*n, x is the multiplicative inverse of a
    else:
        return x % n
