# The Numbers
Category: Cryptography, 50 points

# Description
> The numbers... what do they mean?

# Solution

The picture is of a bunch of 1 and 2 digit numbers separated by spaces, some
of them surrounded by curly brackets. This was one of the main clues that we
had, besides it being of cryptography category. Here's a representation of the
numbers in the picture.

```
16 9 3 15 3 20 6 { 20 8 5 14 21 13 2 5 18 19 13 1 19 15 14 }
```

The intuition is that the numbers encode the letters of the flag, except
for the curly brackets. With this assumption in mind, we can verify that any
of the numbers are in fact <= the number of letters in the alphabet, which are
26, and in fact we find that the max number is 21. Also every number before
the opening curly bracket `{` should be the usual: `picoCTF` part of the flag,
which if true, we can then use to deduce the kind of perhaps rotation cipher
used.

Visualizing this assumption:

```
16 = p
9 = i
3 = c
15 = o
3 = C
20 = T
6 = F
```

We notice that the string is in fact the same length as the `picoCTF` one,
and the cipher is case insensitive i.e: a letter in upper or lower case will
get the same number, which means that for every number there could be 2
representations, that means that there is a number of permutations to be
tried for the same numbers.

Additionally we notice with the number `3 = c` that the number in fact
corresponds to the place in the alphabet of that letter, with `f` being the 6th
letter and `t` being the 20th. In an array with the letters of the alphabet in
order, we would of course, need to subtract 1 from the number to get the
right letter since arrays start at position (index) 0.

With this in mind we can write a script that generates the permutations with
this code in mind.

This is the point in time when a little back of the napkin math done before
the writing of code, pays off. This is a combination situation, each digit can
represent 2 chars (one lower case and one upper case), since the string we are
looking for (which is the one inside the curly brackets) has 15 chars (`20 8 5
14 21 13 2 5 18 19 13 1 19 15 14`), then that's 2 to the power of 15, which
ends up being 32768 possibilities.

Since we are not going to test all the options we started from the simplest by
trying out the all caps solution (`THENUMBERSMASON`), which wasn't valid. Then
tried the all lower case one (`thenumbersmason`) which also wasn't the valid
flag.

At this point in time we decided to look for the hint, which mentioned that
the prefix to the flag itself **should be: "PICOCTF"**, and that was the
missing piece to flag.

All in all this was an awful CTF just because you would not expect the prefix to
deviate from the custom, but I guess in this case, that's just how the cookie
crumbles.


# Flag
PICOCTF{THENUMBERSMASON}
