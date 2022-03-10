#!/usr/bin/env python

import sys


if __name__ == "__main__":
    output = []
    for line in sys.stdin:
        output.append(chr(int(line.strip())))
    print(''.join(output))

