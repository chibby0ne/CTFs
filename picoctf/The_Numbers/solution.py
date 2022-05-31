#!/usr/bin/env python

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
code = [20, 8, 5, 14, 21, 13, 2, 5, 18, 19, 13, 1, 19, 15, 14]
picoctf = [16, 9 ,3, 15, 3, 20, 6]


def decode(code):
    word = []
    for c in code:
        letter = alphabet[c - 1] # Our array starts at position 0
        word.append(letter)
    return ''.join(word)

print(f"flag decoded: {decode(picoctf)}{{{decode(code)}}}")
