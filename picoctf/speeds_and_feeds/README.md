# Speeds and feeds
Category: Reverse Engineering

## Description
> There is something on my shop network running at nc mercury.picoctf.net 59953, but I can't tell what it is. Can you?

## Solution

Connecting to the server returns a big list of G code instructions.

G-code are the most common programming language in CNC (Computer Numerical
Control). It's used in computer aided manufacturing and is the programming
language of choice for programming mills and lathes.

Our guess is that the movement of the tool renders the flag letters.

To prove this we need to render the movement of the tool in a coordinate
system used by G-code and then read what letters the movement's trace would
delineate.


Using an online G-code viewer like https://ncviewer.com/ and pasting the
G-code we are able to see the flag.


## Flag
picoCTF{num3r1cal_c0ntr0l_f3fea95b}
