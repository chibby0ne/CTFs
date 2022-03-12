#!/usr/bin/env python


# Output from server
stack = '0x8da1430.0x804b000.0x80489c3.0xf7efed80.0xffffffff.0x1.0x8d9f160.0xf7f0c110.0xf7efedc7.(nil).0x8da0180.0x3.0x8da1410.0x8da1430.0x6f636970.0x7b465443.0x306c5f49.0x345f7435.0x6d5f6c6c.0x306d5f79.0x5f79336e.0x62633763.0x65616336.0xfff7007d.0xf7f39af8.0xf7f0c440.0xa44c5d00.0x1.(nil).0xf7d9bce9.0xf7f0d0c0.0xf7efe5c0.0xf7efe000.0xfff70718.0xf7d8c68d.0xf7efe5c0.0x8048eca.0xfff70724.(nil).0xf7f20f09.0x804b000.0xf7efe000.0xf7efee20.0xfff70758.0xf7f26d50.0xf7eff890.0xa44c5d00.0xf7efe000.0x804b000.0xfff70758.0x8048c86.0x8d9f160.0xfff70744.0xfff70758.0x8048be9.0xf7efe3fc.(nil).0xfff7080c.0xfff70804.0x1.0x1.0x8d9f160.0xa44c5d00.0xfff70770.(nil).(nil).0xf7d41fa1.0xf7efe000.0xf7efe000.(nil).0xf7d41fa1.0x1.0xfff70804.0xfff7080c'

if __name__ == "__main__":
    # Find the start of the flag
    search_string = '0x' + ''.join([str(hex(ord(c))).lstrip('0x') for c in reversed('pico')])
    start_pos = stack.find(search_string)

    end = start_pos + stack[start_pos:].find('.')
    value = stack[start_pos: end].lstrip('0x')

    ans = []
    while start_pos != -1:
        # Since it is little endian we append the ASCII character represented
        # by every 2 hex digits from back to front, for every word, up until we
        # find terminating character '\0' which is "00" in hex
        for i in range(len(value), 1, -2):
            c = str(value[i - 2: i])
            if c == '00':
                print(''.join(ans))
                exit(0)
            ans.append(chr(int(c, base=16)))

        # Update the start position. Find returns the index relative to the
        # starting position of the given range therefore end and start_pos must
        # be added in order to advance in the string
        start_pos = end + stack[end:].find('0x')
        end = start_pos + stack[start_pos:].find('.')
        value = stack[start_pos:end].lstrip('0x')
 





    # Read until finding '00'
