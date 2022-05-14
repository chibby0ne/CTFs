# Matryoshka doll
Category: Forensics, 30 points

# Description
> Matryoshka dolls are a set of wooden dolls of decreasing size placed one inside another. What's the final one? Image: this

# Solution

Initially looked at the exif of the file, but everything looked OK, nothing
like a flag.

Then tried to grep keywords like "pico" and "CTF" out of the strings of the file with the `strings`.

After being stumped for a few minutes decided to look at the first hint, which
mentioned the fact that files could we hidden in other files, which prompted
me to search a bit on how this works for JPEG. 

First of a bit of theory, JPEG standard specifies the JPEG data stream, which
start with a SOI (Start of Image) and ends with a EOI (End of image). It
doesn't define a JPEG file format, therefore there could be bytes appended
after the EOI, and an image viewer would still render the image correctly.

Having said that looking at the magic numbers of the file I realized it's
actually a PNG, even though it is saved with a JPEG file extension.

Reading a bit more online I noticed that a lot of people use to JPEG file
extensions to place zipped archives, therefore tried to run unzip in the file
and got a directory and another pictures, and then tried the same approach
recursively until at about 4 levels deep we find a flag.txt file.

The file is identified as binary due to the number of NULL (`\0`) characters
in it, but opening it in vim we can discern the letters of it.

I used python to read until EOF and print the printable characters and got the flag.

# Flag
picoCTF{336cf6d51c9d9774fd37196c1d7320ff}
