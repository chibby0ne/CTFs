#!/usr/bin/env python

from new_caesar import b16_encode, shift, ALPHABET

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


assert 'hello' == b16_decode(b16_encode('hello'))

def reverse_shift(c_prime, k):
    t1_prime = ALPHABET.index(c_prime)
    t2 = ALPHABET.index(k)
    return ALPHABET[(t1_prime - t2) % len(ALPHABET)]


for k in ALPHABET:
    assert 'c' == reverse_shift(shift('c', k), k)



# flag = ""
# key = "redacted"
# assert all([k in ALPHABET for k in key])
# assert len(key) == 1

# b16 = b16_encode(flag)
# enc = ""
# for i, c in enumerate(b16):
# 	enc += shift(c, key[i % len(key)])
# print(enc)


# i % len(key)
# This is the same as i % 1, therefore the result of the operation will always be 0
# Therefore the shift's k parameter will always be key[0], which is actually key since key is of length 1.
# c is simply the character for the given index..


def decode_flag(encoded_flag):
    for k in ALPHABET:
        unshifted_encoded_flag = ''
        for c_prime in encoded_flag:
            unshifted_encoded_flag += reverse_shift(c_prime, k)
        flag = b16_decode(unshifted_encoded_flag)
        print(f"picoCTF{{{flag}}}")

if __name__ == "__main__":
    decode_flag("kjlijdliljhdjdhfkfkhhjkkhhkihlhnhghekfhmhjhkhfhekfkkkjkghghjhlhghmhhhfkikfkfhm")
