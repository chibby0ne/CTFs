# Easy Peasy
Category: Cryptography, 30 points

# Description
> A one-time pad is unbreakable, but can you manage to recover the flag? (Wrap
> with picoCTF{}) nc mercury.picoctf.net 20266

# Solution

Let's begin with `startup` function:

## Startup

Both the key and the flag are read from two files: key and flag respectively.

The function takes one parameter named `key_location`, which specifies the
start of the slice that makes up the key used as one-time pad. The key chosen
is of the same length of the flag and starts from the key_location byte of the
key file up to (but not including) the (key_location + FlagLength) byte of the
key file.

Then the result printed, is the concatenation of the hex representation of the
XOR of each byte of the code point of the flag and the value of key chosen.

This tells us that the key must be a numeric value, since we are not using the
code point transformation for each of their bytes as we did for the flag.

The `startup` function is invoked passing `0` as argument, i.e: `key_location
= 0` for startup. Therefore the key chosen starts from the 0th byte and ends
in the (not including) `FlagLength` byte.

The function returns the stop location which is effectively the **length of
the flag** since the stop location is the `key_location + len(flag)`.



## Encrypt

The `encrypt` function also takes a `key_location` as parameter and is also
used in a similar manner as the `startup` function, i.e: `key_location` marks
the starting position of the key slice. The `encrypt` function
also does the hex presentation of the XOR operation of the Unicode value of
the string given in the prompt (`ui`) and the key flag, one byte at a time.

Since XOR is a reversible operation, i.e: let `res` be the result of the XOR
between `a` and `b`, we can get either `a` or `b` by XORing `res` with the
other argument, therefore `a = res XOR b` and `b = res XOR a`. As long as we
have the `key` we can trivially decipher the flag.

Now the tricky thing is that we don't have direct access into the
`key_location`, instead we know from the code that the first time the loop is
called, that `c = FlagLength` and then the return value of `encrypt` is set to
c, which is also fed to `encrypt`.

This is the snippet of code while loop:
```
c = startup(0)
# c is the length of the flag initially
while c >= 0:
   c = encrypt(c)
```

The return value of `encrypt` function is actually a bit more complicated that
with the `startup` function, but is fundamental to how we break the one-pad
encryption, since the value returned is the argument used for the next
`encrypt` invocation:

`stop` is set to:
```
stop = key_location + len(ui)
```

But then it's mutated if and only if `stop >= 50000`, in this case, stop
is set to `stop % 50000`.
Finally `key_location = stop` and `key_location` is returned.

With these details we know 2 things:
1. The first time encrypt is invoked its argument is the length of the flag.
2. The argument `key_location` is used as the starting position of the key
   slice.
3. The return value is `key_location + len(input_string)` only if
   `len(input_string) < 50000` otherwise it's the `(key_location +
   len(input_string)) % 50000`.
4. The returned value of a previous invocation of encrypt is the
   `input_string` (is the argument) of the next invocation.


In addition, we can deduce the length of the key (and thereby the flag),
because it is printed in the `startup` function in an encrypted version.

```
5b1e564b6e415c0e394e0401384b08553a4e5c597b6d4a5c5a684d50013d6e4b
```

We know that was printed using `{:02x}` which means in hex form with lower
case characters for numbers > 9, with at least 2 digits, and 0 for padding.
TL;DR: we know that each value is transcribed into 2 characters in the output,
therefore the output should be a 2 times longer than the input.

```
len('5b1e564b6e415c0e394e0401384b08553a4e5c597b6d4a5c5a684d50013d6e4b') == 64
```

Therefore the **flag and key length should be 32**.

Knowing now that the `startup` is called with 0, and returns 32, we can now
formulate an strategy.

The main goal is to use a known string (submitted by us), let's name it `S`,
as the flag, and use that to get the encrypted version of `S` let's call it
`S'`. But the most important detail is that **we want to use the same key that
was used for the flag** as part of the encrypt XOR procedure, so that with
`S'` and `S` we can get the key.

And we know that the key starts at position 0, and ends in position 32th (31
index) of the file read.

Therefore the goal is to **invoke** `encrypt` **with** `starting_position = 0`
**and give it a string** `S` **with a length of 32 characters**.


Knowing these details, we can establish an strategy:

1. Enter a (50000 - 32) character length string as input, let's call it S.
   The reason we want to subtract these 32 characters is because if you
   remember from earlier, 32 is the argument passed to `encrypt` the first
   time, and this way, according to the condition:
   ```
   ...
   stop = key_location + len(S)
   if stop >= KEY_LEN:
      stop = stop % KEY_LEN
   ...
   key_location = stop
   ...
   return key_location
   ```

   This way we can set the return value `key_location` to `0`, which will be
   used for a future invocation.

2. Pass another string, let's call it `X`, of 32 characters long. Capture the
   output of the encrypt command, call it `X'`


3. Apply the reversing using `X'` and `X`, to get the Key used for the
   one-time pad encryption of the flag.

4. Apply the reversing using `Key` and the encrypted flag, to get the
   unencrypted flag.

Care must be taken, when converting the encrypted values since, they are
formatted as 0-padded 2 characters hex values, while the flag was read as
binary which means it was handled as bytes (int) and therefore we need to
apply the relevant transformations to int carefully to our `S'` and to our
encrypted flag.

The flag returned as the description mentioned needs to be wrapped by
`picoCTF{}`, since it just the contents inside that are returned.


# Flag

picoCTF{99072996e6f7d397f6ea0128b4517c23}
