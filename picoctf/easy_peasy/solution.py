#!/usr/bin/env python

import subprocess

s = "What data would you like to encrypt? Here ya go!\n"
encrypted_flag = '5b1e564b6e415c0e394e0401384b08553a4e5c597b6d4a5c5a684d50013d6e4b'
decrypted_flag = '99072996e6f7d397f6ea0128b4517c23'
len_encrypted_flag = len(encrypted_flag)
len_flag = len_encrypted_flag // 2
KEY_LEN = 50000


def main():
    part1_inject = 'a' * (KEY_LEN - len_flag)   # To set the key_location = 0 for the second invocation
    part_2_inject = 'a' * (len_flag)            # To use the exact same key as was used for the flag encryption
    string_to_inject = part1_inject + '\n' + part_2_inject + '\n\n'

    p = subprocess.run('nc mercury.picoctf.net 20266'.split(' '),
                       input=string_to_inject,
                       capture_output=True,
                       text=True)
    # Only interested in the encrypted part_2_inject which is found inside the whole output
    start_interesting_output = p.stdout.rfind(s) + len(s)
    end_interesting_output = start_interesting_output + len_encrypted_flag
    interesting_output = p.stdout[start_interesting_output: end_interesting_output]

    # Decode the key
    key = []
    for i in range(0, len(interesting_output), 2):
        k = int(interesting_output[i: i + 2], 16) ^ ord('a')
        key.append(k)

    assert len(key) == len_flag

    # Decode the flag
    flag = []
    for i in range(0, len(encrypted_flag), 2):
        f = int(encrypted_flag[i : i + 2], 16) ^ key[i // 2]
        flag.append(chr(f))

    print(f"flag: {''.join(flag)}")



if __name__ == "__main__":
    main()
