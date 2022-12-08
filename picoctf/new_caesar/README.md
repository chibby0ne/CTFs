# New Caesar
Category: Cryptography

## Description
> We found a brand new type of encryption, can you break the secret code? (Wrap with picoCTF{}) kjlijdliljhdjdhfkfkhhjkkhhkihlhnhghekfhmhjhkhfhekfkkkjkghghjhlhghmhhhfkikfkfhm new_caesar.py

## Solution
We are given a script that shows how the ciphertext given in the description was
generated.

In addition, a few hints are given from the assertions in the code:

1. That the alphabet of all possible characters of the key is the first 16 lowercase letters
2. That the key is of length 1.

Therefore there are 16 possible keys.

What's left is to write the inverse procedure of whats done: one that takes
the cyphertext given with each one of the possible keys and checking if the
output contains the flag.

There are two operations.

* One that encodes which doesn't depend on a key and only depends on the
  cyphertext: `b16_encode`

* One that shifts a given character by a certain amount: `shift` 

The `shift` function uses the key.

If we look closely the  code does the following
 
```
enc += shift(c, key[i % len(key)])
```

But since we are certain that the len(key) == 1, then this means that the
modulo operation becomes: `i % 1` which is simply `0`.
This makes total sense since if key's length is 1, having an index > 0, would
result in an IndexError.

That gives us:

```
enc += shift(c, key)
```

That means we should shift all characters from the encoded string *with* the
same key.

So, first we create the reverse operation of the b16_encode:

```
def b16_decode(encoded_flag):
    dec = ""
    for index in range(0, len(encoded_flag), 2):
        up, lo = encoded_flag[index: index + 2]
        index_up = ALPHABET.index(up)
        index_lo = ALPHABET.index(lo)

        up_val = '{0:04b}'.format(index_up)
        lo_val = '{0:04b}'.format(index_lo)
        dec += chr(int(up_val + lo_val, 2))
    return dec
```

And we test it with the encode operation to make sure it works as intended
i.e: is the symmetrical operation of `b16_encode`

```
assert 'hello' == b16_decode(b16_encode('hello'))
```

Then we write the reverse_shift operation:

```
def reverse_shift(c_prime, k):
    t1_prime = ALPHABET.index(c_prime)
    t2 = ALPHABET.index(k)
    return ALPHABET[(t1_prime - t2) % len(ALPHABET)]
```

And again we test it with the shift operation and all the possible keys:

```
for k in ALPHABET:
    assert 'c' == reverse_shift(shift('c', k), k)
```

With this out of the way, we can simply do the same operations described in the file but
in reverse order:
* First we shift all characters to create a new string
* Then we decode the new string
* Print that string (to test it against picoCTF site)

```
def decode_flag(encoded_flag):
    for k in ALPHABET:
        unshifted_encoded_flag = ''
        for c_prime in encoded_flag:
            unshifted_encoded_flag += reverse_shift(c_prime, k)
        flag = b16_decode(unshifted_encoded_flag)
        print(f"picoCTF{{{flag}}}")
```

This gives us 16 strings to test, but out of all 16 many have unprintable
characters and other have non-ASCII characters.

```
picoCTF{©¸¸¹su¥§yªw¨{}vt¥|yzut¥ª©¦vy{v|wu¨¥¥|}
picoCTF{§§¨bdhfjleckhidcehjekfdk}
picoCTF{qQqSWUY[TRZWXSRTWYTZUSZ}
picoCTF{v`@`BrtFwDuHJCArIFGBArwvsCFHCIDBurrI}
picoCTF{et_tu?_1ac5f3d7920a85610afeb2572831daa8}
picoCTF{TcNcd.N PR$U"S&(!/P'$% /PUTQ!$&!'" SPP'}
picoCTF{CR=RS=OADBOODC@BOO}
picoCTF{2A,AB
>32?1>>}     ,>031
picoCTF{!01û
picoCTF{/
/ ê
ìàîâäíëãàáìëíàâíãîìã}
picoCTF{ùÙùÛ
ßÝÑÓÜÚ
      ÒßÐÛÚ

           ÜßÑÜÒÝÛ

                  Ò}
ÈèÊúüÎÿÌýÀÂËÉúÁÎÏÊÉúÿþûËÎÀËÁÌÊýúúÁ}
picoCTF{íü×üý·×¹éë½î»ì¿±º¸é°½¾¹¸éîíêº½¿º°»¹ìéé°}
picoCTF{ÜëÆëì¦Æ¨ØÚ¬ÝªÛ® ©§Ø¯¬­¨§ØÝÜÙ©¬®©¯ª¨ÛØØ¯}
picoCTF{ËÚµÚÛµÇÉÌÊÇÇÌËÈÊÇÇ}
picoCTF{ºÉ¤ÉÊ¤¶¸»¹¶¶»º·¹¶¶}
```

In fact we have a better clue as to which one it is with the name of the
cypher: `new_caesar`. One of the strings has the famous quote from Caesar to
Brutus while he was assasinated in the Senate: `et tu, Brutus?`

## Flag
picoCTF{et_tu?_1ac5f3d7920a85610afeb2572831daa8}
