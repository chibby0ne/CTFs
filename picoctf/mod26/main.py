#!/usr/bin/env python

import string

def rot13(s):
    ans = ''
    for c in s:
        if c not in string.ascii_letters:
            ans += c
            continue

        alphabet = string.ascii_lowercase
        if c in string.ascii_uppercase:
            alphabet = string.ascii_uppercase

        new_pos = (alphabet.find(c) + 13) % len(alphabet)
        ans += alphabet[new_pos]

    return ans

if __name__ == "__main__":
    print(f"{rot13(input())}")
