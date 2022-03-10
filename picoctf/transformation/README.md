# Transformation
Category: Reverse Engineering, 20 points

# Description

> I wonder what this really is... enc ''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])

## Solution
The given code snippet shows how the encoded string was created. 
We noticed a few things:
* The encoded string contains Chinese characters.
* The encoding was done taking 2 bytes at a time
* The 1st byte is taken and shifted 8 bits to the left and then added to the
  2nd byte to get that character representation



First assumption was to do the reverse operation with the given encoded
string.

* Take 2 bytes a time
* Get the first character as Unicode string and AND'ing it with a 0xFF00 mask (so
  that we get the first byte) and then shift it to the right 8 positions, then
  convert it to char again.
  Append this character to the string.
* Get the second byte as unicode code string by AND'ing it with a 0x00FF mask
  (since this wasn't shifted), convert it to char again.
  Append this character to the string

This particular CTF made me read quite a bit about Unicode (a standard), character
encodings (e.g: UTF-8, UTF-16, ASCII, etc...), Chinese language in different
character encodings, and string representations in Python (stored using
Unicode UTF-8).

## Flag
picoCTF{16_bits_inst34d_of_8_26684c20}
