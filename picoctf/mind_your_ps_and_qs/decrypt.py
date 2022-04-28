#!/usr/bin/env python

from factordb.factordb import FactorDB

c = 240986837130071017759137533082982207147971245672412893755780400885108149004760496
n = 831416828080417866340504968188990032810316193533653516022175784399720141076262857
e = 65537

# Wikipedia example
# c = 2790 # This should be 65(int), 'A'(str)
# n = 3233
# e = 17


# Using euclid's algorithm
def gcm(a, b):
    bigger = a
    smaller = b
    if b > a:
        smaller = a
        bigger = b

    while bigger % smaller != 0:
        multiple = bigger // smaller
        diff = bigger - smaller * multiple

        bigger = smaller
        smaller = diff
    return smaller
    
def lcm(a, b):
    return (a * b) // gcm(a, b)

if __name__ == "__main__":

    # Recover p and q
    f = FactorDB(n)
    f.connect()
    p, q = f.get_factor_list()
    print(f"p: {p}, q: {q}")

    # Lambda_n
    lambda_p = p - 1
    lambda_q = q - 1
    lambda_n = lcm(lambda_p, lambda_q)
    print(f"lambda_n: {lambda_n}")

    # d
    d = pow(e, -1, lambda_n)
    print(f"d: {d}")

    # plaintext
    m = pow(c, d, n)
    print(f"m: {m}")

    # Decode the plaintext to unicode
    print(bytes.fromhex(format(m, 'x')).decode())





    

