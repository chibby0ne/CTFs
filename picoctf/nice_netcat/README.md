# Nice netcat...
Category: General Skills, 15 points

## Description
> There is a nice program that you can talk to by using this command in a shell: $ nc mercury.picoctf.net 22902, but it doesn't speak English...

## Solution
Connecting to the server returns a bunch of positive numbers 1 per line.
Since the numbers appear in the range of ASCII values (< 256) I assumed they were and
we could decode them.
Therefore I stored them in a file and wrote a script to do so, as well as
concatenate them into a string, instead of having them one character.

```
$ nc mercury.picoctf.net 22902 > input
```
```
./main < input
```

## Flag
picoCTF{g00d_k1tty!_n1c3_k1tty!_d3dfd6df}
