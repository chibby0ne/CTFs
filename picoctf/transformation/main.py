#!/usr/bin/env python

"""
''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])

Notice that:
    We take 2 bytes are a time
    We get the 1st byte and shift it 8 bits to the left and then + to the 2nd byte and get that character representation


We need to reverse this:
    Take 2 bytes at a time
    Get the first byte as Unicode string by AND'ing with a 0xFF00 mask and shifting >> 8
    Get the second byte as Unicode string by AND'in with 0x00FF
    Add to a list of bytes

    After we go through all the characters then we join the list of strings into a single string
"""
    
ans = []
for c in '灩捯䍔䙻ㄶ形楴獟楮獴㌴摟潦弸弲㘶㠴挲ぽ':
    first = chr((ord(c) & 0xFF00) >> 8)
    second = chr(ord(c) & 0x00FF)
    ans.append(first)
    ans.append(second)

print(''.join(ans))
