# Agama_point 2020-21
# crypto_agama.ecc

# cyclic supbgroup
# group operation: point addition: add P (+) Q = R / doubling P (+) P = 2P
# scalar multiplication


# --- Extended Euclidean algorithm - gcd: greatest common divisor
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
    g, x, y = _euclid(a, n) # g = x * a + y * n
    #If gcd(a,n) is not one, then a has no multiplicative inverse
    if g != 1:
        raise ValueError('multiplicative inverse does not exist')
    #If gcd(a,n) = 1, and gcd(a,n) = x*a + y*n, x is the multiplicative inverse of a
    else:
        return x % n


def point_doubling(px,py,a=0,p=17): # grupe doubling // add?
   s = (3*px*px + a) % p
   t = mult_inv(2*py, p)
   # print(s, t, s / t) # 2**-1 * 9 --- inversion ? --- 9*9 % 17 = 13 ok
   s = t * s % p
   x = (s*s - 2*px) % p
   y = (s*(px -x) - py) % p
   return x, y


def point_adding(px, py, qx, qy, p=17): # grupe doubling // add?
    lam = ((qy-py)  % p) * mult_inv(((qx-px) % p), p)
    rx = (lam*lam - px - qx) % p
    ry = (lam*(px - rx) - py) % p
    return rx, ry


# transform P => -P (P(x,y)=>P(x,-y)) # (-) y: reflect
def reflect_on_x(y, p):
   s = p//2
   delta = abs(y - s)
   if y > s: _y = s - delta
   if y < s: _y = s + delta

   return _y % p


# todo / inspiration
# https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication

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
