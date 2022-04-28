# Mind your Ps and Qs
Category: Cryptography, 20 points

## Description
> In RSA, a small e value can be problematic, but what about N? Can you decrypt this? values

## Solution

Given that the values file contains values for `c`, `n` and `e`, my first intuition
was to read the RSA article in wikipedia and figure out how these values are
used in the RSA algorithm.

From 

RSA is a public-key cryptographic system, whose basic principle is based in
modular exponentiation, and noting that it's very easy to find 3 very large
positive numbers `e`, `d` and `n` such that with modular exponentiation for
all `0 <= m < n`:

<img src="https://render.githubusercontent.com/render/math?math=(m^{e})^{d}\equiv m {\pmod {n}}">

and that knowing `e` and `n` or even `m`, it can be extremely difficult to find `d`.


The public key is represented by `n` and `e` and the private key by `d`. `m`
represents the message. And `c` represents the ciphertext.


What I did was read and try to first recreate the
[example](https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Example) given in
wikipedia, and was specifically interested in the decryption of the ciphertext
step.


The example has basically 4 steps:

* Choosing 2 primes `p` and `q` and from them generating `n` which will be
  used as the modulo for encryption and decryption operations. `n` is
  generated using the following formula:
  ```
  n = p * q
  ```

* With that calculating the `lambda(n)` using the formula:
  ```
  lambda(p) = p - 1
  lambda(q) = q - 1
  lambda(n) = lcm(p, q)
  ```
  Where `lcm` is a function for getting the least common multiple.
  NOTE: I also discovered that we could simply use `lambda(n) = lambda(p) *
  lambda(q)` and achieve the same result, this was used in other writeups for
  this CTF.
  
* Calculate the secret exponent `d`:
  ```
  d = e^(-1) (mod n)
  ```

* Now we can either encrypt or decrypt. To decrypt which is our case we can
  use `d` and `n`, to decrypt the `c` ciphertext.


Initially I tried a naive approach to find the prime factors of `n`, but gave
up after running it for a few minutes and realizing that it would take hours
if not days to even reach around a base of 40 digits which would be around the
sqrt of the given `n`.

Instead I used the [FactorDB](http://factordb.com/) which a database for
factors of arbitrary numbers numbers, with a web interface and there's also a
python package [factordb-python](https://pypi.org/project/factordb-python/).

Then I proceeded with the steps shown in the example of wikipedia writing up
the lcm, and decoding the message.

Additionally once the message was decoded, since it was in an integer format I
needed to convert it to string format by first formatting as hex and then,
using the built-in `bytes` class to create a byte representation that could
then be decoded using the default encoding of `utf-8`.

Reading the python documentation I learned that the meain difference between
`bytes` and `bytesarray` is that `bytes` is `inmutable` and `bytesarray` is
mutable. They both have pretty much the same API.

## Flag
picoCTF{sma11_N_n0_g0od_23540368}
