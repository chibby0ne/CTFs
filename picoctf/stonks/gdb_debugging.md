If we look closely at what is happening when using `%x` and when we use `%p`

```
(gdb) x /20x $sp
0x7fffffffd510: 0xffffd698      0x00007fff      0x00000001      0x00000001
0x7fffffffd520: 0x55554040      0x00005555      0x555592a0      0x00005555
0x7fffffffd530: 0x697007f0      0x54436f63      0x65687b46      0x007d6568
0x7fffffffd540: 0x252e7825      0x78252e78      0x2e78252e      0x252e7825
0x7fffffffd550: 0x78252e78      0x2e78252e      0x252e7825      0x78252e78
```

```
(gdb) x /s flag
0x7fffffffd532: "picoCTF{hehe}"
```
or seeing it in hex

```
(gdb) x /4x flag
0x7fffffffd532: 0x6f636970      0x7b465443      0x65686568      0x7825007d
```

where:

`0x70` is `'p'`
`0x69` is `'i'`
`0x63` is `'c'`
`0x6f` is `'o'`
`0x43` is `'C'`
`0x54` is `'T'`
`0x46` is `'F'`
`0x78` is `'{'`
`0x68` is `'h'`
`0x65` is `'e'`
`0x68` is `'h'`
`0x65` is `'e'`
`0x7d` is `'}'`


When we printf using the `%x` format specifier (more specifically `%x.` 20
times in a sequence) we see this in `stdout` (partial output cut due to size)


```
5555b4a0.0.1.f7f2d3e0.0.ffffd698.1.55554040.555592a0.697007f0.65687b46.252e7825.2e78252e.78252e78
```

These numbers are of course hexadecimal according to the definition of
`printf` format specifier: Unsigned hexadecimal integer. More information: [printf](https://www.cplusplus.com/reference/cstdio/printf/)

If we try correlating this output with the output of the 20 neighbouring words in memory from the stack
pointer, we see that the first few numbers that we can correlate are:

`ffffd698.1`

`0xffffd698` is in the address: `0x7fffffffd510`
and in that same line:
`0x00000001` is in the address: `0x7fffffffd518`

The same applies for the next part of the stdout:

`55554040.555592a0`

This relates to the second line starting in address: `0x7fffffffd520`

`55554040` is in `0x7fffffffd520`
`555592a0` is in `0x7fffffffd528`

And finally we arrive at the neighborhood of where the `flag` variable is
stored in memory:

`697007f0.65687b46`

The `6970` is `'ip'` and the `65687b46` is `'eh{F'` in ASCII.

`697007f0` is in 0x7fffffffd530
`65687b46` is in 0x7fffffffd538


Now the question that eluded me was: where were the missing bytes?
Since these bytes should be contiguous to one another why were they not being
shown when using `%x`.

The question would be answered after looking at the output using `%p` format
specifier instead of the `%x`:

(nil).0xffffffff.0x7ffff7e79257.(nil).0xffffdc83.0x7fffffffd698.0x100000001.0x555555554040.0x5555555592a0.0x54436f63697007f0.0x7d656865687b46.0x78252e78252e7825.0x252e78252e78252e

After using this I could analyze the output and realize that the problem I was
facing was one that in fact is expected. It's not a bug, it's a feature.

If we look again at the definition of the format modifier `x` it says that the
regular length of the data type corresponds to `unsigned int` which in my
machine would be 32bit.

Now when we used `%p` since I was running a 64-bit machine and OS, the
addresses are 64-bit wide, and therefore was able to see the complete contents
of the memory.

Using `%x` would actually only print the top 4 bytes (32 bits) of the 8
bytes (64 bits) word and thus giving the appearance that these bytes were
missing somehow and that's the reason why it would not show bytes in the range
`04`-`07` and `0c`-`0f` of any given 16 bytes (2 words) of memory.



## Examining memory

```
(gdb) info frame
```

```
(gdb) bt
```

```
(gdb) x /10xw SOMEADDRESS
```
