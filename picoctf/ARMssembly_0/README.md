# ARMssembly 0
Category: Reverse Engineering, 30 points

# Description
> What integer does this program print with arguments 182476535 and
> 3742084308? File: chall.S Flag format: picoCTF{XXXXXXXX} -> (hex, lowercase,
> no 0x, and 32 bits. ex. 5614267 would be picoCTF{0055aabb})

# Solution

Since this is a ARMv8 assembly we can't run it in *most* desktop computers so
we have to think (reverse engineer) our way through this one.

Reading the calling convention, adding comments next to the assembly lines and
We notice that there are 2 calls to `atoi` which converts char* to int, and we
know that the arguments passed to main are found in `argv`, which of type
pointer to char*, which fits to the usage of `atoi` to convert the arguments
from char* to int.

Afterwards there's a call to `func1`, which checks: `w1 <= w0`, which given
`w0 = 182476535` and `w1 = 3742084308`, the `CMP` is false and there's no jump
in the next instruction `bls`, which means then that `w0 = w1`, and the
function returns, and from there we maintain w0 and which is then copied to
w1 using `mov w1, w0` and is printed by the call to `printf` with first
argument "Result: %ld\n", and w1 as second argument.

We convert that value, `3742084308` to hex, and we get the contents of the flag
as specified in the description of the file.


# Flag
picoCTF{df0bacd4}
